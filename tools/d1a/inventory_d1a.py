"""Reproducible, offline D1-A source-header inventory and mapping coverage check.

Scope: the public header-only sample workbook, the D1-A mapping documents and the
draft contract header. The script emits header text, column identities and counts.
It never emits cell values from rows that are not declared header rows, so it does
not copy person data into evidence.

It does not freeze a business rule and it does not replace the Gate 0 runner
(tools/gate0/check_contract.py) or the formal MSVC / Win7 verification owned by C.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
SAMPLE = "reference/员工信息表11111.xlsx"
SAMPLE_SHA256 = "427727f5d8062e7cba699b35d9262fb594b717d3dd699f811cbb7475112cf5b6"
CONTRACT = "include/retiree_roster/schema_types.hpp"
REGION1_DOC = "docs/baseline/07_源表字段映射.md"
REGION2_DOC = "docs/baseline/02_字段映射与数据保留策略.md"
DISPOSITIONS = ("PersonField", "BatchRawOnly", "Unsupported")
REGION1_ROW = re.compile(
    r"^\| ([A-Z]{1,2}) \| ([^|]+?) \| ([^|]+?) \| (PersonField|BatchRawOnly|Unsupported) "
    r"\| ([^|]+?) \| ([^|]+?) \|$", re.M)
REGION2_ROW = re.compile(r"^\| ([A-Z]+) \| (.*?) \| (\w+) \| (\w+) \|$", re.M)
REGION_HEADER_DECL = re.compile(r"区域 (\d) 表头行（1 起算）：(\d+)")
DECLARED_KEYS = re.compile(r"^\- ([^：]+)：(.+)$", re.M)
DECLARED_SAMPLE = re.compile(r"样表：`([^`]+)`")
DECLARED_SHEET = re.compile(r"工作表：`([^`]+)`，维度 `([^`]+)`")


class CheckFailure(RuntimeError):
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or {}


def col_letter(index):
    letters = ""
    number = index + 1
    while number:
        number, remainder = divmod(number - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def col_index(letter):
    number = 0
    for char in letter:
        number = number * 26 + (ord(char) - 64)
    return number - 1


def compact(text):
    """Matching key: whitespace (including newlines) removed, case preserved."""
    return re.sub(r"\s+", "", text or "")


def display(text):
    """Readable single-line form: whitespace runs collapsed to one space."""
    return re.sub(r"\s+", " ", (text or "").strip())


def read_text(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def workbook_sheets(archive):
    """Return [(sheet_name, worksheet_part)] resolved through workbook rels."""
    book = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rel_ns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
    targets = {rel.get("Id"): rel.get("Target") for rel in rels.findall("r:Relationship", rel_ns)}
    sheets = []
    for sheet in book.findall("s:sheets/s:sheet", NS):
        rel_id = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = targets.get(rel_id, "")
        if target.startswith("/"):
            part = target.lstrip("/")
        elif target.startswith("xl/"):
            part = target
        else:
            part = "xl/" + target
        sheets.append((sheet.get("name"), part))
    return sheets


def cell_text(cell, shared):
    kind = cell.get("t")
    value = cell.find("s:v", NS)
    if kind == "s" and value is not None:
        return shared[int(value.text)]
    if kind == "inlineStr":
        return "".join(cell.find("s:is", NS).itertext())
    return value.text if value is not None else ""


def sheet_rows(root, shared):
    """{row_number: {column_index: raw text}} for cells that are not blank."""
    rows = {}
    for row in root.findall("s:sheetData/s:row", NS):
        number = int(row.get("r"))
        cells = {}
        for cell in row.findall("s:c", NS):
            reference = cell.get("r") or ""
            match = re.match(r"([A-Z]+)(\d+)$", reference)
            if match is None:
                continue
            text = cell_text(cell, shared)
            if text is not None and str(text).strip() != "":
                cells[col_index(match.group(1))] = str(text)
        if cells:
            rows[number] = cells
    return rows


def merged_ranges(root):
    return [node.get("ref") for node in root.findall("s:mergeCells/s:mergeCell", NS)]


def protected_ranges(root):
    return [(node.get("name"), node.get("sqref"))
            for node in root.findall("s:protectedRanges/s:protectedRange", NS)]


def sheet_dimension(root):
    node = root.find("s:dimension", NS)
    return node.get("ref") if node is not None else ""


def load_sample(relative):
    with ZipFile(ROOT / relative) as archive:
        names = archive.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(node.itertext()) for node in shared_root.findall("s:si", NS)]
        loaded = []
        for name, part in workbook_sheets(archive):
            root = ET.fromstring(archive.read(part))
            loaded.append({
                "sheet_name": name,
                "part": part,
                "dimension": sheet_dimension(root),
                "rows": sheet_rows(root, shared),
                "merges": merged_ranges(root),
                "protected_ranges": protected_ranges(root),
            })
    return loaded


def contract_facts():
    """Person field specs and the canonical fields reachable from ImportFieldId."""
    header = read_text(CONTRACT)
    specs = {}
    for spec in re.findall(
            r"\{FieldId::(\w+), \"([^\"]+)\", FieldValueKind::(\w+), (\w+), (\w+), (\w+), (\w+), (\w+), (\w+)\}",
            header):
        specs[spec[0]] = {
            "key": spec[1], "value_kind": spec[2],
            "required_for_import": spec[3] == "true", "sensitive": spec[4] == "true",
            "source_importable": spec[5] == "true", "user_editable": spec[6] == "true",
            "system_managed": spec[7] == "true", "printable_by_default": spec[8] == "true",
        }
    body = re.search(r"try_to_person_field\(ImportFieldId field, FieldId\* out\)\s*\{(.*?)\n\}",
                     header, re.S)
    if body is None:
        raise CheckFailure("cannot locate try_to_person_field(ImportFieldId)")
    importable = set(re.findall(r"case ImportFieldId::(\w+): \*out = FieldId::(\w+);", body.group(1)))
    # Fail closed: a silent contract-parse break must not turn every mapping check into a no-op.
    if not specs or not importable:
        raise CheckFailure("cannot parse person field specs or ImportFieldId targets from " + CONTRACT,
                           {"specs": len(specs), "import_pairs": len(importable)})
    return {
        "specs": specs,
        "import_targets": {target for _, target in importable},
        "import_pairs": sorted(importable),
    }


def parse_region1(text):
    rows = [{"letter": m[0], "title": display(m[1]), "key": compact(m[2]),
             "disposition": m[3], "target": display(m[4]), "note": display(m[5])}
            for m in REGION1_ROW.findall(text)]
    declared = {name.strip(): [item.strip() for item in value.split("、") if item.strip()]
                for name, value in DECLARED_KEYS.findall(text)}
    header_rows = {int(region): int(row) for region, row in REGION_HEADER_DECL.findall(text)}
    sample = DECLARED_SAMPLE.search(text)
    sheet = DECLARED_SHEET.search(text)
    return {"rows": rows, "header_rows": header_rows, "declared_keys": declared,
            "declared_sample": sample.group(1) if sample else None,
            "declared_sheet": (sheet.group(1), sheet.group(2)) if sheet else None}


def parse_region2(text, header_row):
    rows = [{"letter": m[0], "title": display(m[1]), "key": compact(m[1]),
             "disposition": "PersonField", "target": m[2], "member": m[3]}
            for m in REGION2_ROW.findall(text)]
    return {"rows": rows, "header_row": header_row}


def region_of(sheet, header_row, region_name, source):
    cells = sheet["rows"].get(header_row)
    if cells is None:
        raise CheckFailure("declared header row %d is empty in %s" % (header_row, source))
    return [{"letter": col_letter(index), "index": index, "raw": cells[index],
             "key": compact(cells[index]), "region": region_name}
            for index in sorted(cells)]


def check_fingerprint(relative, assert_baseline):
    digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    if assert_baseline and digest != SAMPLE_SHA256:
        raise CheckFailure("sample fingerprint changed: " + relative, {"sha256": digest})
    return {"file": relative, "sha256": digest,
            "matches_declared_baseline": digest == SAMPLE_SHA256,
            "baseline_asserted": assert_baseline}


def build_inventory(sheet):
    rows = sheet["rows"]
    non_empty_rows = sorted(rows)
    inventory = {
        "sheet_name": sheet["sheet_name"],
        "part": sheet["part"],
        "non_empty_rows": non_empty_rows,
        "cells_per_row": {str(number): len(rows[number]) for number in non_empty_rows},
        "merges": sheet["merges"],
        "protected_ranges": sheet["protected_ranges"],
    }
    return inventory


def check_regions(sheet, region1, region2):
    problems = []
    header_rows = region1["header_rows"]
    for region in (1, 2):
        if region not in header_rows:
            problems.append("区域 %d 未声明表头行" % region)
        elif header_rows[region] not in sheet["rows"]:
            problems.append("区域 %d 声明的表头行 %d 在工作表中不存在" % (region, header_rows[region]))
    if problems:
        raise CheckFailure("；".join(problems), {"problems": problems})
    declared_rows = [header_rows[1], header_rows[2]]
    undeclared = [number for number in sorted(sheet["rows"]) if number not in declared_rows]
    if undeclared:
        raise CheckFailure(
            "工作表出现未声明的非空行：%s。数据行或新表头区域出现时必须先更新 D1-A 盘点文档。"
            % undeclared, {"undeclared_rows": undeclared})

    discovered = {}
    for name, region, row in (("区域 1", region1, header_rows[1]), ("区域 2", region2, header_rows[2])):
        cells = region_of(sheet, row, name, name)
        discovered[name] = cells
        declared_letters = [item["letter"] for item in region["rows"]]
        actual_letters = [item["letter"] for item in cells]
        if declared_letters != actual_letters:
            problems.append("%s 列集合不一致：文档 %s / 工作表 %s"
                            % (name, declared_letters, actual_letters))
        declared_keys = [item["key"] for item in region["rows"]]
        actual_keys = [item["key"] for item in cells]
        if declared_keys != actual_keys:
            mismatch = [(d, a) for d, a in zip(declared_keys, actual_keys) if d != a]
            problems.append("%s 标题规范化键不一致：%s" % (name, mismatch[:8]))
    if problems:
        raise CheckFailure("；".join(problems), {"problems": problems})
    return discovered


def check_region1_dispositions(region1, facts):
    problems = []
    seen = {}
    for row in region1["rows"]:
        if row["disposition"] not in DISPOSITIONS:
            problems.append("%s 处置非法：%s" % (row["letter"], row["disposition"]))
            continue
        target = row["target"]
        if row["disposition"] == "PersonField":
            if target not in facts["specs"]:
                problems.append("%s 目标不是 canonical PersonFieldId：%s" % (row["letter"], target))
                continue
            spec = facts["specs"][target]
            if not spec["source_importable"] or spec["system_managed"]:
                problems.append("%s 目标不可由源表导入：%s" % (row["letter"], target))
            if target not in facts["import_targets"]:
                problems.append("%s 目标没有 ImportFieldId 映射：%s" % (row["letter"], target))
            if target == "LifeStatus" and "status_source_confirmed" not in row["note"]:
                problems.append("%s 状态源缺少 status_source_confirmed 标记" % row["letter"])
            seen.setdefault(target, []).append(row["letter"])
        elif target != "-":
            problems.append("%s 处置 %s 必须使用目标 '-'" % (row["letter"], row["disposition"]))
    for target, letters in sorted(seen.items()):
        if len(letters) > 1:
            problems.append("候选目标重复：%s -> %s" % (target, letters))
    if problems:
        raise CheckFailure("；".join(problems), {"problems": problems})
    return {"rows": len(region1["rows"]),
            "person_field_candidates": sum(1 for row in region1["rows"] if row["disposition"] == "PersonField"),
            "batch_raw_only_candidates": sum(1 for row in region1["rows"] if row["disposition"] == "BatchRawOnly"),
            "unsupported": sum(1 for row in region1["rows"] if row["disposition"] == "Unsupported")}


def check_region2_dispositions(region2, facts):
    problems = []
    seen = {}
    for row in region2["rows"]:
        target = row["target"]
        if target not in facts["specs"]:
            problems.append("%s 目标不是 canonical PersonFieldId：%s" % (row["letter"], target))
            continue
        spec = facts["specs"][target]
        if not spec["source_importable"] or spec["system_managed"]:
            problems.append("%s 目标不可由源表导入：%s" % (row["letter"], target))
        if target not in facts["import_targets"]:
            problems.append("%s 目标没有 ImportFieldId 映射：%s" % (row["letter"], target))
        seen.setdefault(target, []).append(row["letter"])
    for target, letters in sorted(seen.items()):
        if len(letters) > 1:
            problems.append("候选目标重复：%s -> %s" % (target, letters))
    if problems:
        raise CheckFailure("；".join(problems), {"problems": problems})
    return {"rows": len(region2["rows"]), "mapped_person_fields": len(seen)}


def check_declarations(region1, region2, cells1, cells2):
    problems = []
    groups = {}
    for cell in cells1:
        groups.setdefault(cell["key"], []).append(cell["letter"])
    exact = sorted(key for key, letters in groups.items() if len(letters) > 1)
    keys2 = {cell["key"] for cell in cells2}
    shared = sorted({cell["key"] for cell in cells1} & keys2)
    declared = region1["declared_keys"]
    if set(declared.get("区域 1 精确重复键", [])) != set(exact):
        problems.append("区域 1 精确重复键声明不一致：文档 %s / 实际 %s"
                        % (declared.get("区域 1 精确重复键"), exact))
    if set(declared.get("跨区域精确同名键", [])) != set(shared):
        problems.append("跨区域精确同名键声明不一致：文档 %s / 实际 %s"
                        % (declared.get("跨区域精确同名键"), shared))
    if problems:
        raise CheckFailure("；".join(problems), {"problems": problems})
    return {"region1_exact_duplicate_keys": exact, "cross_region_shared_keys": shared,
            "duplicate_groups": {key: letters for key, letters in sorted(groups.items()) if len(letters) > 1}}


def check_declared_inputs(region1, sample, sheet):
    """The declared sample path, worksheet name and dimension must match the real input."""
    problems = []
    if region1["declared_sample"] != sample:
        problems.append("声明样表路径与实际输入不一致：文档 %s / 实际 %s"
                        % (region1["declared_sample"], sample))
    if region1["declared_sheet"] is None:
        problems.append("未声明工作表名与维度")
    else:
        name, dimension = region1["declared_sheet"]
        if name != sheet["sheet_name"]:
            problems.append("声明工作表名不一致：文档 %s / 实际 %s" % (name, sheet["sheet_name"]))
        if dimension != sheet["dimension"]:
            problems.append("声明维度不一致：文档 %s / 实际 %s" % (dimension, sheet["dimension"]))
    if problems:
        raise CheckFailure("；".join(problems), {"problems": problems})
    return {"sample": sample, "sheet_name": sheet["sheet_name"], "dimension": sheet["dimension"]}


def check_cross_region_targets(region1, region2, shared_keys):
    """A key present in both regions is the only independent check of a target's meaning.

    Region-1 columns without a same-named region-2 column have no independent source for
    their semantic target; that judgement stays a human review item.
    """
    problems = []
    map1 = {row["key"]: row["target"] for row in region1["rows"]
            if row["disposition"] == "PersonField"}
    map2 = {row["key"]: row["target"] for row in region2["rows"]}
    compared = []
    for key in shared_keys:
        if key in map1 and key in map2:
            compared.append(key)
            if map1[key] != map2[key]:
                problems.append("同名键目标不一致：%s -> 区域 1 %s / 区域 2 %s"
                                % (key, map1[key], map2[key]))
    if not compared:
        problems.append("没有任何同名键可比较，跨区域目标一致性检查失效")
    if problems:
        raise CheckFailure("；".join(problems), {"problems": problems})
    return {"compared_keys": compared,
            "uncompared_region1_keys": sorted(set(map1) - set(compared))}


def render(sections):
    lines = []
    for title, body in sections:
        lines.append("")
        lines.append("== " + title + " ==")
        lines.extend(body)
    return "\n".join(lines).lstrip("\n") + "\n"


def write_text(path, text):
    """UTF-8 with LF endings, independent of the host line separator."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="repository root; defaults to the tree containing this script")
    parser.add_argument("--sample", help="sample workbook path relative to root; overrides " + SAMPLE)
    parser.add_argument("--output", help="directory for results.json; defaults to <root>/build/d1a")
    parser.add_argument("--evidence-dir", help="also write the UTF-8 evidence report into this directory")
    args = parser.parse_args()

    global ROOT
    if args.root:
        ROOT = Path(args.root).resolve()
    if args.evidence_dir and args.sample:
        # Tracked L0 evidence must always describe the declared sample.
        parser.error("--evidence-dir 不能与 --sample 同时使用：受版本控制的证据只能来自已声明样表")
    sample = args.sample or SAMPLE
    output = Path(args.output) if args.output else ROOT / "build" / "d1a"
    output.mkdir(parents=True, exist_ok=True)

    # The frozen baseline fingerprint is only asserted for the declared sample path;
    # an alternate sample is recorded by digest so a mutation cannot pass silently.
    fingerprint = check_fingerprint(sample, assert_baseline=args.sample is None)
    sheets = load_sample(sample)
    if len(sheets) != 1:
        raise CheckFailure("expected exactly one worksheet in the public sample",
                           {"sheets": [sheet["sheet_name"] for sheet in sheets]})
    sheet = sheets[0]
    inventory = build_inventory(sheet)
    facts = contract_facts()
    region1 = parse_region1(read_text(REGION1_DOC))
    region2 = parse_region2(read_text(REGION2_DOC), region1["header_rows"].get(2))
    header1, header2 = region1["header_rows"].get(1), region1["header_rows"].get(2)
    discovered = check_regions(sheet, region1, region2)
    cells1, cells2 = discovered["区域 1"], discovered["区域 2"]
    region1_stats = check_region1_dispositions(region1, facts)
    region2_stats = check_region2_dispositions(region2, facts)
    declared_inputs = check_declared_inputs(region1, sample, sheet)
    declarations = check_declarations(region1, region2, cells1, cells2)
    cross_region = check_cross_region_targets(region1, region2,
                                              declarations["cross_region_shared_keys"])

    region1_rows = {row["letter"]: row for row in region1["rows"]}
    region2_rows = {row["letter"]: row for row in region2["rows"]}

    def region_table(cells, rows, with_member):
        body = []
        header = "  列  索引  原文/标题                            规范化键            处置           目标"
        body.append(header)
        for cell in cells:
            row = rows[cell["letter"]]
            body.append("  %-3s %-5d %-36s %-20s %-14s %s" % (
                cell["letter"], cell["index"], repr(cell["raw"])[:36], cell["key"][:20],
                row["disposition"], row["target"]))
            if with_member:
                body.append("      持久化成员: " + row["member"])
        return body

    header_only = len(inventory["non_empty_rows"]) == len({header1, header2})
    sections = [
        ("输入身份", [
            "文件: " + sample,
            "SHA-256: " + fingerprint["sha256"],
            "与 docs/baseline/00 基线指纹一致: %s" % ("是" if fingerprint["matches_declared_baseline"] else "否"),
            "工作表: %s (%s)" % (sheet["sheet_name"], sheet["part"]),
            "含非空单元格的行: %s" % inventory["non_empty_rows"],
            "每行非空单元格数: %s" % inventory["cells_per_row"],
            "合并单元格: %s" % (inventory["merges"] or "无"),
            "受保护区域: %s" % (inventory["protected_ranges"] or "无"),
        ]),
        ("表头区域", [
            "区域 1（工作/质检表头）: 表头行 %d，非空标题 %d 个" % (header1, len(region1["rows"])),
            "区域 2（人事/名册表头）: 表头行 %d，非空标题 %d 个" % (header2, len(region2["rows"])),
            "数据行: %d 行 -> %s" % (len(inventory["non_empty_rows"]) - len({header1, header2}),
                                    "HEADER_ONLY_SAMPLE" if header_only else "存在数据行"),
            "重复率、日期分布、脏数据比例、枚举实际值域: 未测量（无数据行，不得推断）",
        ]),
        ("区域 1 逐列盘点与候选处置（候选，未确认）", region_table(cells1, region1_rows, False)),
        ("区域 2 逐列盘点与候选映射（既有候选文档）", region_table(cells2, region2_rows, True)),
        ("覆盖与冲突检查", [
            "区域 1 处置统计: PersonField 候选 %d / BatchRawOnly 候选 %d / Unsupported %d"
            % (region1_stats["person_field_candidates"], region1_stats["batch_raw_only_candidates"],
               region1_stats["unsupported"]),
            "区域 2 映射字段数: %d" % region2_stats["mapped_person_fields"],
            "区域 1 精确重复键: %s" % "、".join(declarations["region1_exact_duplicate_keys"]),
            "跨区域精确同名键: %s" % "、".join(declarations["cross_region_shared_keys"]),
            "跨区域目标一致性: 已比较 %d 个同名键 -> %s"
            % (len(cross_region["compared_keys"]), "、".join(cross_region["compared_keys"])),
            "无同名键可独立校验的区域 1 源键（语义判断留人工复核）: %s"
            % ("、".join(cross_region["uncompared_region1_keys"]) or "无"),
        ]),
    ]
    for key, letters in sorted(declarations["duplicate_groups"].items()):
        sections[-1][1].append("  重复组 %s: %s" % (key, "、".join(letters)))

    report = render(sections)
    results = {
        "scope": "D1-A source header inventory and mapping coverage",
        "sample": fingerprint,
        "inventory": inventory,
        "regions": {
            "region1": {"doc": REGION1_DOC, "header_row": header1,
                        "columns": len(region1["rows"]), "stats": region1_stats},
            "region2": {"doc": REGION2_DOC, "header_row": header2,
                        "columns": len(region2["rows"]), "stats": region2_stats},
        },
        "declarations": declarations,
        "declared_inputs": declared_inputs,
        "cross_region_targets": cross_region,
        "header_only_sample": header_only,
        "rule_engine_executed": False,
        "business_rule_frozen": False,
    }
    write_text(output / "results.json", json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    if args.evidence_dir:
        evidence = ROOT / args.evidence_dir
        evidence.mkdir(parents=True, exist_ok=True)
        write_text(evidence / "01-source-header-inventory.txt", report)
    # Printed without an extra newline so that stdout equals the evidence file byte for byte.
    print(report, end="")
    print("results.json -> " + str(output / "results.json"))
    return 0


if __name__ == "__main__":
    # Evidence must be identical regardless of the host console code page.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    try:
        sys.exit(main())
    except CheckFailure as failure:
        print("FAIL " + str(failure))
        print(json.dumps(failure.details, ensure_ascii=False, indent=2))
        sys.exit(1)
