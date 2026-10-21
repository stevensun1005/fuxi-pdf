"""Build the fixed real-lecture demo; this is not an automatic course summarizer."""
import argparse
import csv
from hashlib import sha256
from io import BytesIO
import json
import math
from pathlib import Path
import re
from xml.sax.saxutils import escape

import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
INK = '#203b34'
SOURCE = json.loads((ROOT/'examples/source.json').read_text(encoding='utf-8'))
CONTENT = json.loads((ROOT/'examples/demo-content.json').read_text(encoding='utf-8'))


def paragraph(canvas, text, y, width, x=34, size=10.5, leading=15, bold=False, gap=5):
    style = ParagraphStyle('body', fontName='CN-Bold' if bold else 'CN', fontSize=size,
                           leading=leading, wordWrap='CJK', textColor=HexColor(INK))
    block = Paragraph(escape(text), style)
    _, height = block.wrap(width, 2000)
    block.drawOn(canvas, x, y-height)
    return y-height-gap


def walkthrough_flows(item, width):
    """Readable technical notes: prose, numbered headings, code, tables and a takeaway."""
    style=ParagraphStyle('walk-body',fontName='CN',fontSize=11.5,leading=18,
                         wordWrap='CJK',textColor=HexColor('#20262D'),spaceAfter=8)
    heading=ParagraphStyle('walk-heading',parent=style,fontName='CN-Bold',fontSize=12,leading=19,spaceBefore=7,spaceAfter=6)
    title=ParagraphStyle('walk-title',parent=heading,fontSize=15,leading=23,textColor=HexColor('#146B72'),spaceBefore=0,spaceAfter=10)
    cell=ParagraphStyle('walk-cell',parent=style,fontSize=10.5,leading=16,spaceAfter=0)
    th=ParagraphStyle('walk-table-heading',parent=cell,fontName='CN-Bold')
    code=ParagraphStyle('walk-code',parent=style,fontName='Code',fontSize=10.5,leading=16,spaceAfter=0)
    tip=ParagraphStyle('walk-tip',parent=style,fontName='CN-Bold',textColor=HexColor('#146B72'),spaceAfter=0)

    def code_text(text):
        parts=re.split(r'([^\x00-\x7f]+)',text.expandtabs(4))
        escaped=[escape(part).replace(' ','&#160;').replace('\n','<br/>') for part in parts]
        return ''.join('<font name="CN">'+value+'</font>' if any(ord(ch)>127 for ch in part) else value for part,value in zip(parts,escaped))

    def text(value, selected=style):
        pieces=re.split(r'(`[^`]+`)',value)
        rich=''.join('<font name="Code">'+code_text(p[1:-1])+'</font>' if p.startswith('`') else escape(p) for p in pieces)
        return Paragraph(rich,selected)

    flows=[text(item['title'],title)]
    for index,(label,body) in enumerate(item['walkthrough']):
        if index:flows.append(text(label,heading))
        flows.append(text(body))
        for block in item.get('walkthrough_insertions',[]):
            if block['after']!=index:continue
            if block['type']=='code':
                box=Table([[Paragraph(code_text(block['text']),code)]],colWidths=[width])
                box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor('#F1F3F4')),('BOX',(0,0),(-1,-1),.5,HexColor('#D9E1E3')),
                    ('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
            elif block['type']=='table':
                rows=[[text(value,th if index==0 else cell) for value in row] for index,row in enumerate([block['headers'],*block['rows']])]
                box=Table(rows,colWidths=[width*.38,width*.62])
                box.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#F5F7F7')),
                    ('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#D9E1E3')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
                    ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
            else:raise ValueError('Unknown walkthrough block: '+block['type'])
            box.spaceAfter=10;flows.append(box)
    box=Table([[text(item['takeaway'],tip)]],colWidths=[width])
    box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),HexColor('#EAF5F4')),('LEFTPADDING',(0,0),(-1,-1),11),('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),11)]))
    flows.append(box)
    return flows


def canvas_for(path, size):
    canvas = Canvas(path if isinstance(path, BytesIO) else str(path), pagesize=size,
                    initialFontName='CN', initialFontSize=10.5)
    canvas.setAuthor('fuxi-pdf; source lecture: Katrina LaCurts / MIT OpenCourseWare')
    canvas.setTitle('Real lecture demo: RAID 1, RAID 4 and RAID 5')
    canvas.setSubject('Adapted educational excerpt; CC BY-NC-SA 4.0; not an official course handout')
    return canvas


def footer(canvas, width, original, page, total):
    canvas.setFillColor(HexColor('#62746b'));canvas.setFont('CN', 7.2)
    canvas.drawString(34, 28, f'MIT 6.033 | Katrina LaCurts | Spring 2018 | 原课件 p.{original}')
    canvas.drawRightString(width-34, 28, f'fuxi-pdf / {page} of {total}')
    canvas.drawString(34, 16, 'CC BY-NC-SA 4.0 | 选页与中文讲解：fuxi-pdf | 非官方示例')
    canvas.linkURL(SOURCE['resource_url'], (34, 26, width-130, 37), relative=0)
    canvas.linkURL(SOURCE['license_url'], (34, 13, 125, 24), relative=0)


def extract_source(full_pdf, output):
    if sha256(full_pdf.read_bytes()).hexdigest() != SOURCE['upstream_sha256']:
        raise ValueError('Source PDF differs from the inspected version in source.json.')
    reader = PdfReader(full_pdf)
    assert len(reader.pages) == SOURCE['upstream_page_count']
    writer = PdfWriter()
    for number in SOURCE['selected_pages']:
        writer.add_page(reader.pages[number-1])
    writer.add_metadata({'/Title':'MIT 6.033 Lecture 14 - excerpt of original pages 11-13',
                         '/Author':SOURCE['author'], '/Subject':SOURCE['resource_url']+' | '+SOURCE['license']})
    with output.open('wb') as handle:
        writer.write(handle)


def build_walkthrough(source, path):
    width, minimum_height = A4;usable=width-68
    originals = PdfReader(source)
    assert len(originals.pages) == len(CONTENT)
    memory = BytesIO();canvas = canvas_for(memory,A4)
    transforms = []
    for page, (slide, item) in enumerate(zip(originals.pages,CONTENT),1):
        scale = usable/float(slide.mediabox.width)
        slide_height=float(slide.mediabox.height)*scale
        flows=walkthrough_flows(item,usable)
        sizes=[flow.wrap(usable,10000)[1] for flow in flows]
        body_height=sum(size+flow.getSpaceBefore()+flow.getSpaceAfter() for flow,size in zip(flows,sizes))
        height=max(minimum_height,math.ceil((43+slide_height+14+body_height+50)/(10*72/25.4))*(10*72/25.4))
        canvas.setPageSize((width,height))
        paragraph(canvas, f'真实课件精讲 / 原页 {item["original_page"]} / 节选 {page} of {len(CONTENT)}', height-18, usable,size=9,leading=12)
        slide_y=height-43-slide_height
        transforms.append(Transformation().scale(scale).translate(34,slide_y))
        canvas.setStrokeColor(HexColor('#D9E1E3'));canvas.setLineWidth(.5)
        canvas.rect(33.7,slide_y-.3,usable+.6,slide_height+.6,stroke=1,fill=0)
        y=slide_y-14
        for flow,size in zip(flows,sizes):
            y-=flow.getSpaceBefore()+size;flow.drawOn(canvas,34,y);y-=flow.getSpaceAfter()
        assert y>44, ('Walkthrough overflow',page,y)
        footer(canvas,width,item['original_page'],page,len(CONTENT));canvas.showPage()
    canvas.save();memory.seek(0)
    writer=PdfWriter()
    for index,overlay in enumerate(PdfReader(memory).pages):
        writer.add_page(overlay)
        writer.pages[-1].merge_transformed_page(originals.pages[index],transforms[index])
        writer.add_outline_item(f'原页 {CONTENT[index]["original_page"]}: {CONTENT[index]["title"]}',index)
    writer.add_metadata({'/Title':'真实课件逐页中文精讲：RAID', '/Author':'fuxi-pdf; Katrina LaCurts (source lecture)', '/Subject':SOURCE['license_url']})
    with path.open('wb') as handle:
        writer.write(handle)


def comparison(canvas,y,width):
    rows=[['方案','物理盘数 / 可用容量','主要取舍'],
          ['RAID 1','2N / N×C','完整镜像；容量开销大'],
          ['RAID 4','N+1 / N×C','专用校验盘；写入集中'],
          ['RAID 5','N+1 / N×C','分布校验；仍需更新校验']]
    table=Table(rows,colWidths=[72,150,width-222],rowHeights=22)
    table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'CN'),('FONTSIZE',(0,0),(-1,-1),9),
        ('BACKGROUND',(0,0),(-1,0),HexColor('#edf3ee')),('TEXTCOLOR',(0,0),(-1,-1),HexColor(INK)),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,-1),0.3,HexColor('#b8c5bd'))]))
    _,h=table.wrap(width,1000);table.drawOn(canvas,34,y-h)
    return y-h-5


