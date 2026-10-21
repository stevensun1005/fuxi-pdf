---
name: fuxi-pdf
description: 复习pdf：将 PDF/PPTX 课件、教材或提取文本制作成带来源页码的复习 PDF。支持原页在上、中文精讲在下的逐页版，以及先中文解释、再给英文答题表述的可打印 cheatsheet；也支持完整复习包、七步笔记与练习卷。适用于课件精读、零基础复习、考点和易错辨析；纯 PDF 合并拆分、一般问答不使用。
---

# 复习pdf

将课程资料变成能学习、能查证、能打印的复习文件。一个入口处理逐页教学、考场资料、完整复习与练习卷，无需串联多个技能。第三方素材的许可见 [sources.md](references/sources.md)。

## 默认选择与模式

根据用户请求直接推断，无需为已有合理默认值打断任务：

| 请求 | 模式 | 默认交付 |
| --- | --- | --- |
| 复习 PDF 和 cheatsheet、按之前方式准备学习与考场两册 | `study-pack` | 逐页中文精讲 PDF + 可打印考场重点 PDF；可编辑源文件与覆盖报告 |
| 每页课件都解释、上面原课件下面讲解 | `slide-walkthrough` | 每张原课件对应一张竖版讲解页；完整中文精讲与来源映射 |
| 打印带进考场、详细 cheatsheet、考场重点复习资料 | `exam-reference` | 中文机制、例子、易错点之后给英文核心表述与概念题短答；印刷目录和术语索引 |
| 完整复习、期末复习、多份讲义、未指定规模的复习资料、三册或课程图 | `full` | 完整复习、速查、易错点三套源文件与 PDF；课程图；覆盖报告 |
| 总结这个课件、考点总结、简短速查、极简 cheatsheet | `summary` | `summary.tex` 和 `summary.pdf`；覆盖报告 |
| 系统学习、七步笔记、章节笔记 | `notes` | `notes.tex` 和 `notes.pdf`；覆盖报告 |
| 真题整理、冲刺练习 | `practice` | `practice.tex/pdf` 与独立 `practice-solutions.tex/pdf`；覆盖报告 |

请求“准备复习 PDF 和 cheatsheet”或明确需要学习与考场两册时，默认采用 `study-pack` 两册流程；只请求某一册则只做该册。使用 `study-pack`、`slide-walkthrough` 或 `exam-reference` 前，读 [study-and-exam-pack.md](references/study-and-exam-pack.md)。Cheatsheet 不自动等于一页，按明确页限和可读性决定篇幅；不把课程实例的页数或考试规则写成通用要求。

页数限制本身不改变语言组织：请求中文理解与英文答题的考场资料，即使限两页也采用 `exam-reference`，在限页内安排内容。

用户明确要求的单个产物或章节范围优先，不强制扩展为完整套装。`notes` 可按明确请求适配考研、考公、科研、项目或竞赛；结构见 [note-modes.md](references/note-modes.md)，不默认扩展普通课程复习的范围。

默认参数：`language=auto`、`depth=comprehensive`、`format=latex`、单栏可读排版。支持 `language=auto|zh|en|bilingual`、`depth=concise|comprehensive|deep`、`format=latex|typst|markdown`。`auto` 为中文解释并保留英文术语、定义与考试原文；明确要求跟随课件时才跟随原语言。公式符号、定理名与标准缩写保留。只在请求影响实质内容且无法推断时澄清。

语言按成品分别决定：逐页精讲默认中文教学，保留必要英文术语而不附整段英文复述；考场重点册默认每个考点先中文解释，再给可用于考试的英文表述。明确的语言要求始终优先，不把一种成品的双语要求套到另一种。

默认必须生成 PDF 并保留可编辑源文件。用户选择 Typst 时保留 `.typ`，明确选择 Markdown 或仅聊天时尊重选择，不强制 PDF。语言细则见 [bilingual-writing.md](references/bilingual-writing.md)。

## 输入、文件与环境

1. 登记全部输入：PDF、PPTX、教材、Revision、syllabus、作业、Quiz、往年题、答案；记录角色、讲次、页数、语言及授课顺序依据。接受逐页 OCR/提取文本；没有原件时披露视觉核验限制，不声称已看过原页。
2. 优先遵从用户和当前宿主规定的输出路径；否则在当前工作目录的 `outputs/复习pdf-<课程或源文件名>/` 放成品，`work/复习pdf-<课程或源文件名>/` 放提取文本、逐段笔记、图片和编译中间文件。先建目录，避免生成内容散落在原资料旁。
3. 使用可用的 PDF/PPTX 读取与渲染工具；宿主提供 PDF 转 Markdown 流程时先转换以便检索，同时保留页码映射，公式与图形仍需看原页。允许使用格式专用技能，不继承上游互斥的技能白名单。
4. 提前检查中文字体与 PDF 编译方式。优先 XeLaTeX；可用宿主内置 LaTeX 编译器。Typst 为用户选择或缺少 LaTeX 时可行的替代；报告替代与实际验证结果。若均不可用，保存源文件、继续可做的核验并准确报告 PDF 未完成，不能把草稿说成已完成 PDF。

## 先全局理解，再分段精读

先浏览全部资料，找出讲次、章节边界、概念依赖、公式密集区和考核依据，再建立涵盖所有页的分段图。不能因为文档长而只处理前面几章。

