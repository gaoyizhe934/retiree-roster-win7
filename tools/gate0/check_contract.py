"""Reproducible, offline checks of the Gate 0 draft contract (not the product)."""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "build" / "gate0"
BASELINES = {
    "docs/退休人员名册打印小程序需求说明.docx": "658b10952e2cba734990d2b37f862b2495196e51427c117cf2a4edde7992c641",
    "docs/退休人员名册打印小程序开发规划.docx": "c1caac2094c6778363b27af2011af3cd0118fa4e96e570761479247748d347c1",
    "reference/七阶段开发任务清单.xlsx": "7648e936d249f817bc61d43bcf109eafc94802b9a1dfd370fd23cdb45d802e26",
    "reference/员工信息表11111.xlsx": "427727f5d8062e7cba699b35d9262fb594b717d3dd699f811cbb7475112cf5b6",
}
RESULTS = []


class CheckFailure(RuntimeError):
    def __init__(self, message, details):
        super().__init__(message)
        self.details = details


def documentation_paths():
    paths = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "GitHub协作命名规范.md"]
    for folder in ("docs/baseline", "docs/decisions", "docs/status", "docs/dependencies", "tools/gate0"):
        paths.extend(sorted((ROOT / folder).glob("*.md")))
    return paths


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    # Limit the ownership exception to this process and the known workspace.
    return subprocess.run(
        ["git", "-c", "safe.directory=" + ROOT.as_posix(), *args],
        cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace",
    )


def baseline_fingerprints():
    for name, expected in BASELINES.items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        require(actual == expected, "baseline fingerprint changed: " + name)
    return {"files": len(BASELINES)}


def source_mapping():
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(ROOT / "reference/员工信息表11111.xlsx") as archive:
        shared = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        strings = ["".join(si.itertext()) for si in shared.findall("s:si", ns)]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    headers = {}
    for cell in sheet.findall("s:sheetData/s:row[@r='3']/s:c", ns):
        value = cell.find("s:v", ns)
        if cell.get("t") == "s" and value is not None:
            title = strings[int(value.text)].strip()
        elif cell.get("t") == "inlineStr":
            title = "".join(cell.find("s:is", ns).itertext()).strip()
        else:
            title = (value.text or "").strip() if value is not None else ""
        if title:
            headers[re.sub(r"\d+$", "", cell.get("r"))] = title
    table = (ROOT / "docs/baseline/02_字段映射与数据保留策略.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| ([A-Z]+) \| (.*?) \| (\w+) \| (\w+) \|$", table, re.M)
    require(len(rows) == 23 and len(headers) == 23, "expected 23 source mappings")
    require({col: title for col, title, _, _ in rows} == headers, "source mapping differs from workbook")
    header = (ROOT / "include/retiree_roster/schema_types.hpp").read_text(encoding="utf-8")
    person = re.search(r"struct PersonRecord \{(.*?)\n\};", header, re.S).group(1)
    for _, _, field_id, member in rows:
        require("{FieldId::" + field_id + "," in header, "missing field spec: " + field_id)
        require(re.search(r"\b" + member + r"\s*;", person), "missing stored member: " + member)
    require(len({row[2] for row in rows}) == 23, "ambiguous target mapping")
    return {"source_columns": 23, "mapped_person_fields": 23, "blank_column": "W", "remark_column": "X"}


