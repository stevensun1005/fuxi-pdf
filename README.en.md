<p align="center"><img src="docs/assets/banner.svg" alt="fuxi-pdf — understand the slides, prepare the answers" width="100%"></p>

# fuxi-pdf · 复习pdf

**Understand in Chinese. Answer in English.**

[中文说明](README.md) · [Skill instructions](SKILL.md) · [Actual PDF examples](examples/README.md)

A Codex skill that turns supplied slides, textbooks and exam information into source-cited study PDFs. Its main workflow separates two needs:

| Study walkthrough | Printable exam reference |
| --- | --- |
| Complete original slide above a Chinese explanation | Chinese explanation followed by usable English answers |
| Slide-by-slide, in lecture order | Organized by concepts, conditions and tradeoffs |
| Mechanisms, examples, diagrams and common mistakes | Worked examples, short-answer questions, printed contents and term index |

A cheatsheet is not automatically one page. Explicit exam limits take precedence. Screen-oriented extended pages are kept separate from standard-paper print layouts.

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

The demo uses three real slides (original pages 11-13) from Katrina LaCurts' MIT OpenCourseWare 6.033, Spring 2018, Lecture 14: RAID 1, RAID 4 and RAID 5. It includes the [source excerpt](examples/input/demo-slides.pdf), a three-page [Chinese walkthrough](examples/output/slide-walkthrough.pdf), and a three-page [printable bilingual reference](examples/output/exam-reference.pdf). Preview images show page 2 (RAID 4). These are independently written educational adaptations of a selected passage, not a full-lecture guide or official answers. See the [official resource](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/mit6_033s18lec14/) and [reproduction instructions](examples/README.md).

## Validate

```sh
python -m pip install -r requirements-dev.txt
python tools/check_package.py
python -m unittest discover -s tests -v
python scripts/validate_coverage.py examples/coverage.csv --inventory examples/inventory.json
```

Inventory format: `{"Lecture01": 30}`. Without an inventory, the validator checks supplied rows only. With one, it detects missing pages, out-of-range pages and unknown sources. It does not establish content correctness or visual quality.

GitHub Actions runs package and test checks on Python 3.11 and 3.13. This is an agent skill and template package, not a standalone automatic course-generation CLI.

## License

Skill and build code are [MIT licensed](LICENSE). The real lecture excerpt, demo teaching content, derived PDFs and their previews are [CC BY-NC-SA 4.0](licenses/MIT-OCW-demo-LICENSE.md). Other copyright and license notices are documented in [license notes](references/sources.md).
