"""Isolated regression checks for tools/d1a/inventory_d1a.py.

The checks build a temporary tree containing copies of the public sample workbook,
the D1-A mapping documents and the contract header, mutate one input per case, and
prove that the D1-A checker fails on drift and passes on the declared baseline.
No repository file is modified and no network access is used.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "d1a" / "inventory_d1a.py"
SAMPLE = "reference/员工信息表11111.xlsx"
REGION1_DOC = "docs/baseline/07_源表字段映射.md"
REGION2_DOC = "docs/baseline/02_字段映射与数据保留策略.md"
CONTRACT = "include/retiree_roster/schema_types.hpp"
SHEET_PART = "xl/worksheets/sheet1.xml"
SHARED_PART = "xl/sharedStrings.xml"
EVIDENCE_INVENTORY = "docs/evidence/D1-A/01-source-header-inventory.txt"
EVIDENCE_REGRESSION = "docs/evidence/D1-A/02-checker-regression.txt"


def build_tree(destination):
    for name in (SAMPLE, REGION1_DOC, REGION2_DOC, CONTRACT):
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return destination


def run_tool(tree, sample_override=False, output=None, evidence_dir=None):
    command = [sys.executable, str(TOOL), "--root", str(tree)]
    if sample_override:
        command += ["--sample", SAMPLE]
    if output:
        command += ["--output", str(output)]
    if evidence_dir:
        command += ["--evidence-dir", evidence_dir]
    environment = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(command, cwd=ROOT, capture_output=True, encoding="utf-8",
                          errors="replace", env=environment)


def edit_zip(path, edits):
    original = path.read_bytes()
    with ZipFile(path) as source, ZipFile(path.with_suffix(".tmp"), "w", ZIP_DEFLATED) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename in edits:
                data = edits[item.filename](data)
            target.writestr(item, data)
    assert path.read_bytes() == original
    path.with_suffix(".tmp").replace(path)


def add_data_row(data):
    text = data.decode("utf-8")
    row = '<row r="2"><c r="A2" t="s"><v>0</v></c></row>'
    assert "</sheetData>" in text
    return text.replace("</sheetData>", row + "</sheetData>").encode("utf-8")


def rename_header(old, new):
    def apply(data):
        text = data.decode("utf-8")
        assert ">" + old + "<" in text, "shared string not found: " + old
        return text.replace(">" + old + "<", ">" + new + "<").encode("utf-8")
    return apply


def replace_in_doc(relative, old, new):
    def apply(tree):
        path = tree / relative
        text = path.read_text(encoding="utf-8")
        assert old in text, "pattern not found in %s: %s" % (relative, old)
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    return apply


def expect_failure(name, tree, needle, log, sample_override=False):
    result = run_tool(tree, sample_override=sample_override)
    if result.returncode == 0:
        raise AssertionError("%s: checker passed but failure was expected" % name)
    combined = result.stdout + result.stderr
    if needle not in combined:
        raise AssertionError("%s: expected %r in output, got: %s" % (name, needle, combined[:400]))
    record = "PASS %s -> %s" % (name, needle)
    print(record)
    log.append(record)


def check_committed_evidence(workspace, log):
    """The tracked L0 evidence must equal freshly regenerated output."""
    committed_inventory = (ROOT / EVIDENCE_INVENTORY).read_text(encoding="utf-8")
    result = run_tool(ROOT, output=workspace / "evidence-refresh")
    if result.returncode != 0:
        raise AssertionError("refreshing the inventory against the real tree failed: " + result.stdout)
    regenerated = result.stdout.split("results.json -> ")[0]
    if regenerated != committed_inventory:
        raise AssertionError("%s is stale or hand-edited; refresh with "
                             "python tests/contract/check_d1a_regressions.py --update-evidence"
                             % EVIDENCE_INVENTORY)
    record = "PASS committed_inventory_matches -> " + EVIDENCE_INVENTORY
    print(record)
    log.append(record)

    # The log's own last line is part of the expected content, so it is appended here.
    final = "PASS committed_regression_log_matches -> " + EVIDENCE_REGRESSION
    committed_log = (ROOT / EVIDENCE_REGRESSION).read_text(encoding="utf-8")
    expected_log = "\n".join(log + [final]) + "\n"
    if committed_log != expected_log:
        raise AssertionError("%s is stale; refresh with "
                             "python tests/contract/check_d1a_regressions.py --update-evidence"
                             % EVIDENCE_REGRESSION)
    print(final)
    log.append(final)


def write_log(relative, log):
    if not relative:
        return
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(log) + "\n")


def refresh_evidence(workspace):
    """Regenerate both tracked L0 evidence files from the current tree."""
    result = run_tool(ROOT, output=workspace / "evidence-refresh",
                      evidence_dir="docs/evidence/D1-A")
    if result.returncode != 0:
        raise AssertionError("inventory refresh failed: " + result.stdout + result.stderr)
    print("refreshed " + EVIDENCE_INVENTORY)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", help="also write the UTF-8 (LF) regression log to this path")
    parser.add_argument("--update-evidence", action="store_true",
                        help="regenerate the tracked L0 evidence instead of verifying it")
    args = parser.parse_args()
    log = []
    workspace = Path(tempfile.mkdtemp(prefix="d1a-regression-"))
    try:
        baseline = build_tree(workspace / "baseline")
        result = run_tool(baseline)
        if result.returncode != 0:
            raise AssertionError("baseline tree must pass: " + result.stdout + result.stderr)
        print("PASS baseline_tree -> exit 0")
        log.append("PASS baseline_tree -> exit 0")

        case = build_tree(workspace / "data_row")
        edit_zip(case / SAMPLE, {SHEET_PART: add_data_row})
        expect_failure("undeclared_data_row", case, "未声明的非空行", log, sample_override=True)

        case = build_tree(workspace / "renamed_header")
        edit_zip(case / SAMPLE, {SHARED_PART: rename_header("备注", "备注X")})
        expect_failure("renamed_header", case, "标题规范化键不一致", log, sample_override=True)

        case = build_tree(workspace / "duplicate_target")
        replace_in_doc(REGION1_DOC, "| AT | 现学历 | 现学历 | PersonField | Education |",
                       "| AT | 现学历 | 现学历 | PersonField | ProfessionalTitle |")(case)
        expect_failure("duplicate_person_target", case, "候选目标重复", log)

        case = build_tree(workspace / "raw_only_target")
        replace_in_doc(REGION1_DOC, "| K | 分区 | 分区 | BatchRawOnly | - |",
                       "| K | 分区 | 分区 | BatchRawOnly | FullName |")(case)
        expect_failure("batch_raw_only_target", case, "必须使用目标", log)

        case = build_tree(workspace / "collision_declaration")
        replace_in_doc(REGION1_DOC, "区域 1 精确重复键：其他联系、姓名、性别、政治面貌、民族、身份证号",
                       "区域 1 精确重复键：其他联系、姓名、性别、政治面貌、民族")(case)
        expect_failure("collision_declaration", case, "精确重复键声明不一致", log)

        case = build_tree(workspace / "status_marker")
        replace_in_doc(REGION1_DOC, "必须 status_source_confirmed 显式确认", "必须显式确认")(case)
        expect_failure("status_source_marker", case, "status_source_confirmed", log)

        case = build_tree(workspace / "unimportable_target")
        replace_in_doc(REGION1_DOC, "| AH | 备注 | 备注 | PersonField | Remark |",
                       "| AH | 备注 | 备注 | PersonField | PinyinSortKey |")(case)
        expect_failure("unimportable_target", case, "目标不可由源表导入", log)

        case = build_tree(workspace / "header_row_declaration")
        replace_in_doc(REGION1_DOC, "区域 1 表头行（1 起算）：1", "区域 1 表头行（1 起算）：2")(case)
        expect_failure("header_row_declaration", case, "声明的表头行", log)

        case = build_tree(workspace / "cross_region_target")
        replace_in_doc(REGION1_DOC, "| AA | 职称 | 职称 | PersonField | ProfessionalTitle |",
                       "| AA | 职称 | 职称 | PersonField | Degree |")(case)
        expect_failure("cross_region_target_mismatch", case, "同名键目标不一致", log)

        case = build_tree(workspace / "declared_sheet")
        replace_in_doc(REGION1_DOC, "工作表：`Sheet1`，维度 `A1:IS3`",
                       "工作表：`Sheet9`，维度 `A1:IS3`")(case)
        expect_failure("declared_sheet_mismatch", case, "声明工作表名不一致", log)

        case = build_tree(workspace / "declared_sample")
        replace_in_doc(REGION1_DOC, "样表：`reference/员工信息表11111.xlsx`",
                       "样表：`reference/another.xlsx`")(case)
        expect_failure("declared_sample_mismatch", case, "声明样表路径与实际输入不一致", log)

        print("all D1-A regression checks passed")
        log.append("all D1-A regression checks passed")

        if args.update_evidence:
            refresh_evidence(workspace)
            log.append("PASS committed_inventory_matches -> " + EVIDENCE_INVENTORY)
            log.append("PASS committed_regression_log_matches -> " + EVIDENCE_REGRESSION)
            write_log(args.log, log)
            print("evidence refreshed; re-run without --update-evidence to verify")
            return 0

        check_committed_evidence(workspace, log)
        write_log(args.log, log)
        return 0
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
