import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('coverage_validator', ROOT / 'scripts/validate_coverage.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CoverageTests(unittest.TestCase):
    def run_case(self, pages, inventory=None, edit=None, columns=None):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'coverage.csv'
            rows = []
            for page in pages:
                row = {k: 'checked' for k in validator.COLUMNS}
                row.update(source_id='DEMO', page_or_slide=str(page), disposition='covered')
                rows.append(row)
            if edit:
                edit(rows)
            with path.open('w', encoding='utf-8-sig', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=columns or validator.COLUMNS, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(rows)
            return validator.inspect_ledger(path, inventory)[0]

    def test_complete_inventory_and_utf8_bom(self):
        self.assertFalse(self.run_case([1, 2], {'DEMO': 2}))

    def test_entire_missing_page(self):
        self.assertIn('Missing page: DEMO/2', self.run_case([1], {'DEMO': 2}))

    def test_leading_zero_duplicate(self):
        self.assertTrue(any('repeated' in s for s in self.run_case([1, '01'])))

    def test_invalid_page_numbers(self):
        for page in ['0', '-1', '1.5', 'one']:
            with self.subTest(page=page):
                self.assertTrue(self.run_case([page]))

    def test_unresolved_disposition(self):
        self.assertTrue(self.run_case([1], edit=lambda r: r[0].update(disposition='uncertain')))

    def test_exclusion_needs_reason(self):
        self.assertTrue(self.run_case([1], edit=lambda r: r[0].update(disposition='duplicate', notes='')))

    def test_covered_page_needs_locator(self):
        self.assertTrue(self.run_case([1], edit=lambda r: r[0].update(summary_location='')))

    def test_unknown_source_and_out_of_range(self):
        self.assertTrue(self.run_case([1, 3], {'OTHER': 2}))

    def test_empty_ledger(self):
        self.assertTrue(self.run_case([]))

    def test_missing_columns(self):
        self.assertTrue(self.run_case([1], columns=['source_id']))

    def test_invalid_inventory(self):
        for inventory in [{}, {'DEMO': 0}, {'DEMO': True}, ['DEMO']]:
            with self.subTest(inventory=inventory), self.assertRaises(ValueError):
                self.run_case([1], inventory)

    def test_ledger_only_does_not_claim_completeness(self):
        self.assertFalse(self.run_case([2]))


if __name__ == '__main__':
    unittest.main()
