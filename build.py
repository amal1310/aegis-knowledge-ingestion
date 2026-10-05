from __future__ import annotations
import json
from pathlib import Path
from .curated_facts import FACTS


def build_facts(ingested_path: str, out_path: str):
    ingested=json.loads(Path(ingested_path).read_text(encoding='utf-8'))
    by_path={r['path']:r for r in ingested}
    out=[]
    for f in FACTS:
        src=by_path.get(f['source'],{})
        rec=dict(f)
        rec['source_id']=src.get('source_id','')
        rec['source_sha256']=src.get('sha256','')
        out.append(rec)
    Path(out_path).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    return out