def build_exam(path):
    width,height=letter;usable=width-68;canvas=canvas_for(path,letter)
    for page,item in enumerate(CONTENT,1):
        y=paragraph(canvas,item['title'],height-29,usable,size=16,leading=23,bold=True,gap=7)
        y=paragraph(canvas,'考点册 / 中文理解 → English answers / 原页 '+str(item['original_page']),y,usable,size=9,leading=13,gap=10)
        for heading,body in item['chinese']:
            y=paragraph(canvas,heading,y,usable,bold=True)
            y=paragraph(canvas,body,y,usable,gap=8)
        y=paragraph(canvas,'考试英文表述',y,usable,bold=True)
        y=paragraph(canvas,item['english'],y,usable,gap=9)
        for question,answer in item['questions']:
            y=paragraph(canvas,question,y,usable,bold=True)
            y=paragraph(canvas,answer,y,usable,gap=8)
        if page==3:
            y=comparison(canvas,y-3,usable)
            y=paragraph(canvas,'N：原始数据所需等容量盘数；C：单盘容量。三者均可恢复任意单盘失效；均不代替独立备份。',y,usable,size=9,leading=13)
        assert y>44, ('Exam reference overflow',page,y)
        canvas.bookmarkPage(str(page));canvas.addOutlineEntry(item['title'],str(page),level=0)
        footer(canvas,width,item['original_page'],page,len(CONTENT));canvas.showPage()
    canvas.save()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font',type=Path)
    parser.add_argument('--source-pdf',type=Path,help='Re-extract inspected pages from the original 15-page lecture PDF')
    args=parser.parse_args()
    candidates=[args.font,Path('C:/Windows/Fonts/msyh.ttc'),Path('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')]
    font=next((p for p in candidates if p and p.is_file()),None)
    if font is None:parser.error('Supply --font with a CJK TrueType .ttf/.ttc font.')
    pdfmetrics.registerFont(TTFont('CN',str(font),subfontIndex=0))
    bold=font.with_name('msyhbd.ttc') if font.name.lower()=='msyh.ttc' else font
    pdfmetrics.registerFont(TTFont('CN-Bold',str(bold if bold.is_file() else font),subfontIndex=0))
    mono=next((p for p in [Path('C:/Windows/Fonts/consola.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')] if p.is_file()),None)
    if mono:pdfmetrics.registerFont(TTFont('Code',str(mono)))
    else:pdfmetrics.registerFont(pdfmetrics.Font('Code','Courier','WinAnsiEncoding'))
    source=ROOT/'examples/input/demo-slides.pdf';walk=ROOT/'examples/output/slide-walkthrough.pdf';exam=ROOT/'examples/output/exam-reference.pdf'
    for directory in (source.parent,walk.parent,ROOT/'docs/assets'):
        directory.mkdir(parents=True,exist_ok=True)
    if args.source_pdf:extract_source(args.source_pdf,source)
    build_walkthrough(source,walk);build_exam(exam)
    for path,name in [(walk,'walkthrough'),(exam,'exam-reference')]:
        doc=pdfium.PdfDocument(str(path))
        doc[1].render(scale=1.5).to_pil().save(ROOT/f'docs/assets/{name}.png');doc.close()
    source_id=SOURCE['source_id']
    (ROOT/'examples/inventory.json').write_text(json.dumps({source_id:len(CONTENT)},indent=2)+'\n',encoding='utf-8')
    columns='source_id lecture_id page_or_slide topic concept_id importance disposition summary_location explanation_depth visual_check citation notes'.split()
    with (ROOT/'examples/coverage.csv').open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=columns);writer.writeheader()
        for page,item in enumerate(CONTENT,1):
            writer.writerow(dict(source_id=source_id,lecture_id='MIT6.033-L14',page_or_slide=page,topic=item['title'],disposition='covered',concept_id=item['concept'],importance='Demo selection, not an exam prediction',summary_location=f'slide-walkthrough.pdf p.{page}; exam-reference.pdf p.{page}',explanation_depth='Diagram, mechanism, example, limitations, English answers',visual_check='manual inspection required after rebuilding',citation=f'MIT 6.033 L14 original p.{item["original_page"]}',notes=f'Excerpt page {page}; original page {item["original_page"]}; only original pp.11-13 are in scope'))
    print('Built 3 A4-width extended walkthrough pages, 3 Letter reference pages, two previews and the three-page excerpt ledger.')


if __name__=='__main__':main()
