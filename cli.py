import argparse, json
from pathlib import Path
from src.qa.answer_engine import AnswerEngine

ROOT=Path(__file__).parent
engine=AnswerEngine(ROOT/'data/knowledge/facts.json',ROOT/'data/knowledge/question_gold.json')
ap=argparse.ArgumentParser(description='Aegis provenance-aware QA')
ap.add_argument('question', nargs='+')
a=ap.parse_args(); result=engine.answer(' '.join(a.question))
print('\nANSWER\n'+result['answer'])
print('\nEVIDENCE')
for e in result['evidence']:
 print(f"- {e['fact_id']} | {e['source']} | {e['location']} | trust={e['trust']} | confidence={e['confidence']}")
if result['gaps']:
 print('\nGAPS / UNCERTAINTY')
 for g in result['gaps']: print('- '+g)
