<p align="center">
  <img src="docs/assets/banner.svg" alt="fuxi-pdf: slide walkthroughs, compact formula sheets and detailed exam references" width="100%">
</p>

<h1 align="center">fuxi-pdf · 复习pdf</h1>

<p align="center"><strong>Understand the slides. Turn the essentials into printable references.</strong></p>

<p align="center">
  <a href="https://github.com/stevensun1005/fuxi-pdf/actions/workflows/validate.yml"><img src="https://github.com/stevensun1005/fuxi-pdf/actions/workflows/validate.yml/badge.svg" alt="Validate skill"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/skill_%26_code-MIT-26705d" alt="Skill and code: MIT"></a>
  <a href="references/sources.md"><img src="https://img.shields.io/badge/course_demos-CC_BY--NC--SA_4.0-26705d" alt="Course demos: CC BY-NC-SA 4.0"></a>
  <img src="https://img.shields.io/badge/built_for-Codex-173e36" alt="Built for Codex">
</p>

<p align="center">
  <a href="README.md">中文</a> ·
  <a href="#see-the-actual-results">See results</a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#requests-you-can-copy">Copy a request</a> ·
  <a href="#frequently-asked-questions">FAQ</a> ·
  <a href="SKILL.md">Skill instructions</a>
</p>

**fuxi-pdf is a Codex skill** that turns supplied slides, textbooks and exam instructions into teaching PDFs, compact cheatsheets or detailed study references. It connects original pages, explanations, formula conditions and sources, and keeps editable files for revision.

Use it to learn a course from scratch, organize a semester of material, understand English-language lectures, or prepare references within a paper limit. **You choose the page budget and language balance:** English-first, more Chinese explanation, or full Chinese–English.

## Three outputs for three needs

| What you need | Output | Structure and content |
| --- | --- | --- |
| Understand what every slide means | **Slide walkthrough** | Original slide above a structured explanation; mechanisms, diagrams, examples and pitfalls |
| Fit formulas and methods into a fixed budget | **Compact cheatsheet** | Multiple columns, narrow margins and three semantic colors; formulas, conditions, steps and short examples |
| Review systematically and find answers quickly | **Detailed exam reference** | Concept chapters with reasoning, comparisons, examples and answer wording; longer booklets can include contents and indexes |

Request one output or combine a study guide with a reference. All three support your language choice; the examples do not impose one language profile on everyone.

## See the actual results

### ① One-page formula sheet: a first-half linear algebra selection

**21 public lecture summaries → 20 reference topics → one landscape Letter face.**

Based on **MIT OpenCourseWare 18.06SC Linear Algebra (Fall 2011, Gilbert Strang)**: systems, elimination, subspaces, projections, least squares, QR and determinants. This example selects **English-first wording with just four Chinese clarifications**, four columns, black/blue/red, 3.5 mm margins and no footer.

[**Open the one-page PDF**](examples/compact-math/cheatsheet.pdf) · [Editable source and reproduction](examples/compact-math/README.md) · [Source manifest](examples/compact-math/sources.json) · [Validation record](examples/compact-math/validation.md)

![Actual English-first linear algebra cheatsheet preview](examples/compact-math/preview-english.png)

This approximates a half-semester **topic selection**, not an official midterm scope. Full proofs and most original examples are explicitly omitted and logged. The sources contain 85 PDF pages, including 21 attribution/license pages.

### ② Walkthrough and detailed reference: two treatments of one complete lecture

A separate example uses **MIT OCW 6.033 Computer System Engineering (Spring 2018, Katrina LaCurts), Lecture 14**. Its 15 source pages become a **15-page Chinese walkthrough** and a **10-page Chinese–English reference booklet**.

<details>
<summary><strong>Expand previews: original slide above explanation, plus a detailed bilingual reference</strong></summary>

| Walkthrough · source page 12: RAID 4 | Unlimited-budget bilingual booklet · page 3: availability |
| --- | --- |
| ![Actual slide walkthrough preview](docs/assets/walkthrough.png) | ![Actual detailed bilingual reference preview](docs/assets/exam-reference.png) |
| [Open the 15-page walkthrough](examples/output/slide-walkthrough.pdf) | [Open the 10-page reference](examples/output/exam-reference.pdf) |

</details>

The booklet includes seven concept chapters, fourteen original English short answers, printed contents, an English index and a source map. It demonstrates a different density and language choice from the one-page sheet above.

The public slide adaptation preserves lecture order. A vendor image on original page 9 is excluded from the OCW license, so that page is replaced with a clearly labeled text-only adaptation; the other fourteen pages retain their original visuals. See the [demo guide](examples/README.md) and [course-material license](licenses/MIT-OCW-demo-LICENSE.md) for provenance and changes.

