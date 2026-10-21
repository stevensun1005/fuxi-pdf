"""Build three original demo PDFs and their README previews (not a course generator)."""
import argparse
from io import BytesIO
from pathlib import Path
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
INK, TEAL, LIGHT = '#203b34', '#26705d', '#edf3ee'


def paragraph(canvas, text, y, width, x=34, size=11, leading=17, bold=False):
    style = ParagraphStyle('body', fontName='CN-Bold' if bold else 'CN', fontSize=size,
                           leading=leading, wordWrap='CJK', textColor=HexColor(INK))
    block = Paragraph(escape(text).replace('\n', '<br/>'), style)
    _, height = block.wrap(width, 2000)
    block.drawOn(canvas, x, y - height)
    return y - height - 8


def canvas_for(path, size):
    canvas = Canvas(str(path), pagesize=size)
    canvas.setAuthor('fuxi-pdf')
    canvas.setTitle(Path(str(path)).stem if not isinstance(path, BytesIO) else 'Chinese walkthrough')
    return canvas


def build_slides(path):
    canvas = canvas_for(path, (720, 405))
    for number in [1, 2]:
        canvas.setFillColor(HexColor(INK));canvas.rect(0, 0, 720, 405, fill=1, stroke=0)
        canvas.setFillColor(HexColor('#b8d5c3'));canvas.setFont('CN', 12)
        canvas.drawString(40, 365, f'FUXI-PDF / ORIGINAL DEMO / {number:02d}')
        canvas.setFillColor(HexColor('#ffffff'));canvas.setFont('CN-Bold', 30)
        canvas.drawString(40, 309, 'Why mean-of-means fails' if number == 1 else 'Keep a mergeable state')
        for x, label, value, detail in [(40, 'PARTITION A', '[2, 4]', 'mean = 3' if number == 1 else '(sum, count) = (6, 2)'),
                                        (380, 'PARTITION B', '[12]', 'mean = 12' if number == 1 else '(sum, count) = (12, 1)')]:
            canvas.setFillColor(HexColor('#ffffff'));canvas.roundRect(x, 129, 300, 139, 9, fill=1, stroke=0)
            canvas.setFillColor(HexColor(TEAL));canvas.setFont('CN', 12);canvas.drawString(x+18, 240, label)
            canvas.setFont('CN-Bold', 29);canvas.drawString(x+18, 194, value)
            canvas.setFont('CN', 16);canvas.drawString(x+18, 155, detail)
        canvas.setFillColor(HexColor('#ffffff'));canvas.setFont('CN', 18)
        canvas.drawString(40, 83, '(3 + 12) / 2 = 7.5    but    (2 + 4 + 12) / 3 = 6' if number == 1 else
                          'Merge: (6, 2) + (12, 1) = (18, 3).  Finalize: 18 / 3 = 6.')
        canvas.setFont('CN', 10);canvas.drawString(40, 34, 'Original teaching example. No course materials used.')
        canvas.showPage()
    canvas.save()


def footer(canvas, width, text):
    canvas.setFont('CN', 8.5);canvas.setFillColor(HexColor('#62746b'))
    canvas.drawString(34, 24, text)
    canvas.drawRightString(width-34, 24, 'fuxi-pdf / demo')


