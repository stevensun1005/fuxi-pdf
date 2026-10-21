"""Regression checks for the published one-page mathematical reference."""
import csv
import json
from pathlib import Path
import re
import unittest

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1] / 'examples' / 'compact-math'


class CompactMathTests(unittest.TestCase):
    def test_single_standard_landscape_page(self):
        reader = PdfReader(ROOT / 'cheatsheet.pdf')
        self.assertEqual(len(reader.pages), 1)
        self.assertEqual(tuple(float(v) for v in reader.pages[0].mediabox), (0, 0, 792, 612))
        self.assertEqual(reader.pages[0].get('/Rotate', 0), 0)

    def test_twenty_topics_and_english_survive_export(self):
        text = PdfReader(ROOT / 'cheatsheet.pdf').pages[0].extract_text()
        headings = ['Systems: three pictures', 'Products and transposes', 'Elimination, permutations, LU',
                    'Invertibility', 'Subspaces: the closure test', 'RREF, rank and nullspace',
                    'Consistency and solution count', 'Independence, basis, dimension',
                    'Four fundamental subspaces', 'Matrix spaces and rank one',
                    'Graphs and network matrices', 'Orthogonality and normal equations',
                    'Orthogonal projections', 'Least squares and line fitting', 'Orthonormal columns',
                    'Gram–Schmidt and QR', 'Determinants and elimination',
                    'Cofactors and determinant formulas', 'Inverse, Cramer and volume',
                    'Exam workflow and checks']
        for i, title in enumerate(headings, 1):
            self.assertRegex(text, rf'(?m)^{i:02} .*{re.escape(title)}')
        # Protect English-first density while retaining a few CJK clarifications.
        latin = len(re.findall(r'[A-Za-z]', text))
        chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
        self.assertGreater(chinese, 0)
        self.assertGreater(latin, 10 * chinese)
        self.assertLessEqual(text.count('中文提示'), 6)
        self.assertIn('CC BY-NC-SA 4.0', text)
        self.assertNotIn('\ufffd', text)

    def test_cjk_and_math_fonts_are_embedded(self):
        fonts = PdfReader(ROOT / 'cheatsheet.pdf').pages[0]['/Resources']['/Font']
        names = []
        for ref in fonts.values():
            font = ref.get_object()
            names.append(str(font['/BaseFont']))
            for descendant in font.get('/DescendantFonts', [ref]):
                descriptor = descendant.get_object()['/FontDescriptor'].get_object()
                self.assertTrue(any(k in descriptor for k in ('/FontFile', '/FontFile2', '/FontFile3')))
        self.assertTrue(any('YaHei' in name for name in names))
        self.assertTrue(any('Math' in name for name in names))

    def test_source_inventory_and_citation_bounds(self):
        sources = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))['sources']
        inventory = json.loads((ROOT / 'inventory.json').read_text(encoding='utf-8'))
        self.assertEqual(len(sources), 21)
        self.assertEqual(sum(inventory.values()), 85)
        self.assertEqual(inventory, {s['source_id']: s['pages'] for s in sources})
        with (ROOT / 'coverage.csv').open(encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        actual = [(r['source_id'], int(r['page_or_slide'])) for r in rows]
        expected = {(sid, p) for sid, count in inventory.items() for p in range(1, count + 1)}
        self.assertEqual(len(actual), len(expected))
        self.assertEqual(set(actual), expected)
        manuscript = (ROOT / 'cheatsheet.typ').read_text(encoding='utf-8')
        for sid, first, last in re.findall(r'(S\d{2}) p(\d+)(?:[–-](\d+))?', manuscript):
            self.assertTrue(1 <= int(first) <= int(last or first) <= inventory[sid])


if __name__ == '__main__':
    unittest.main()
