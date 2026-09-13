from __future__ import annotations
import argparse, json, re
from pathlib import Path
from jsonschema import Draft202012Validator

def order_of(p:Path):
    m=re.search(r'-l(\d\d)\.json$',p.name); return int(m.group(1)) if m else -1

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('directory'); ap.add_argument('schema'); ap.add_argument('--from',dest='lo',type=int,default=1); ap.add_argument('--to',dest='hi',type=int,default=90); ns=ap.parse_args()
    schema=json.loads(Path(ns.schema).read_text(encoding='utf-8')); v=Draft202012Validator(schema); errors=[]; n=0
    for p in sorted(Path(ns.directory).glob('a2-s*-l*.json')):
        o=order_of(p)
        if not ns.lo<=o<=ns.hi: continue
        n+=1; doc=json.loads(p.read_text(encoding='utf-8'))
        for e in sorted(v.iter_errors(doc),key=lambda x:list(x.path)):
            errors.append(f'{p.name} :: {"/".join(map(str,e.path))} :: {e.message}')
    if errors:
        print(f'SCHEMA FAILED: {len(errors)} issue(s) across {n} files'); [print('-',e) for e in errors]; raise SystemExit(1)
    print(f'SCHEMA PASSED: {n} A2 files.')
if __name__=='__main__': main()
