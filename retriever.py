from __future__ import annotations
import json,re
from pathlib import Path

STOP=set('the a an is are was were what which who how does do did and or to of for with under from before after as on in by according current normal same only some all this that'.split())

def toks(s): return {x for x in re.findall(r'[a-z0-9][a-z0-9_-]+',s.lower()) if x not in STOP}

class Retriever:
    def __init__(self, facts_path):
        self.facts=json.loads(Path(facts_path).read_text(encoding='utf-8'))
    def search(self, query, top_k=8):
        q=toks(query)
        scored=[]
        for f in self.facts:
            text=' '.join(str(f.get(k,'')) for k in ['subject','predicate','value','applicability','source_path','location','note'])
            ft=toks(text)
            overlap=len(q & ft)
            if overlap:
                scored.append((overlap/(len(q) or 1), overlap, f))
        scored.sort(key=lambda x:(x[0],x[1],x[2]['confidence']),reverse=True)
        return [x[2] for x in scored[:top_k]]
