"""Exercise the checker CLI on isolated Git histories, never the product repository."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run(command, cwd, expected=0, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                            encoding="utf-8", errors="replace")
    if result.returncode != expected:
        raise RuntimeError(str(command) + " returned " + str(result.returncode) + ": " + result.stdout + result.stderr)
    return result.stdout.strip()


def main():
    output = ROOT / "build/gate0"
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="diff-regression-", dir=output) as directory:
        fixture = Path(directory)
        assert fixture.resolve().is_relative_to(output.resolve())
        tool = fixture / "tools/gate0/check_contract.py"
        tool.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "tools/gate0/check_contract.py", tool)
        run(["git", "init", "-q", "-b", "test/diff-check"], fixture)
        run(["git", "config", "user.name", "Contract test"], fixture)
        run(["git", "config", "user.email", "contract-test@example.invalid"], fixture)
        (fixture / ".gitignore").write_text("build/\n", encoding="utf-8")
        sample = fixture / "sample.txt"
        sample.write_text("baseline\n", encoding="utf-8")
        run(["git", "add", "."], fixture)
        run(["git", "commit", "-q", "-m", "test: 建立Diff基线"], fixture)
        base = run(["git", "rev-parse", "HEAD"], fixture)
        sample.write_text("committed trailing space \n", encoding="utf-8")
        run(["git", "add", "sample.txt"], fixture)
        run(["git", "commit", "-q", "-m", "test: 加入空白缺陷样例"], fixture)
        head = run(["git", "rev-parse", "HEAD"], fixture)
        assert not run(["git", "status", "--porcelain"], fixture)
        run([sys.executable, str(tool), "--layer", "diff", "--base-ref", base], fixture, expected=1)
        failed = json.loads((fixture / "build/gate0/results.json").read_text(encoding="utf-8"))
        check = failed["checks"][0]
        assert not check["passed"]
        assert check["details"]["base_sha"] == base and check["details"]["head_sha"] == head
        assert check["details"]["commands"][0]["exit_code"] != 0
        assert "trailing whitespace" in check["details"]["commands"][0]["stdout"]
        sample.write_text("fixed content\n", encoding="utf-8")
        run(["git", "add", "sample.txt"], fixture)
        run(["git", "commit", "-q", "-m", "test: 修复空白缺陷样例"], fixture)
        run([sys.executable, str(tool), "--layer", "diff", "--base-ref", base], fixture)
        passed = json.loads((fixture / "build/gate0/results.json").read_text(encoding="utf-8"))
        assert passed["checks"][0]["passed"]
        # An unknown base must fail rather than produce a vacuous clean PASS.
        run([sys.executable, str(tool), "--layer", "diff", "--base-ref", "missing-ref"], fixture, expected=1)
        env = dict(os.environ, ROSTER_BASE_REF=base)
        run([sys.executable, str(tool), "--layer", "diff"], fixture, env=env)
        # A discoverable but unexecutable compiler must not affect the Python diff layer.
        poison_bin = fixture / "poison-bin"
        poison_bin.mkdir()
        poison_compiler = poison_bin / ("g++.exe" if sys.platform == "win32" else "g++")
        poison_compiler.write_bytes(b"this is deliberately not an executable\n")
        if sys.platform != "win32":
            poison_compiler.chmod(0o755)
        poison_env = dict(env, PATH=str(poison_bin) + os.pathsep + os.environ.get("PATH", ""))
        assert Path(shutil.which("g++", path=poison_env["PATH"])).resolve() == poison_compiler.resolve()
        run([sys.executable, str(tool), "--layer", "diff"], fixture, env=poison_env)
        python_only = json.loads((fixture / "build/gate0/results.json").read_text(encoding="utf-8"))
        assert python_only["tools"]["compiler"]["status"] == "not_executed"
    print("PASS committed PR whitespace, clean diff, invalid base, base override, and no compiler invocation")


if __name__ == "__main__":
    main()
