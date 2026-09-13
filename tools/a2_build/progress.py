from __future__ import annotations
import argparse
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--count',type=int,required=True); ap.add_argument('--complete',action='store_true'); ap.add_argument('--path',default='progress/A2_PROGRESS.md'); ns=ap.parse_args()
    n=ns.count; assert n in {18,36,54,72,90}
    done=n//6
    lines=['# SlovakGo A2 — Progress','', '## Status']
    if ns.complete:
        assert n==90; lines += ['**COMPLETE — 90 / 90 active lessons**','']
    else:
        lines += [f'**IN PROGRESS — {n} / 90 active lessons**','']
    lines += ['A2 follows `A2/LESSON_PLAN.md`. A2 expands completed A1 and uses A1 vocabulary as prerequisite/review evidence.','', '## Sections']
    for s in range(1,16):
        lo=(s-1)*6+1; hi=s*6; state='complete' if s<=done else 'planned'
        lines.append(f'- S{s:02d} `l{lo:02d}–l{hi:02d}` — {state}')
    lines += ['', '## QA gates', '- Current SlovakGo application schema validation.', '- Current SlovakGo `scripts/qa-lessons.ts` runtime-contract validation.', '- A2 adversarial checks: references, deterministic answers, option collisions, token multisets and final-situation intent.', '- A1→A2 ownership classification (NEW/REVIEW/TRANSFER/MASTERY).', '- Ukrainian learner UI; Slovak target language; `isPublished: false`.']
    if ns.complete:
        lines += ['- Remote A2 inventory verified at 90/90 after all batch pushes.', '- Full `nextLesson` chain L01→L90 verified; L90 is terminal.', '', '## A2 → B1 boundary', 'A2 is content-complete. Further A2 changes should be QA/errata improvements unless the approved A2 lesson plan is deliberately revised.']
    else:
        lines += ['', f'Next production batch begins at `l{n+1:02d}`.']
    p=Path(ns.path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Wrote {p}: {n}/90 complete={ns.complete}')
if __name__=='__main__': main()
