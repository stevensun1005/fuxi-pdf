<p align="center"><img src="docs/assets/banner.svg" alt="复习pdf：把课件讲明白，把答案写清楚" width="100%"></p>

<p align="center">
  <a href="https://github.com/stevensun1005/fuxi-pdf/actions/workflows/validate.yml"><img src="https://github.com/stevensun1005/fuxi-pdf/actions/workflows/validate.yml/badge.svg" alt="Validate skill"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-26705d" alt="Code: MIT"></a>
  <a href="licenses/MIT-OCW-demo-LICENSE.md"><img src="https://img.shields.io/badge/demo-CC_BY--NC--SA_4.0-26705d" alt="Demo: CC BY-NC-SA 4.0"></a>
  <img src="https://img.shields.io/badge/languages-中文%20%2B%20English-26705d" alt="中文与英文">
</p>

<p align="center"><b>从“这页在讲什么”，到“考试该怎么回答”。</b><br><a href="README.en.md">English</a> · <a href="SKILL.md">技能入口</a> · <a href="examples/README.md">真实 PDF 演示</a></p>

## 两种用途，两本资料

**复习pdf** 是一个面向 Codex 的学习资料技能。它读取你提供的课件、教材和考试说明，整理成有来源、有例子、经过核验的 PDF；尤其适合需要从零理解英文课程，再用英文参加考试的学习者。

| | 逐页精讲 · 学习册 | 考场重点 · Cheatsheet |
| --- | --- | --- |
| 读者要解决的问题 | 这张课件具体讲了什么？ | 这个概念怎样用英文答题？ |
| 结构 | 上方完整原课件，下方中文分节讲解 | 中文机制、例子和易错点之后，给英文表述与短答 |
| 组织 | 按讲次与原页顺序，逐页保留 | 合并重复，按考点检索，覆盖全范围实质主题 |
| 版式 | 竖版阅读，原页与解释明确对应 | 标准纸张、灰度清楚、目录和术语索引 |
| 语言 | 中文教学，保留必要英文术语 | 先理解中文，再练习英文回答 |

Cheatsheet 不默认等于一页。考试规定两页，就按两页设计；允许详细纸质资料时，优先保证内容和字号可读。它也不会把一份屏幕长页 PDF 直接当成打印册。

## 看一眼成品

以下演示使用 **MIT OpenCourseWare 6.033（Spring 2018，Katrina LaCurts）第 14 讲的真实课件第 11–13 页**，依次解释 RAID 1、RAID 4 与 RAID 5。两册各 3 页；下图预览第 2 页的 RAID 4。选页保留完整原图，讲解由本项目编写，属于节选演示，不代表整讲覆盖或官方答案。

| 逐页中文精讲 | 可打印考场重点册 |
| --- | --- |
| ![逐页精讲实际预览](docs/assets/walkthrough.png) | ![考场重点册实际预览](docs/assets/exam-reference.png) |
| [打开学习册 PDF](examples/output/slide-walkthrough.pdf) | [打开考场册 PDF](examples/output/exam-reference.pdf) |

[真实课件节选](examples/input/demo-slides.pdf) · [官方课件来源](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/mit6_033s18lec14/) · [演示说明与复现](examples/README.md)

## 安装

将本仓库放进 Codex 的技能目录，目录名保留 `fuxi-pdf`。仓库根目录就是技能入口，无需再找子目录。

**macOS / Linux**

```sh
git clone https://github.com/stevensun1005/fuxi-pdf.git ~/.codex/skills/fuxi-pdf
```

**Windows PowerShell**

```powershell
git clone https://github.com/stevensun1005/fuxi-pdf.git "$env:USERPROFILE\.codex\skills\fuxi-pdf"
```

已有同名安装时先备份，再更新。之后在支持本地技能的 Codex 会话中使用 `$fuxi-pdf`；界面显示名是“复习pdf”。生成 PDF 需要宿主可用的读取、编译和渲染能力，字体与后端会在实际任务中检查。

## 直接这样说

**学习和考场两册一起准备**

```text
使用 $fuxi-pdf，根据这些课件准备复习 PDF 和 cheatsheet。
我没上过课，需要从零讲清楚。
学习册每页上方放原课件，下方中文解释。
考场册详细一点，先中文解释，再给英文答题表述。
```

**只要逐页精讲**

```text
使用 $fuxi-pdf，解释这份课件的每一页。
上面原课件，下面中文分节讲解，加具体例子和易错点，不需要英文复述。
```

**只要限页考场资料**

```text
使用 $fuxi-pdf，做一份可打印的考场 cheatsheet。
最多两页 A4、可双面，考试使用英文。
保留公式条件和关键区别，中文帮助理解，英文给简洁答题表述。
```

提供课件，以及已有的 syllabus、Revision、考试规则或真题即可。资料不齐时会说明边界，不编造出题频率、官方答案或成绩保证。

## 支持的模式

| 模式 | 用途 |
| --- | --- |
| `study-pack` | 学习册 + 考场册，同源核验、不同语言组织 |
| `slide-walkthrough` | 原页在上、中文逐页解释在下 |
| `exam-reference` | 详细考点、中文机制、英文短答、打印检索 |
| `summary` | 简短总结或明确限页速查 |
| `full` | 完整复习、速查、易错三册及课程图 |
| `notes` | 七步章节笔记、概念与练习 |
| `practice` | 题目与答案分开的练习卷 |

明确的范围、页数和语言要求优先；只请求一本就不会强制做整套。默认保留 PDF 与可编辑源文件，支持 LaTeX，也可按要求使用 Typst 或 Markdown。

## 怎样避免“看起来做完了”

- **逐页有去向**：每张源页登记为覆盖、重复、行政、空白或未决，不只统计已有记录。
- **解释有条件**：定义、机制、适用条件、例子和反例一起核对，图中的箭头要逐条读。
- **英文能作答**：直接回应概念题，保留决定结论的条件，而非机械翻译整页中文。
- **PDF 真正检查**：实际编译、重开、渲染并查看成品页；自动校验不等于视觉核验。
- **重点有证据**：区分教师明确要求、题目观察和整理推断，不把推测写成教师承诺。

随附脚本可以检查台账。传入真实页数后，还能发现**完全漏记的一页**：

```sh
python scripts/validate_coverage.py examples/coverage.csv --inventory examples/inventory.json
```

`inventory.json` 格式为 `{"Lecture01": 30, "Lecture02": 42}`。不传 inventory 时只检查现有 CSV，不声称完整覆盖。脚本不评判公式或教学质量。

## 开发与验证

```sh
python -m pip install -r requirements-dev.txt
python tools/check_package.py
python -m unittest discover -s tests -v
```

GitHub Actions 在 Python 3.11、3.13 上执行元数据、链接、覆盖脚本与演示 PDF 检查。仓库包含实际演示产物；它是技能与素材包，完整课程的内容生成由宿主代理完成，不是一个离线自动总结 CLI。

本次实际执行的编译与视觉检查范围见 [验证记录](docs/validation.md)。

## 许可

技能与构建代码采用 [MIT License](LICENSE)。真实课件节选、演示讲解与其 PDF/预览采用 [CC BY-NC-SA 4.0](licenses/MIT-OCW-demo-LICENSE.md)。其他素材声明见 [许可说明](references/sources.md)。
