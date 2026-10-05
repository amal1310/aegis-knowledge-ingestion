from pathlib import Path
import json,sys
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT))
from src.ingestion.ingest import ingest
from src.knowledge.build import build_facts

data_root=ROOT/'data_raw'
processed=ROOT/'data/processed'; knowledge=ROOT/'data/knowledge'
processed.mkdir(parents=True,exist_ok=True); knowledge.mkdir(parents=True,exist_ok=True)
records=ingest(str(data_root),str(processed/'ingested.json'))
facts=build_facts(str(processed/'ingested.json'),str(knowledge/'facts.json'))
print(f'Ingested files: {len(records)}')
print(f'Facts: {len(facts)}')