## Quick start

### 1. Install the skill

You need Git and a Codex environment that supports local skills. The repository root is the skill; keep its directory name `fuxi-pdf`.

**macOS / Linux**

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/stevensun1005/fuxi-pdf.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/fuxi-pdf"
```

**Windows PowerShell**

```powershell
$skillRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
git clone https://github.com/stevensun1005/fuxi-pdf.git (Join-Path $skillRoot 'fuxi-pdf')
```

If the directory already exists, back up your changes before updating. The display name is **复习pdf**; invoke it with **`$fuxi-pdf`**. If a new installation is not available in the current session, start a fresh session.

### 2. Supply your material

Attach PDF/PPTX slides, textbook material or extracted text. Include the syllabus, revision guidance, exam scope, paper rules, quizzes or past papers when available, so ordering and priorities have evidence.

PDF generation also requires reading, compilation and rendering tools, plus suitable fonts in the host environment. The skill checks availability; LaTeX is preferred, Typst is an alternative, and explicit Markdown requests are respected. **Installing this skill does not install a complete PDF toolchain.**

### 3. Describe the result

```text
Use $fuxi-pdf to turn these slides into a study PDF and a cheatsheet.
```

You do not need to remember mode names. Missing page and language choices are asked first; existing explicit answers are reused. Specify everything up front to begin directly.

## Choose pages and language independently

| Choice | Options | Behavior |
| --- | --- | --- |
| **Cheatsheet page budget** | One page / two pages / unlimited, or another explicit budget | One page means one printed face; a double-sided sheet has two pages. Keep essential conditions and document tradeoffs within the limit. |
| **Language balance** | English-first / more Chinese explanation / full Chinese–English | The document's balance is not inferred from the chat language, source language or exam language. |

If both choices are missing, ask them together. If only one is missing, ask only that one. Reuse clear answers. The study guide and cheatsheet can use different languages: **one page does not require English, and unlimited pages do not require bilingual text.**

A one-page formula sheet normally uses landscape A4/Letter, multiple columns, narrow margins and black/blue/red to distinguish conditions, core formulas and important pitfalls. Explicit style references and exam rules take precedence.

## Requests you can copy

### One page, English-first

```text
Use $fuxi-pdf to make a one-page landscape Letter linear algebra cheatsheet.
Use English headings, formula conditions, methods and answer cues.
Add Chinese only for complicated or easily confused points.
Use multiple columns, narrow margins, black/blue/red and no footer.
Keep necessary formula conditions and source references.
```

### Two pages, more Chinese explanation

```text
Use $fuxi-pdf to make a two-page A4 cheatsheet with more Chinese explanation.
Keep standard English terminology, formulas and concise English answer cues.
Prioritize mechanisms, conditions for choosing a method and common mistakes.
Do not repeat every sentence in both languages.
```

### Learn from scratch, then prepare an unlimited bilingual reference

```text
Use $fuxi-pdf to prepare a study guide and an exam reference from scratch.
Study guide: original slide above a Chinese explanation; explain every page
and include concrete examples.
Reference: no page limit, full Chinese–English; explain the mechanism in
Chinese first, then give English wording suitable for exam answers.
Keep editable sources, source-page references and a coverage ledger.
```

### Explain every slide, with no additional booklet

```text
Use $fuxi-pdf to explain this deck slide by slide. Only make the study guide.
Explain each diagram, formula, code sample and example in Chinese.
Keep English terminology; no English restatement is needed.
```

## Why sources and validation records matter

**Every source page gets a disposition.** Pages are marked covered, duplicate, administrative, blank or unresolved. Constrained references log compression and omissions; “covered” does not mean every detail fits on one sheet.

**Formulas keep their conditions.** Preserve symbols, units, assumptions and boundaries. Check diagrams and derivations against the source; label original examples and practice questions.

**The PDF gets inspected.** Reopen and render the compiled result to check Chinese glyphs, fractions, subscripts, tables, overlap, clipping and print dimensions. File existence and passing tests do not replace visual and content review.

**Priorities have an evidence level.** Distinguish explicit instructor guidance, patterns observed in assessments and inferred emphasis. Original short answers are not official solutions or exam predictions.

See the [validation record](docs/validation.md) for checks actually performed on this repository. Demonstrations use public courses, not users' private course files.

## More ways to organize material

| Mode | Purpose |
| --- | --- |
| `study-pack` | Study guide + exam reference, checked against shared sources, with separate language choices |
| `slide-walkthrough` | Original slide above its explanation, in source order |
| `exam-reference` | Concept-based printable reference with the selected length and language |
| `summary` | Concise summary, quick reference or explicitly page-limited cheatsheet |
| `full` | Full review, quick-reference and pitfalls PDFs, plus a course map and coverage report |
| `notes` | Seven-step notes: introduce concepts, formulas, methods, examples, exercises and reflection |
| `practice` | Exercises and a separate answer booklet; mock exams on request with sufficient assessment evidence |

Choose the mode that fits the request. Asking for one cheatsheet does not automatically expand into a complete study package.

## Deliverables

Receive the requested PDFs, editable sources and source records. For example, a study-guide-plus-reference request can produce:

```text
outputs/复习pdf-course/
├── slide-walkthrough.pdf     # Slide-by-slide teaching
├── exam-reference.pdf        # Printable reference
├── … .tex / .typ             # Corresponding editable sources
├── coverage.csv             # Source pages mapped to topics/output locations
└── coverage-report.md        # Compression, exclusions, checks and limits
```

Names and formats can be adjusted. Screen-oriented walkthroughs may use extended pages; print references use standard paper, with that distinction stated clearly. See [SKILL.md](SKILL.md) and the [output schemas](references/output-schemas.md).

## Frequently asked questions

<details>
<summary><strong>Is this an app, a hosted service or a skill?</strong></summary>

It is an instruction, template and asset package for Codex. The host agent handles understanding and writing. Repository scripts perform specific checks and demo builds; there is no standalone CLI that automatically summarizes any course offline.

</details>

<details>
<summary><strong>What if everything will not fit on one page?</strong></summary>

Allocate space across the requested scope, retain evidence-backed priorities, formula conditions and useful methods, and state omissions. Do not silently add a back side, exceed the budget, truncate formulas or shrink text indefinitely. A separate study guide can hold the full explanations.

</details>

<details>
<summary><strong>Can I choose all English, more Chinese, or different languages for two outputs?</strong></summary>

Yes. Missing choices are asked first; explicit requirements are followed. The English formula sheet, Chinese walkthrough and bilingual booklet demonstrate selected profiles, not fixed language restrictions.

</details>

<details>
<summary><strong>Can it handle scanned or formula-heavy material?</strong></summary>

That depends on the host's OCR, reading and rendering tools. Text extraction helps retrieval, but formulas, diagrams and spatial relationships still require original-page inspection. Unreliably recognized content stays unresolved rather than being invented. Without the originals, the skill does not claim original-page visual verification.

</details>

<details>
<summary><strong>Are these official answers, and may I bring them into an exam?</strong></summary>

The demos are independently written study materials, not official answers. Permission, page count and single-/double-sided rules come from your exam instructions. Requesting an unlimited reference does not establish that the exam allows one.

</details>

## Development and validation

Python dependencies support repository development, demo inspection and validation; they are not a complete PDF compilation environment.

```sh
python -m pip install -r requirements-dev.txt
python tools/check_package.py
python -m unittest discover -s tests -v
python scripts/validate_coverage.py examples/coverage.csv --inventory examples/inventory.json
python scripts/validate_coverage.py examples/compact-math/coverage.csv --inventory examples/compact-math/inventory.json
```

[GitHub Actions](https://github.com/stevensun1005/fuxi-pdf/actions/workflows/validate.yml) checks metadata, local links, coverage scripts and demo PDFs on Python 3.11 and 3.13. Given an inventory of actual page counts, the coverage validator detects missing pages, unknown sources and out-of-range pages. Without an inventory, it checks existing CSV rows only and does not establish complete coverage.

## Feedback and contributions

Use [Issues](https://github.com/stevensun1005/fuxi-pdf/issues) for layout problems, reproduction failures, formula corrections or feedback; [pull requests](https://github.com/stevensun1005/fuxi-pdf/pulls) are welcome. Include your operating system, output type, page/language choices, reproduction steps and a minimal example that can be shared publicly.

Keep Chinese and English documentation aligned. When changing a demo, update its source, PDF, preview and provenance/license notices together, and inspect the final render. See [SKILL.md](SKILL.md), [references/](references/) and [tests/](tests/) for structure.

If this helps you make sense of a course, a Star can help others find it.

## Licensing and course attribution

| Content | License |
| --- | --- |
| Skill instructions and build/validation code | [MIT License](LICENSE) |
| MIT 6.033 public slide adaptation, teaching content, derived PDFs and previews | [CC BY-NC-SA 4.0 · attribution and changes](licenses/MIT-OCW-demo-LICENSE.md) |
| MIT 18.06SC mathematics cheatsheet, source and preview | [CC BY-NC-SA 4.0 · attribution and changes](licenses/MIT-OCW-math-LICENSE.md) |

The repository's MIT code license does not relicense third-party course material. This project is not affiliated with or endorsed by MIT or the instructors. Font files are not distributed. See the [license notes](references/sources.md) for complete material notices.