def build_walkthrough(source, path):
    width, height = A4
    memory = BytesIO();canvas = Canvas(memory, pagesize=A4)
    canvas.setAuthor('fuxi-pdf');canvas.setTitle('Slide walkthrough / Chinese teaching')
    notes = [
        ('为什么“平均局部平均值”会算错？', [
            ('这页在讲什么', '问题不是加法算错了，而是局部平均值丢掉了它代表多少条记录。A 有两个观测值，B 只有一个；两组均值不能直接当成等重的两条观测。'),
            ('1. 先算两组局部结果', 'A 的数据是 2、4，局部均值为 (2+4)/2=3。B 只有 12，局部均值为 12。若把 3 和 12 直接平均，得到 7.5，但这个动作把 B 的单条记录赋予了整组 A 的权重。'),
            ('2. 回到原问题检查答案', '原问题是三条记录的平均值，总和为 18、数量为 3，因此结果是 6。加机器或改变分区不应改变这个逻辑答案；问题在于中间表示没有保留计算所需信息。'),
            ('3. 什么时候局部均值可以再平均？', '各组大小相同，或明确按组内数量加权时才成立。一般分布式分组不能擅自假设组大小相同。下一页用可合并状态保留权重。')
        ], '记住：分组方式会变，但全局答案不应因丢失组大小而改变。'),
        ('保留 (sum, count)，最后再除一次', [
            ('这页在讲什么', '把平均值改写为能继续合并的状态：总和 sum 与数量 count。状态代表一个组贡献的全部信息，而不是已经丢掉权重的最终均值。'),
            ('1. 每条记录变成状态', '输入数值 x 先变成 (x,1)。A 合并为 (6,2)，B 合并为 (12,1)。即使先局部合并、再跨机器合并，状态的意义仍保持一致。'),
            ('2. 合并只做分量相加', '(s1,c1) 与 (s2,c2) 合并为 (s1+s2,c1+c2)，所以两组变成 (18,3)。在整数精确且不溢出的假设下，加法允许重新分组；浮点数舍入时还需注意精度。'),
            ('3. 最后计算输出', '只有所有贡献都合并完成后才计算 sum/count，得到 18/3=6。count=0 时按问题约定处理；涉及整数类型时，也要确认除法语义。部分结果应始终具有兼容的状态类型。')
        ], '记住：先保存足够信息，再安全合并，最后才做不可逆的结果计算。')
    ]
    slide_width = width - 68;slide_height = slide_width * 405 / 720
    for page, (title, sections, takeaway) in enumerate(notes, 1):
        y = paragraph(canvas, f'DEMO · 原课件第 {page} 页', height-22, slide_width, size=9, leading=12)
        y = height - 45 - slide_height - 17
        y = paragraph(canvas, title, y, slide_width, size=15, leading=22, bold=True)
        for heading, text in sections:
            y = paragraph(canvas, heading, y, slide_width, bold=True)
            y = paragraph(canvas, text, y, slide_width, size=10.5, leading=16)
        y = paragraph(canvas, takeaway, y-2, slide_width, size=10.5, leading=16, bold=True)
        assert y > 40, ('Walkthrough overflow', page, y)
        footer(canvas, width, f'来源：原创演示课件 p.{page} | 成品 {page}/2')
        canvas.showPage()
    canvas.save();memory.seek(0)
    writer = PdfWriter();originals = PdfReader(source);overlays = PdfReader(memory)
    for i, overlay in enumerate(overlays.pages):
        writer.add_page(overlay)
        scale = slide_width / 720
        writer.pages[-1].merge_transformed_page(originals.pages[i], Transformation().scale(scale).translate(34, height-45-slide_height))
    writer.add_metadata({'/Title':'Chinese slide walkthrough','/Author':'fuxi-pdf'})
    with path.open('wb') as handle:writer.write(handle)


