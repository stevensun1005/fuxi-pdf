"""Validate discoverability, UI metadata and local Markdown links."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    text = (root / 'SKILL.md').read_text(encoding='utf-8')
    assert text.startswith('---\n'), 'SKILL.md needs YAML frontmatter'
    meta = yaml.safe_load(text.split('---', 2)[1])
    assert meta['name'] == 'fuxi-pdf'
    assert isinstance(meta['description'], str) and meta['description'].strip()
    ui = yaml.safe_load((root / 'agents/openai.yaml').read_text(encoding='utf-8'))
    assert ui['interface']['display_name'] == '复习pdf'
    assert 25 <= len(ui['interface']['short_description']) <= 64
    assert '$fuxi-pdf' in ui['interface']['default_prompt']
    assert ui['policy']['allow_implicit_invocation'] is True
    for path in root.rglob('*.md'):
        if '.git' in path.parts:
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            assert (path.parent / target.split('#')[0]).exists(), f'{path}: missing {target}'
    for name in ['LICENSE', 'licenses/NovaForge-LICENSE.txt', 'licenses/summarize-slides-LICENSE.txt']:
        assert (root / name).is_file(), name
    print('PASS: skill metadata, local links and attribution files')


if __name__ == '__main__':
    check()
