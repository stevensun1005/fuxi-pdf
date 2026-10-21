"""Check the actual published PDFs; visual review remains a separate gate."""
from pathlib import Path
import json
import unittest

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


class DemoTests(unittest.TestCase):
    def test_page_counts_and_paper(self):
        for relative, count, dimensions in [
            ('input/demo-slides.pdf', 15, None),
            ('output/slide-walkthrough.pdf', 15, (595.28, None)),
            ('output/exam-reference.pdf', 10, (612, 792)),
        ]:
            with self.subTest(file=relative):
                reader = PdfReader(ROOT / 'examples' / relative)
                self.assertEqual(len(reader.pages), count)
                for page in reader.pages:
                    if dimensions is None:continue
                    self.assertAlmostEqual(float(page.mediabox.width), dimensions[0], places=1)
                    if dimensions[1] is None:
                        self.assertGreaterEqual(float(page.mediabox.height),841.88)
                    else:
                        self.assertAlmostEqual(float(page.mediabox.height), dimensions[1], places=1)

    def test_walkthrough_blocks_preserve_the_complete_teaching_text(self):
        items=json.loads((ROOT/'examples/demo-content.json').read_text(encoding='utf-8'))
        reader=PdfReader(ROOT/'examples/output/slide-walkthrough.pdf')
        compact=lambda text: ''.join(text.replace('`','').split())
        for item,page in zip(items,reader.pages):
            actual=compact(page.extract_text())
            expected=[item['title'],item['takeaway']]
            expected.extend(body for heading,body in item['walkthrough'])
            for block in item['walkthrough_insertions']:
                if block['type']=='code':expected.append(block['text'])
                else:expected.extend(value for row in [block['headers'],*block['rows']] for value in row)
            for text in expected:
                self.assertIn(compact(text),actual)
            if any(block['type']=='code' for block in item['walkthrough_insertions']):
                fonts=[str(font.get_object().get('/BaseFont','')) for font in page['/Resources']['/Font'].values()]
                self.assertTrue(any(any(name in font for name in ['Consolas','DejaVuSansMono','Courier']) for font in fonts))

    def test_chinese_and_english_are_extractable(self):
        walk = PdfReader(ROOT / 'examples/output/slide-walkthrough.pdf')
        for i,term in [(6,'可用性'),(8,'MTBF'),(10,'镜像'),(11,'XOR'),(12,'校验')]:
            self.assertIn(term, walk.pages[i].extract_text())
        exam = PdfReader(ROOT / 'examples/output/exam-reference.pdf')
        text='\n'.join(page.extract_text() for page in exam.pages)
        for phrase in ['中文理解', '考试英文表述', 'Q1.', 'Q2.', 'CC BY-NC-SA 4.0','目录','English index','Source map']:
            self.assertIn(phrase,text)
        self.assertIn('two missing blocks',text.lower())

    def test_real_source_identity_and_original_page_mapping(self):
        meta=json.loads((ROOT/'examples/source.json').read_text(encoding='utf-8'))
        self.assertEqual(meta['selected_pages'],list(range(1,16)))
        source=PdfReader(ROOT/'examples/input/demo-slides.pdf')
        walk=PdfReader(ROOT/'examples/output/slide-walkthrough.pdf')
        for i,level in [(10,1),(11,4),(12,5)]:
            for reader in [source,walk]:
                text=reader.pages[i].extract_text()
                self.assertIn(f'RAID {level}',text)
                self.assertIn('Katrina LaCurts',text)
                self.assertIn(str(meta['selected_pages'][i]),text)
        self.assertEqual(len(walk.outline),15)

    def test_excluded_vendor_image_is_replaced_explicitly(self):
        reader=PdfReader(ROOT/'examples/input/demo-slides.pdf')
        self.assertEqual(len(reader.pages[8].images),0)
        text=reader.pages[8].extract_text()
        self.assertIn('Public adaptation',text)
        self.assertIn('excluded',text)
        meta=json.loads((ROOT/'examples/source.json').read_text(encoding='utf-8'))
        self.assertEqual(meta['replaced_pages'],[9])

    def test_rotated_source_page_is_upright_when_embedded(self):
        source=PdfReader(ROOT/'examples/input/demo-slides.pdf')
        self.assertEqual(source.pages[-1].rotation,90)
        walk=PdfReader(ROOT/'examples/output/slide-walkthrough.pdf')
        self.assertIn('https://ocw.mit.edu/terms',walk.pages[-1].extract_text(orientations=(0,)))

    def test_all_exam_teaching_and_answers_survive_pagination(self):
        items=json.loads((ROOT/'examples/exam-content.json').read_text(encoding='utf-8'))
        reader=PdfReader(ROOT/'examples/output/exam-reference.pdf')
        compact=lambda text: ''.join(text.replace('`','').split())
        actual=compact(''.join(page.extract_text() for page in reader.pages))
        for item in items:
            expected=[item['english'],item['takeaway']]
            expected.extend(body for label,body in item['walkthrough'])
            expected.extend(value for pair in item['questions'] for value in pair)
            for block in item['walkthrough_insertions']:
                expected.extend([block['text']] if block['type']=='code' else [value for row in [block['headers'],*block['rows']] for value in row])
            for value in expected:self.assertIn(compact(value),actual)
            self.assertLess(actual.index(compact(item['walkthrough'][0][1])),actual.index(compact(item['english'])))

    def test_printed_concept_destinations_match_actual_pages(self):
        report=json.loads((ROOT/'examples/build-report.json').read_text(encoding='utf-8'))
        reader=PdfReader(ROOT/'examples/output/exam-reference.pdf')
        self.assertEqual(len(reader.pages),report['exam']['pages'])
        for destination in reader.outline:
            title=destination.title
            key=title[:3] if title.startswith('C0') else 'IDX' if title.startswith('英文术语') else 'APP'
            self.assertEqual(reader.get_destination_page_number(destination)+1,report['exam']['chapter_pages'][key])
        for key,page in report['exam']['chapter_pages'].items():
            expected=key if key.startswith('C0') else 'English index' if key=='IDX' else 'Source map'
            self.assertIn(expected,reader.pages[page-1].extract_text())

    def test_availability_example_and_full_inventory(self):
        self.assertAlmostEqual(43200/43210,0.99976857,places=8)
        text=''.join(page.extract_text() for page in PdfReader(ROOT/'examples/output/exam-reference.pdf').pages)
        self.assertIn('0.99976857',text)
        inventory=json.loads((ROOT/'examples/inventory.json').read_text(encoding='utf-8'))
        self.assertEqual(inventory,{'MIT6.033-L14':15})

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