def build_exam(path):
    width, height = letter;usable = width-68;canvas = canvas_for(path, letter)
    y = paragraph(canvas, '重点速查：平均值与可合并状态', height-34, usable, size=17, leading=24, bold=True)
    y = paragraph(canvas, 'Mean aggregation / 中文理解 → English answers', y, usable, size=10, leading=14)
    for head, body in [
        ('一、中文理解', '平均值不仅依赖各组的结果，也依赖组内记录数。任意局部平均值直接平均会改变观测的权重，因此中间结果必须保留总和与数量。'),
        ('机制与前提', '每个数值 x 变成 (x,1)，状态按分量相加。最后在 count>0 时计算 sum/count。局部结果要能继续作为同类型状态参与合并；数值溢出、浮点舍入和空组需要按任务约定处理。'),
        ('手算反例', 'A=[2,4] 的均值为 3；B=[12] 的均值为 12。直接平均得到 7.5。正确结果为 (6+12)/(2+1)=6。若各组数量相同，直接平均局部均值才与正确加权结果一致。'),
        ('易错点', '局部均值丢失权重；中间状态不是最终答案；改变分区或合并树，不应在数学模型中改变业务问题。')]:
        y=paragraph(canvas, head, y, usable, bold=True)
        y=paragraph(canvas, body, y, usable, size=10.5, leading=15)
    y=paragraph(canvas, '二、考试英文表述', y, usable, bold=True)
    y=paragraph(canvas, 'A mean cannot generally be combined by averaging local means, because the groups may have different counts. Preserve a sum-count state, merge both components, and divide only after the final aggregation. This retains each observation’s weight. The state type must remain compatible with repeated merging, and zero counts and numeric division semantics need explicit handling.', y, usable, size=10.5, leading=14.5)
    for q,a in [
        ('Q1. Why is the unweighted mean of local means unsafe?', 'It treats groups as equally weighted even when their counts differ. For [2,4] and [12], it gives 7.5 instead of the global mean 6.'),
        ('Q2. What information makes a mean safely mergeable?', 'Keep the sum and count of each partial group. Add the corresponding components and divide once at the end; this preserves the information required for correct weighting.')]:
        y=paragraph(canvas,q,y,usable,size=10.5,leading=14.5,bold=True)
        y=paragraph(canvas,a,y,usable,size=10.5,leading=14.5)
    assert y > 44, ('Exam reference overflow', y)
    footer(canvas,width,'来源：原创演示 p.1–2 | Letter / 单面 1 页 / 100%')
    canvas.save()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font',type=Path)
    args=parser.parse_args()
    candidates=[args.font,Path('C:/Windows/Fonts/msyh.ttc'),Path('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')]
    font=next((p for p in candidates if p and p.is_file()),None)
    if font is None:parser.error('Supply --font with a CJK TrueType .ttf/.ttc font.')
    pdfmetrics.registerFont(TTFont('CN',str(font),subfontIndex=0))
    bold=font.with_name('msyhbd.ttc') if font.name.lower()=='msyh.ttc' else font
    pdfmetrics.registerFont(TTFont('CN-Bold',str(bold if bold.is_file() else font),subfontIndex=0))
    source=ROOT/'examples/input/demo-slides.pdf';walk=ROOT/'examples/output/slide-walkthrough.pdf';exam=ROOT/'examples/output/exam-reference.pdf'
    for directory in (source.parent,walk.parent,ROOT/'docs/assets'):
        directory.mkdir(parents=True,exist_ok=True)
    build_slides(source);build_walkthrough(source,walk);build_exam(exam)
    for path,name in [(walk,'walkthrough'),(exam,'exam-reference')]:
        doc=pdfium.PdfDocument(str(path));doc[0].render(scale=1.3).to_pil().save(ROOT/f'docs/assets/{name}.png');doc.close()
    import csv
    import json
    (ROOT/'examples/inventory.json').write_text(json.dumps({'DEMO':2},indent=2)+'\n',encoding='utf-8')
    columns='source_id lecture_id page_or_slide topic concept_id importance disposition summary_location explanation_depth visual_check citation notes'.split()
    with (ROOT/'examples/coverage.csv').open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=columns);writer.writeheader()
        for page,concept in [(1,'mean-of-means'),(2,'sum-count-state')]:
            writer.writerow(dict(source_id='DEMO',lecture_id='demo',page_or_slide=page,topic='Mean aggregation',disposition='covered',concept_id=concept,importance='Inferred: demonstration focus',summary_location=f'slide-walkthrough.pdf p.{page}; exam-reference.pdf p.1',explanation_depth='Mechanism, example and caveat',visual_check='manual inspection required after rebuilding',citation=f'DEMO p.{page}',notes='Original demonstration material'))
    print('Built 2 source slides, 2 walkthrough pages, 1 Letter reference, both previews and the coverage ledger.')


if __name__=='__main__':main()
