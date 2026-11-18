import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from library.presentation.cli.main import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.config = root / "appsettings.json"
        self.config.write_text(json.dumps({
            "Storage": {"Type": "json", "Path": str(root / "books.json")},
            "Loan": {"DefaultDays": 14},
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--config", str(self.config), *args])
        return code, out.getvalue()

    def test_full_scenario(self):
        code, out = self.run_cli("add", "Кобзар", "Тарас Шевченко", "1840")
        self.assertEqual(code, 0)
        book_id = out.split("[")[1].split("]")[0]
        _, out = self.run_cli("borrow", book_id, "Олена")
        self.assertIn("видана: Олена", out)
        _, out = self.run_cli("list", "--available")
        self.assertIn("Каталог порожній", out)
        _, out = self.run_cli("return", book_id)
        self.assertIn("доступна", out)


if __name__ == "__main__":
    unittest.main()
