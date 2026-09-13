from __future__ import annotations
import json, re, unicodedata
from pathlib import Path
from .model import PlanLesson, OwnedTarget, LessonCopy

LESSON_RE = re.compile(r'^###\s+(\d{2})\.\s+(.+?)\s*$')
SECTION_RE = re.compile(r'^##\s+Section\s+(\d{2})\s+—\s+(.+?)\s*$')
INTENT_PREFIX = '**Что будет:**'
TARGET_PREFIX = '**Новые слова/фразы:**'


def normalize_sk(text: str) -> str:
    text = unicodedata.normalize('NFC', text).strip().lower()
    text = re.sub(r'[.!?]+$', '', text)
    return re.sub(r'\s+', ' ', text)


def load_a1_owned(path: Path) -> set[str]:
    owned: set[str] = set()
    for p in sorted(path.glob('a1-s*-l*.json')):
        doc = json.loads(p.read_text(encoding='utf-8'))
        for lesson in doc.get('lessons', []):
            for w in lesson.get('words', []):
                sk = w.get('sk')
                if isinstance(sk, str) and sk.strip():
                    owned.add(normalize_sk(sk))
    return owned


def parse_a2_plan(path: Path) -> list[PlanLesson]:
    lines = path.read_text(encoding='utf-8').splitlines()
    current_section: int | None = None
    lessons: list[PlanLesson] = []
    i = 0
    while i < len(lines):
        sm = SECTION_RE.match(lines[i])
        if sm:
            current_section = int(sm.group(1)); i += 1; continue
        lm = LESSON_RE.match(lines[i])
        if lm:
            if current_section is None:
                raise AssertionError(f'lesson before section at line {i+1}')
            order = int(lm.group(1)); title = lm.group(2).strip()
            intent = None; targets = None
            j = i + 1
            while j < len(lines) and not LESSON_RE.match(lines[j]) and not SECTION_RE.match(lines[j]):
                line = lines[j].strip()
                if line.startswith(INTENT_PREFIX): intent = line[len(INTENT_PREFIX):].strip()
                if line.startswith(TARGET_PREFIX):
                    raw = line[len(TARGET_PREFIX):].strip()
                    protected = {
                        'kvôli tomu, že': 'kvôli tomu§ že',
                        'myslím, že': 'myslím§ že',
                    }
                    for a,b in protected.items(): raw = raw.replace(a,b)
                    targets = tuple(x.strip().replace('§', ',') for x in raw.split(',') if x.strip())
                j += 1
            if not intent or not targets:
                raise AssertionError(f'incomplete A2 map entry {order}: {title}')
            lessons.append(PlanLesson(current_section, order, f'a2-s{current_section:02d}-l{order:02d}', title, intent, targets))
            i = j; continue
        i += 1
    assert len(lessons) == 90, f'expected 90 A2 lessons, got {len(lessons)}'
    assert [x.order for x in lessons] == list(range(1,91)), 'A2 orders are not 1..90'
    counts: dict[int,int] = {}
    for x in lessons: counts[x.section] = counts.get(x.section,0)+1
    assert counts == {i:6 for i in range(1,16)}, f'bad section distribution: {counts}'
    return lessons


def classify_targets(plan_lesson: PlanLesson, copy: LessonCopy, a1_owned: set[str], prior_a2_owned: set[str]) -> list[OwnedTarget]:
    assert len(plan_lesson.mapped_targets) == len(copy.target_uk), (
        plan_lesson.lesson_id, len(plan_lesson.mapped_targets), len(copy.target_uk))
    out: list[OwnedTarget] = []
    for sk, uk in zip(plan_lesson.mapped_targets, copy.target_uk):
        norm = normalize_sk(sk)
        if plan_lesson.section == 15 and (norm in a1_owned or norm in prior_a2_owned): status = 'MASTERY'
        elif norm in prior_a2_owned: status = 'TRANSFER'
        elif norm in a1_owned: status = 'REVIEW'
        else: status = 'NEW'
        out.append(OwnedTarget(sk=sk, uk=uk, status=status))
    return out
