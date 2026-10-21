<p align="center"><img src="docs/assets/banner.svg" alt="fuxi-pdf — understand the slides, prepare the answers" width="100%"></p>

# fuxi-pdf · 复习pdf

**Understand in Chinese. Answer in English.**

[中文说明](README.md) · [Skill instructions](SKILL.md) · [Actual PDF examples](examples/README.md)

A Codex skill that turns supplied slides, textbooks and exam information into source-cited study PDFs. Its main workflow separates two needs:

| Study walkthrough | Printable exam reference |
| --- | --- |
| Complete original slide above a Chinese explanation | Compact: English-first; unlimited booklet: Chinese explanations then English answers |
| Slide-by-slide, in lecture order | Organized by concepts, conditions and tradeoffs |
| Mechanisms, examples, diagrams and common mistakes | Worked examples, short-answer questions, printed contents and term index |

If a cheatsheet has no explicit page budget, the skill first asks: **one page, two pages, or no page limit?** An existing answer is reused. Words such as "detailed" or "minimal", and attached style references, do not set a page budget. One page means one printed face; a double-sided sheet has two pages.

One-page requests default to a [compact formula-sheet layout](references/compact-cheatsheet.md): landscape standard paper, narrow margins, multiple columns, black explanations, blue formulas and English answer cues, and sparse red warnings. No separate cover, contents or index is added. Two-page requests stay within two pages; the detailed booklet style applies when no page limit is explicitly chosen. Compact formula sheets, including two-page versions, default to English with Chinese only for selected difficult explanations. Only an explicitly unlimited detailed booklet defaults to full Chinese explanations followed by English answers. Explicit language and layout requests take precedence. Screen-oriented extended pages remain separate from print layouts.

Walkthroughs use an engineering-handout style: teal headings, numbered sections, light-gray code or pseudocode blocks, field/state tables, and takeaway panels. Code, data flow and worked traces get structured formatting; conceptual teaching remains readable prose.

## Install

The skill lives at the repository root:

```sh
git clone https://github.com/stevensun1005/fuxi-pdf.git ~/.codex/skills/fuxi-pdf
```

On Windows PowerShell:

```powershell
git clone https://github.com/stevensun1005/fuxi-pdf.git "$env:USERPROFILE\.codex\skills\fuxi-pdf"
```

Back up an existing installation before updating. Invoke `$fuxi-pdf` in a Codex environment that supports local skills. PDF reading, compilation, rendering and suitable Chinese fonts must be available in the host environment; the skill checks these during the task.

## Example request

```text
Use $fuxi-pdf to prepare a study PDF and a printable exam reference
from these lecture slides. Teach from scratch.
For the study PDF, place the original slide above a Chinese explanation.
For the exam reference, explain each concept in Chinese first,
then provide concise English wording and conceptual short answers.
```

For a constrained reference, specify the page budget, paper, sides and answer language. Requesting one artifact does not force a complete bundle.

## Modes

`study-pack` · `slide-walkthrough` · `exam-reference` · `summary` · `full` · `notes` · `practice`

The skill preserves editable sources, source-page references and a coverage ledger. Priorities distinguish explicit instructor statements, observed assessment evidence and inferred study emphasis. Authored practice answers are not presented as official solutions or predictions.

## Inspect the examples

This is an unlimited-length booklet example, not the default density for a one-page cheatsheet.

The demo covers all 15 pages of Katrina LaCurts' MIT OpenCourseWare 6.033, Spring 2018, Lecture 14 and its official companion outline: fault models, fault-tolerance design, availability, MTBF, RAID 1/4/5 and reliability tradeoffs. It includes a [15-page public source adaptation](examples/input/demo-slides.pdf), a [15-page Chinese walkthrough](examples/output/slide-walkthrough.pdf), and a [10-page Letter cheatsheet](examples/output/exam-reference.pdf) with seven concept chapters, fourteen original English short-answer examples, a printed contents page, an English index and a source map.

The vendor image on original page 9 is explicitly excluded from the OCW license, so that page is replaced with a clearly labeled text-only adaptation; the other fourteen pages retain their original visuals. The complete unmodified source is available from the [official resource](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/mit6_033s18lec14/). These are independently written learning materials, not official answers. Previews show walkthrough page 12 and cheatsheet page 3. See [reproduction instructions](examples/README.md).

## One-page compact mathematics example

A separate example condenses a first-half topic selection from **MIT OCW 18.06SC Linear Algebra (Fall 2011, Gilbert Strang)** into one landscape Letter face: 21 lecture summaries, 85 source pages, and 20 compact sections covering systems, subspaces, orthogonality, least squares and determinants. It uses four columns and semantic black/blue/red, with English-first headings, formulas, conditions and solution steps; brief Chinese notes clarify only selected difficult points.

[One-page PDF](examples/compact-math/cheatsheet.pdf) · [Editable source, provenance and reproduction](examples/compact-math/README.md)

![Compact mathematics preview](examples/compact-math/preview.png)

This approximates a half-semester topic range, not an official midterm scope. Proofs and most worked examples are omitted explicitly. It demonstrates a different density from the ten-page detailed computer-systems booklet.

## Validate

The walkthrough uses A4-width extended pages to keep each slide with its complete explanation. The exam reference uses standard Letter pages for printing.

```sh
python -m pip install -r requirements-dev.txt
python tools/check_package.py
python -m unittest discover -s tests -v
python scripts/validate_coverage.py examples/coverage.csv --inventory examples/inventory.json
```

Inventory format: `{"Lecture01": 30}`. Without an inventory, the validator checks supplied rows only. With one, it detects missing pages, out-of-range pages and unknown sources. It does not establish content correctness or visual quality.

GitHub Actions runs package and test checks on Python 3.11 and 3.13. This is an agent skill and template package, not a standalone automatic course-generation CLI.

## License

Skill and build code are [MIT licensed](LICENSE). The real lecture public adaptation, demo teaching content, derived PDFs and their previews are [CC BY-NC-SA 4.0](licenses/MIT-OCW-demo-LICENSE.md). The compact linear-algebra adaptation has its own [CC BY-NC-SA 4.0 notice](licenses/MIT-OCW-math-LICENSE.md). Other copyright and license notices are documented in [license notes](references/sources.md).
