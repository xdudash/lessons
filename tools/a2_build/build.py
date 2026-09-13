from __future__ import annotations
import argparse, json
from pathlib import Path
from .content import COPY
from .ownership import parse_a2_plan, load_a1_owned, normalize_sk, classify_targets
from .generator import write_lessons

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--out',default='lessons/a2'); ap.add_argument('--from',dest='lo',type=int,default=1); ap.add_argument('--to',dest='hi',type=int,default=90); ap.add_argument('--manifest',default='tools/a2_build/ownership-manifest.json'); ns=ap.parse_args()
    root=Path(ns.root); plan=parse_a2_plan(root/'A2'/'LESSON_PLAN.md'); a1=load_a1_owned(root/'lessons'/'a1'); prior=set(); rows=[]; manifest=[]
    for p in plan:
        copy=COPY[p.order]
        owned=classify_targets(p,copy,a1,prior)
        manifest.append({'lessonId':p.lesson_id,'targets':[{'sk':t.sk,'uk':t.uk,'status':t.status} for t in owned]})
        for t in owned:
            if t.status=='NEW': prior.add(normalize_sk(t.sk))
        if ns.lo<=p.order<=ns.hi: rows.append((p,copy,owned))
    assert set(COPY)==set(range(1,91)), 'COPY must define exactly 1..90'
    ids=[p.lesson_id for p in plan]
    paths=write_lessons(rows,root/ns.out,ids)
    mp=root/ns.manifest; mp.parent.mkdir(parents=True,exist_ok=True); mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Generated {len(paths)} A2 lessons ({ns.lo}-{ns.hi}); A1 owned={len(a1)}; manifest={mp}.')
if __name__=='__main__': main()
