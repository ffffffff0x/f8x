import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK_RELEASES_PATH = REPO_ROOT / "check_releases.py"


def _load_check_releases():
    spec = importlib.util.spec_from_file_location("check_releases", CHECK_RELEASES_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {CHECK_RELEASES_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CheckReleasesTests(unittest.TestCase):
    def test_excludes_repositories_that_do_not_track_compatible_releases(self):
        checker = _load_check_releases()
        lines = [
            "# https://github.com/chaitin/xray/releases\n",
            'xray_Ver="1.9.11"\n',
            "# https://github.com/praetorian-inc/fingerprintx\n",
            'fingerprintx_Ver="v1.1.13"\n',
            "# https://github.com/projectdiscovery/nuclei/releases\n",
            'Nuclei_Ver="v3.11.0"\n',
        ]

        entries = checker.parse_entries(lines)

        self.assertEqual(
            [(entry.owner, entry.repo, entry.var) for entry in entries],
            [("projectdiscovery", "nuclei", "Nuclei_Ver")],
        )


if __name__ == "__main__":
    unittest.main()