def boundary_fixture():
    with (ROOT / "tests/contract/chongyang_cases.csv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    # Independently enumerated R02 expectations, including the 90+ boundary.
    expected = {
        "age_69": (1957, "Living", "false"), "age_70": (1956, "Living", "true"),
        "age_71": (1955, "Living", "false"), "age_74": (1952, "Living", "false"),
        "age_75": (1951, "Living", "true"), "age_79": (1947, "Living", "false"),
        "age_80": (1946, "Living", "true"), "age_84": (1942, "Living", "false"),
        "age_85": (1941, "Living", "true"), "age_89": (1937, "Living", "false"),
        "age_90": (1936, "Living", "true"), "age_91": (1935, "Living", "true"),
        "deceased_90": (1936, "Deceased", "false"),
    }
    actual = {r["case_id"]: (int(r["birth_year"]), r["life_status"], r["expected_selected"]) for r in rows}
    require(len(rows) == 13 and actual == expected, "R02 acceptance fixture is incomplete")
    require(all(r["target_year"] == "2026" for r in rows), "fixture reference year changed")
    return {"cases": 13, "rule_engine_executed": False}


def compile_and_run(source_name):
    compiler = shutil.which("g++")
    require(compiler is not None, "g++ not available")
    executable = "build/gate0/" + Path(source_name).stem + (".exe" if sys.platform == "win32" else "")
    command = [compiler, "-std=c++14", "-Wall", "-Wextra", "-pedantic-errors",
               "-I", "include", source_name, "-o", executable]
    compiled = subprocess.run(command, cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
    require(compiled.returncode == 0, "compilation failed: " + compiled.stderr)
    ran = subprocess.run([str(ROOT / executable)], cwd=ROOT, capture_output=True,
                         encoding="utf-8", errors="replace")
    require(ran.returncode == 0, "test failed: " + str(ran.returncode) + " " + ran.stderr)
    return {"command": command, "compile_exit": compiled.returncode, "test_exit": ran.returncode}


def obsolete_api_rejected():
    compiler = shutil.which("g++")
    require(compiler is not None, "g++ not available")
    snippets = {
        "export_refilter": "ExportRosterRequest r; r.filter = FilterSpec{};",
        "person_care": "PersonRecord p; p.care.has_financial_difficulty = true;",
        "tag_as_person_field": "auto f = FieldId::TagCodes; (void)f;",
        "mutable_print_roster": "PrintModel m; m.roster->rows.clear();",
        "confirm_status_change": "ConfirmImportRequest r; r.status_resolution = ImportStatusResolution{};",
        "confirm_mapping_change": "ConfirmImportRequest r; r.mapping_version = 2;",
        "create_system_id": "CreatePersonRequest r; r.person.person_id = \"forged\";",
        "create_fixed_code": "CreatePersonRequest r; r.person.person_code = \"forged\";",
        "create_audit": "CreatePersonRequest r; r.person.audit.created_at = \"forged\";",
        "edit_system_id": "FieldChange c; c.field = EditableFieldId::PersonId;",
        "tag_audit_time": "UpdateTagRequest r; r.mutation.updated_at = \"forged\";",
        "tag_audit_operator": "UpdateTagRequest r; r.mutation.updated_by = \"forged\";",
        "caller_freezes_profile": "ImportProfile p; p.frozen = true;",
        "ambiguous_schema_version": "ApiMeta m; m.schema_version = 3;",
    }
    for field in ("PersonId", "PersonCode", "CreatedAt", "UpdatedAt", "ImportBatchId", "LastModifiedBy", "PinyinSortKey"):
        snippets["import_protected_" + field] = "ImportColumnBinding b; b.target_field = ImportFieldId::" + field + ";"
    control = OUTPUT / "syntax_control.cpp"
    control.write_text('#include "retiree_roster/schema_types.hpp"\nint main() { return 0; }\n', encoding="utf-8")
    syntax_command = [compiler, "-std=c++14", "-pedantic-errors", "-I", "include", "-fsyntax-only"]
    control_command = syntax_command + ["build/gate0/" + control.name]
    control_result = subprocess.run(control_command, cwd=ROOT, capture_output=True,
                                    encoding="utf-8", errors="replace")
    require(control_result.returncode == 0, "syntax-mode control failed: " + control_result.stderr)
    diagnostics = []
    for name, snippet in snippets.items():
        code = '#include "retiree_roster/schema_types.hpp"\nusing namespace retiree_roster::schema;\nint main(){' + snippet + '}\n'
        source = OUTPUT / (name + ".cpp")
        source.write_text(code, encoding="utf-8")
        command = syntax_command + ["build/gate0/" + source.name]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
        require(result.returncode == 1 and "error:" in result.stderr,
                "expected compiler rejection, got tool failure or success: " + name + " " + result.stderr)
        diagnostics.append({"name": name, "command": command, "exit_code": result.returncode,
                            "diagnostics": result.stderr})
    return {"control_command": control_command, "control_exit": control_result.returncode,
            "rejected_consumers": diagnostics}


def ignore_and_attributes():
    ignored = [".vs/state", ".xmake/state", "build/gate0/result", "dist/app.exe", "out/temp",
               "data/roster.db", "data/archive/private.xlsx", "backups/nested/data.zip",
               "exports/roster.xlsx", "logs/session.log", "private.sqlite-wal", "~$input.xlsx"]
    for name in ignored:
        require(git("check-ignore", "-q", "--no-index", name).returncode == 0, "not ignored: " + name)
    public = ["CMakeLists.txt", "xmake.lua", "templates/default.json", "data/.gitkeep",
              "tests/contract/chongyang_cases.csv", "reference/员工信息表11111.xlsx"]
    for name in public:
        require(git("check-ignore", "-q", "--no-index", name).returncode == 1, "wrongly ignored: " + name)
    attrs = git("check-attr", "text", "eol", "--", "README.md", "include/retiree_roster/schema_types.hpp",
                "reference/员工信息表11111.xlsx", "docs/退休人员名册打印小程序需求说明.docx")
    require(attrs.returncode == 0, "git check-attr failed")
    require(attrs.stdout.count("text: unset") == 2, "Word/Excel must be binary")
    require(attrs.stdout.count("eol: lf") == 2, "Markdown/C++ must use LF")
    return {"ignored_probes": len(ignored), "public_probes": len(public), "attributes": "verified"}


def documentation_links():
    paths = documentation_paths()
    count = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "#")):
                continue
            relative = unquote(target.split("#", 1)[0].strip("<>"))
            require((path.parent / relative).is_file(), "missing link in " + path.name + ": " + relative)
            count += 1
    return {"files": len(paths), "local_links": count}


