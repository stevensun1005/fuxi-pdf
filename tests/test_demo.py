"""Check the actual published PDFs; visual review remains a separate gate."""
from pathlib import Path
import json
import unittest

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


class DemoTests(unittest.TestCase):
    def test_page_counts_and_paper(self):
        for relative, count, dimensions in [
            ('input/demo-slides.pdf', 3, (1024, 768)),
            ('output/slide-walkthrough.pdf', 3, (595.28, 841.89)),
            ('output/exam-reference.pdf', 3, (612, 792)),
        ]:
            with self.subTest(file=relative):
                reader = PdfReader(ROOT / 'examples' / relative)
                self.assertEqual(len(reader.pages), count)
                for page in reader.pages:
                    self.assertAlmostEqual(float(page.mediabox.width), dimensions[0], places=1)
                    self.assertAlmostEqual(float(page.mediabox.height), dimensions[1], places=1)

    def test_chinese_and_english_are_extractable(self):
        walk = PdfReader(ROOT / 'examples/output/slide-walkthrough.pdf')
        for i,term in enumerate(['镜像', 'XOR', '校验']):
            self.assertIn(term, walk.pages[i].extract_text())
        exam = PdfReader(ROOT / 'examples/output/exam-reference.pdf')
        for page in exam.pages:
            text=page.extract_text()
            for phrase in ['中文理解', '考试英文表述', 'Q1.', 'Q2.', 'CC BY-NC-SA 4.0']:
                self.assertIn(phrase,text)
            self.assertLess(text.index('中文理解'),text.index('考试英文表述'))
        self.assertIn('two missing blocks',exam.pages[2].extract_text().lower())

    def test_real_source_identity_and_original_page_mapping(self):
        meta=json.loads((ROOT/'examples/source.json').read_text(encoding='utf-8'))
        self.assertEqual(meta['selected_pages'],[11,12,13])
        source=PdfReader(ROOT/'examples/input/demo-slides.pdf')
        walk=PdfReader(ROOT/'examples/output/slide-walkthrough.pdf')
        for i,level in enumerate([1,4,5]):
            for reader in [source,walk]:
                text=reader.pages[i].extract_text()
                self.assertIn(f'RAID {level}',text)
                self.assertIn('Katrina LaCurts',text)
                self.assertIn(str(meta['selected_pages'][i]),text)
        self.assertEqual(len(walk.outline),3)

    def test_cjk_fonts_embedded(self):
        for path in (ROOT / 'examples/output').glob('*.pdf'):
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