- 主复习正文按 syllabus 明确顺序、讲义内部编号、日期、依赖声明、文件名的优先顺序确定授课顺序；含糊处记录依据与不确定性。
- 在各讲内保留原页顺序；章节笔记的七步结构用于相应知识模块内，不能为套模板重排主复习的讲义。
- 按独立章节/主题分段，不拆开跨页推导、证明或连续例题。每段先保存笔记再全局合并，避免一次性压缩整本课件。
- 每段记录：段编号、源文件和页范围、核心考点、公式及条件、中文与英文概念、代表例题、解题技巧、易错点、需要重绘的图、覆盖疑问。
- 支持并适合委派时，可并行处理独立段，并用不同于写作者的核验者检查合稿；否则顺序处理后单独回到原资料做核验。不要声称独立代理审查已经发生而实际没有执行。

## 来源与覆盖

在确定重点前读 [source-and-priority.md](references/source-and-priority.md)。优先读 Revision、syllabus，再读题目证据；将考试判断标为 `Explicit`（明确说明）、`Observed`（题目中反复出现）、`Inferred`（推断），不可混为教师确认。

为每一页/幻灯片建立 `coverage.csv`，字段如下：

`source_id,lecture_id,page_or_slide,topic,concept_id,importance,disposition,summary_location,explanation_depth,visual_check,citation,notes`

`disposition` 仅用 `covered|duplicate|administrative|blank|uncertain`。跳过重复/行政/空白页必须有理由；`uncertain` 阻止完成声明。正文用 `[Lecture 04, p.17]`、`[Quiz 2, Q3]` 等紧密引用，多来源综合需分别引用。缺失页码不可编造。

运行随附 `scripts/validate_coverage.py <coverage.csv>`。默认检查已给记录的格式、重复键与必要字段；添加 `--inventory inventory.json`（源 ID 到真实页数的 JSON 映射）可额外检查完全缺失、越界和未知来源页。不传 inventory 时不得声称已验证完整覆盖。脚本不验证公式、图形或解释质量，这些仍须回源核对。

## 写作与图解

完整模式使用 [output-schemas.md](references/output-schemas.md) 的结构。核心知识点包含：定义、直觉/用途、机制/推导、前提与边界、例题/应用、易错辨析、引用。Revision 点名的内容和重要概念必须解释充分，不能只出现标题。

- `summary` 保留全范围的考点、公式条件、英语术语、代表题型与技巧，使用清晰短句；压缩深度不能变成省略后半本课件。
- `notes` 采用概念引入 → 核心公式 → 方法速通 → 典型示例 → 真题/实战 → 巩固练习 → 总结复盘。没有真题时写“自编练习”，不能编造学校、年份或题号。
- `practice` 按有证据的题型/考点组织，题目留答题空间，答案另册；可按题型重排，但保留到原讲义的索引。
- 公式必须定义符号与适用条件；图表解释坐标、表头、图例与结论。仅在有助理解时用 TikZ/pgfplots 或 Typst 原生图解，不加入装饰图。
- 渲染并核对涉及公式、矩阵、下标、箭头、图例、表格关系、OCR 异常或空间布局的源页。重绘不了的图保留不确定性，不能凭空补全。
- 使用语义配色、公式框、例题框、练习留白；可用模板见 [note-modes.md](references/note-modes.md)。复制模板到任务目录后编辑，替换演示作者、机构、课程、日期等内容，勿将模板占位符带入成品。

## 完整复习包与模拟题

`full` 默认生成：

- `final-review.tex/pdf`：按授课与源页顺序的完整讲解。
- `quick-reference.tex/pdf`：定义/公式、符号、条件、用途、常见陷阱、来源。
- `mistakes-and-distinctions.tex/pdf`：易混概念、反例、无效捷径与判断提示。
- `course-map.json`、`course-map.mmd`：先以 JSON 作为唯一结构源，再导出 Mermaid，并将一致的图嵌入主 PDF。
- `coverage.csv`、`coverage-report.md`：记录来源、页覆盖、重点覆盖、核验和编译证据。

本地 Mermaid 不可用时，从相同 JSON 生成 LaTeX/Typst 原生层级图，保留 Mermaid 源码；远程渲染会上传课程结构，仅在用户明确同意时使用。

完整模式有足够考核资料或用户明确要求模拟题时，读 [mock-exam.md](references/mock-exam.md)，先建 `mock-exam-blueprint.md` 再编写 `mock-exam.tex/pdf` 和独立 `mock-exam-solutions.tex/pdf`。其他模式仅在用户要求时附加模拟卷。

题型与权重依次依据 Revision/syllabus、往年题、Quiz/作业、课堂例题。优先原创变式，模拟时长/分数必须标明为设计假设。题目册无答案和泄题引用；答案册含推导、评分点、常错、难度、概念与来源。验证答案可解、单选唯一、计算正确、分数相加一致、题目与课程吻合。

## 核验、编译与完成

按 [quality-gates.md](references/quality-gates.md) 检查适用门槛。模式适配：`study-pack` 只要求约定的学习册和考场册；`slide-walkthrough`、`exam-reference`、summary/notes/practice 不要求额外生成完整模式的三册或课程图；Typst/Markdown 按所选格式核验。只把真正不适用的项目记为 N/A，并说明理由。

核验要回到原资料、逐页台账与分段图，不能只读合稿。记录 `APPROVED|APPROVED_WITH_NOTES|REJECTED`、覆盖发现、准确性/样式发现、缺失与待改项；修正待改项后重新核验。

LaTeX 按需要多遍编译以稳定目录和交叉引用；Typst 通常单遍。所有实际要求的 PDF 均须编译成功，再渲染逐页检查中文缺字、溢出、截断、重叠、公式、图表与留白。文件存在不等于编译成功，编译成功也不等于内容和排版合格。

最终先给成品链接，再简述产物和已验证覆盖数量、排除项及尚存限制。仅在文件确实已落盘、适用门槛通过时宣称完成；未编译、未视觉核验、无原页等情形必须据实标明。