def diff_whitespace(base_ref=None):
    base_ref = base_ref or os.environ.get("ROSTER_BASE_REF", "origin/main")
    base = git("rev-parse", "--verify", "--end-of-options", base_ref + "^{commit}")
    require(base.returncode == 0, "cannot resolve base ref: " + base_ref)
    head = git("rev-parse", "--verify", "HEAD^{commit}")
    require(head.returncode == 0, "cannot resolve HEAD")
    base_sha, head_sha = base.stdout.strip(), head.stdout.strip()
    merge = git("merge-base", base_sha, head_sha)
    require(merge.returncode == 0, "base and HEAD have no merge base")
    merge_sha = merge.stdout.strip()
    details = {"base_ref": base_ref, "base_sha": base_sha, "head_sha": head_sha,
               "merge_base_sha": merge_sha, "commands": []}
    for kind, args in (
        ("committed_pr", ("diff", "--check", merge_sha + "..." + head_sha)),
        ("staged", ("diff", "--cached", "--check")),
        ("worktree", ("diff", "--check")),
    ):
        result = git(*args)
        details["commands"].append({"scope": kind, "command": ["git", *args],
                                    "exit_code": result.returncode,
                                    "stdout": result.stdout, "stderr": result.stderr})
    if any(c["exit_code"] != 0 for c in details["commands"]):
        raise CheckFailure("whitespace check failed; see commands and diagnostics", details)
    return details


