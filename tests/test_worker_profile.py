import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPO_ROOT / "tools" / "check_worker_catalog.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_worker_catalog", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkerCatalogCheckerTests(unittest.TestCase):
    def test_worker_mode_exports_noninteractive_package_manager_environment(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        worker_mode = script.split("-worker | worker)", 1)[1].split(";;", 1)[0]

        self.assertIn("export F8X_NONINTERACTIVE=1", worker_mode)
        self.assertIn("export DEBIAN_FRONTEND=noninteractive", worker_mode)
        self.assertIn("export APT_LISTCHANGES_FRONTEND=none", worker_mode)
        self.assertIn("export NEEDRESTART_MODE=l", worker_mode)

    def test_worker_profile_installs_mihomo_for_supported_linux_architectures(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        installer = script.split("Worker_mihomo_Install(){", 1)[1].split(
            "Worker_SecLists_Install(){", 1
        )[0]

        self.assertIn("mihomo|mihomo|Worker_mihomo_Install|none|install|", script)
        self.assertIn('mihomo_Ver="v1.19.29"', script)
        self.assertIn('mihomo-linux-amd64-${mihomo_Ver}.gz', installer)
        self.assertIn('mihomo-linux-arm64-${mihomo_Ver}.gz', installer)
        self.assertIn("/usr/local/bin/mihomo", installer)

    def test_worker_profile_does_not_install_or_report_sliver(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        profile = script.split('F8X_WORKER_CAPABILITIES="', 1)[1].split('\n"', 1)[0]

        self.assertNotIn("sliver-client", profile)
        self.assertNotIn("sliver-server", profile)

    def test_enum4linux_ng_uses_isolated_system_python_environment(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        installer = script.split("Pentest_enum4linux_ng_Install(){", 1)[1].split(
            "# ===================== Install bloodyAD", 1
        )[0]

        self.assertIn('F8x_Worker_Pipx_Install "$dir"', installer)
        self.assertIn('Install_Switch "smbclient"', installer)
        self.assertNotIn("setup.py install", installer)
        self.assertNotIn("Install_Switch7", installer)
        self.assertNotIn("--break-system-packages", installer)
        self.assertNotIn("--python", installer)
        self.assertNotIn("--fetch-missing-python", installer)

    def test_worker_report_includes_failure_log_and_summary(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        report_code = script.split(
            'python3 - "$_f8x_worker_result_file" "$report" "$F8x_Version" <<\'PY\'\n', 1
        )[1].split("\nPY", 1)[0]

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            source = temporary_path / "results.tsv"
            destination = temporary_path / "report.json"
            source.write_text(
                "donpapi\tfailed\tinstallation failed\t"
                "/tmp/f8x-worker-logs/donpapi.log\tError installing donpapi.\n",
                encoding="utf-8",
            )

            subprocess.run(
                [sys.executable, "-c", report_code, str(source), str(destination), "test-version"],
                check=True,
            )
            result = json.loads(destination.read_text(encoding="utf-8"))["results"][0]

        self.assertEqual(result["error_log"], "/tmp/f8x-worker-logs/donpapi.log")
        self.assertEqual(result["error_summary"], "Error installing donpapi.")

    def test_worker_failure_uses_a_per_capability_error_log(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        worker_implementation = script.split("Worker_Tools(){", 1)[1].split(
            "# ===================== Tool Map", 1
        )[0]

        self.assertIn("/tmp/f8x-worker-logs", worker_implementation)
        self.assertIn('export F8X_WORKER_CURRENT_LOG="$error_log"', worker_implementation)
        self.assertIn("F8x_Worker_Error_Summary", worker_implementation)
        self.assertIn(
            'F8x_Worker_Record_Result "$capability" "failed" "$failure_detail" '
            '"$error_log" "$error_summary"',
            worker_implementation,
        )

    def test_worker_profile_reports_install_failures_without_failing_the_command(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        worker_functions = "F8x_Worker_Record_Result(){" + script.split(
            "F8x_Worker_Record_Result(){", 1
        )[1].split("# ===================== Tool Map", 1)[0]
        harness = f'''\
F8X_WORKER_CAPABILITIES="broken|definitely-not-an-f8x-command|Fail_Install|none|install|"
F8X_WORKER_RESOURCES=""
Echo_INFOR() {{ printf '%s\\n' "$*"; }}
Echo_ERROR() {{ :; }}
F8x_Worker_Find_Binary() {{ return 1; }}
F8x_Worker_Find_Resource() {{ return 1; }}
F8x_Worker_Ensure_Dependency() {{ return 0; }}
Fail_Install() {{ return 23; }}
{worker_functions}
F8x_Worker_Write_Report() {{ :; }}
Worker_Tools
status=$?
printf 'worker_status=%s\\n' "$status"
exit "$status"
'''

        result = subprocess.run(
            ["bash", "-c", harness],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("failed=1", result.stdout)
        self.assertIn("worker_status=0", result.stdout)

    def test_worker_mode_does_not_abort_remaining_arguments_after_install_failures(self):
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        worker_mode = script.split("-worker | worker)", 1)[1].split(";;", 1)[0]

        self.assertIn("Worker_Tools", worker_mode)
        self.assertNotIn("Worker_Tools || exit 1", worker_mode)

    def test_reports_missing_bins_unknown_entries_and_missing_functions(self):
        checker = _load_checker()
        catalog = {
            "tools": [
                {"name": "alpha", "bins": ["alpha", "alpha-cli"]},
                {"name": "beta"},
                {"name": "gamma"},
            ]
        }
        script = '''
F8X_WORKER_CAPABILITIES="
alpha|alpha|Alpha_Install|0|install|
beta|beta|-|0|skip|unsupported upstream
extra|extra|Extra_Install|0|install|
"
Alpha_Install(){ :; }
'''

        report = checker.check_catalog(catalog, script)

        self.assertEqual(report["missing"], ["gamma"])
        self.assertEqual(report["unknown"], ["extra"])
        self.assertEqual(report["bin_mismatches"], {"alpha": ["alpha-cli"]})
        self.assertEqual(report["missing_functions"], ["Extra_Install"])

    def test_current_worker_profile_matches_pojun_catalog(self):
        checker = _load_checker()
        default_catalog = (
            REPO_ROOT.parent.parent / "Agentic" / "pojun" / "common" / "capability_catalog.json"
        )
        catalog_path = Path(os.environ.get("POJUN_CAPABILITY_CATALOG", default_catalog))
        if not catalog_path.is_file():
            self.skipTest("PoJun capability catalog is not available in this checkout")

        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        script = (REPO_ROOT / "f8x").read_text(encoding="utf-8")
        report = checker.check_catalog(catalog, script)

        self.assertEqual(report["missing"], [])
        self.assertEqual(report["unknown"], [])
        self.assertEqual(report["bin_mismatches"], {})
        self.assertEqual(report["missing_functions"], [])
        self.assertEqual(report["invalid_entries"], [])
        self.assertEqual(report["installed_count"], 55)
        self.assertEqual(report["resource_count"], 5)
        self.assertEqual(report["installed_resource_count"], 5)
        self.assertEqual(report["missing_resources"], [])
        self.assertEqual(report["unknown_resources"], [])
        self.assertEqual(report["resource_path_mismatches"], {})
        self.assertEqual(
            report["skipped"],
            {
                "crackmapexec": "archived upstream; superseded by NetExec",
            },
        )
        self.assertIn("-worker | worker)", script)
        self.assertIn("export F8X_NONINTERACTIVE=1", script)
        self.assertIn('"${F8X_NONINTERACTIVE:-0}" = "1"', script)
        worker_implementation = script.split("F8x_Worker_Write_Report(){", 1)[1].split(
            "# ===================== Tool Map", 1
        )[0]
        self.assertIn("/tmp/f8x-worker-report.json", worker_implementation)
        self.assertNotIn("/opt/", worker_implementation)
        self.assertNotIn("F8x_Record_Install", worker_implementation)


if __name__ == "__main__":
    unittest.main()
