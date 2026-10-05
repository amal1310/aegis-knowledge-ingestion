from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from .parsers import parse_file

TRUST={
 'manuals':'controlled_manual', 'engineering_bulletins':'engineering_change',
 'reference':'controlled_reference', 'configuration':'machine_configuration',
 'diagrams':'controlled_diagram', 'screenshots':'operational_screenshot',
 'extra':'training_material', 'low_trust':'field_note', 'noise':'irrelevant_reference',
 'scans':'uncontrolled_calibration_scan'
}


def source_id(path: Path, root: Path):
    rel=path.relative_to(root).as_posix()
    return hashlib.sha1(rel.encode()).hexdigest()[:12]


def ingest(root: str, out_path: str):
    root=Path(root); records=[]
    for path in sorted(root.rglob('*')):
        if not path.is_file(): continue
        if path.suffix.lower() not in {'.pdf','.html','.docx','.xlsx','.json','.pptx','.png'}: continue
        rel=path.relative_to(root)
        top=rel.parts[0]
        sid=source_id(path,root)
        chunks=parse_file(path)
        records.append({
            'source_id':sid,'path':rel.as_posix(),'format':path.suffix.lower()[1:],
            'trust':TRUST.get(top,'unknown'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'chunks':chunks
        })
    Path(out_path).write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
    return records

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('output')
    a=ap.parse_args(); print(f'Ingested {len(ingest(a.root,a.output))} files')