def checker_regressions():
    command = [sys.executable, "tests/contract/check_tool_regressions.py"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
    require(result.returncode == 0, result.stdout + result.stderr)
    return {"command": command, "exit_code": result.returncode, "result": result.stdout}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layer", choices=("all", "structure", "cpp14", "diff"), default="all")
    parser.add_argument("--base-ref", help="PR base ref; defaults to ROSTER_BASE_REF or origin/main")
    args = parser.parse_args()
    RESULTS.clear()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    structure_checks = [
        ("baseline_fingerprints", baseline_fingerprints), ("23_column_mapping", source_mapping),
        ("R02_fixture_completeness", boundary_fixture),
        ("ignore_and_attributes", ignore_and_attributes), ("documentation_links", documentation_links),
        ("diff_whitespace", lambda: diff_whitespace(args.base_ref)),
        ("checker_regressions", checker_regressions),
    ]
    cpp14_checks = [
        ("date_value_behavior", lambda: compile_and_run("tests/contract/date_value_test.cpp")),
        ("cpp14_consumer", lambda: compile_and_run("tests/contract/consumer_contract_test.cpp")),
        ("preview_revision", lambda: compile_and_run("tests/contract/preview_revision_test.cpp")),
        ("input_authority", lambda: compile_and_run("tests/contract/input_authority_test.cpp")),
        ("obsolete_api_rejected", obsolete_api_rejected),
    ]
    if args.layer == "all":
        checks = structure_checks + cpp14_checks
    elif args.layer == "structure":
        checks = structure_checks
    elif args.layer == "cpp14":
        checks = cpp14_checks
    else:
        checks = [("diff_whitespace", lambda: diff_whitespace(args.base_ref))]
    for name, check in checks:
        try:
            details = check()
            RESULTS.append({"name": name, "passed": True, "details": details})
            print("PASS " + name)
        except Exception as error:
            entry = {"name": name, "passed": False, "error": str(error)}
            if isinstance(error, CheckFailure):
                entry["details"] = error.details
            RESULTS.append(entry)
            print("FAIL " + name + ": " + str(error))
    inputs = [ROOT / name for name in BASELINES]
    inputs.extend([ROOT / "include/retiree_roster/schema_types.hpp", Path(__file__)])
    inputs.extend(sorted((ROOT / "tests/contract").glob("*")))
    inputs.extend(documentation_paths())
    inputs.extend(ROOT / p for p in (".gitignore", ".gitattributes", ".github/pull_request_template.md"))
    compiler_information = {"status": "not_executed", "reason": "Python-only layer"}
    if args.layer in ("all", "cpp14"):
        compiler = shutil.which("g++")
        if compiler:
            try:
                version = subprocess.run([compiler, "--version"], cwd=ROOT, capture_output=True,
                                         encoding="utf-8", errors="replace")
                compiler_information = {"status": "executed", "command": [compiler, "--version"],
                                        "exit_code": version.returncode, "version": version.stdout,
                                        "diagnostics": version.stderr}
            except OSError as error:
                compiler_information = {"status": "unavailable", "error": str(error)}
        else:
            compiler_information = {"status": "unavailable", "reason": "g++ not on PATH"}
    evidence = {
        "scope": "Gate 0 draft contract checks only; no product/Win7/Gate approval",
        "layer": args.layer,
        "invocation": ["python", "tools/gate0/check_contract.py", *sys.argv[1:]],
        "unexecuted_layers": {
            "all": ["formal_msvc_cmake", "win7"],
            "structure": ["cpp14", "formal_msvc_cmake", "win7"],
            "cpp14": ["structure", "formal_msvc_cmake", "win7"],
            "diff": ["structure_except_diff", "cpp14", "formal_msvc_cmake", "win7"],
        }[args.layer],
        "tools": {"python_version": sys.version,
                  "compiler": compiler_information},
        "inputs": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in inputs if p.is_file()},
        "checks": RESULTS,
    }
    (OUTPUT / "results.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    passed = sum(item["passed"] for item in RESULTS)
    print(str(passed) + "/" + str(len(RESULTS)) + " checks passed; build/gate0/results.json")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
