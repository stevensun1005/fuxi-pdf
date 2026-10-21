"""Check the actual published PDFs; visual review remains a separate gate."""
from pathlib import Path
import unittest

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


class DemoTests(unittest.TestCase):
    def test_page_counts_and_paper(self):
        for relative, count, dimensions in [
            ('input/demo-slides.pdf', 2, (720, 405)),
            ('output/slide-walkthrough.pdf', 2, (595.28, 841.89)),
            ('output/exam-reference.pdf', 1, (612, 792)),
        ]:
            with self.subTest(file=relative):
                reader = PdfReader(ROOT / 'examples' / relative)
                self.assertEqual(len(reader.pages), count)
                for page in reader.pages:
                    self.assertAlmostEqual(float(page.mediabox.width), dimensions[0], places=1)
                    self.assertAlmostEqual(float(page.mediabox.height), dimensions[1], places=1)

    def test_chinese_and_english_are_extractable(self):
        walk = PdfReader(ROOT / 'examples/output/slide-walkthrough.pdf')
        self.assertIn('局部平均值', walk.pages[0].extract_text())
        self.assertIn('合并', walk.pages[1].extract_text())
        exam = PdfReader(ROOT / 'examples/output/exam-reference.pdf').pages[0].extract_text()
        for phrase in ['中文理解', '考试英文表述', 'Q1.', 'Q2.', '7.5', 'sum-count']:
            self.assertIn(phrase, exam)
        self.assertLess(exam.index('中文理解'), exam.index('考试英文表述'))

    def test_cjk_fonts_embedded(self):
        for path in (ROOT / 'examples').rglob('*.pdf'):
            found = 0
            for page in PdfReader(path).pages:
                for reference in page['/Resources'].get('/Font', {}).values():
                    font = reference.get_object()
                    descriptor = font.get('/FontDescriptor')
                    if descriptor:
                        descriptor = descriptor.get_object()
                        self.assertTrue(any(k in descriptor for k in ['/FontFile', '/FontFile2', '/FontFile3']))
                        found += 1
            self.assertGreater(found, 0, str(path))


if __name__ == '__main__':
    unittest.main()
