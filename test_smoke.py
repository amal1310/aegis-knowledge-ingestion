from pathlib import Path
from src.qa.answer_engine import AnswerEngine
ROOT=Path(__file__).resolve().parents[1]

def test_pressure():
 e=AnswerEngine(ROOT/'data/knowledge/facts.json',ROOT/'data/knowledge/question_gold.json')
 r=e.answer('What is the current normal operating pressure for the HPU?')
 assert '200 bar' in r['answer']
 assert 'F005' in r['claims']

def test_abstain():
 e=AnswerEngine(ROOT/'data/knowledge/facts.json',ROOT/'data/knowledge/question_gold.json')
 r=e.answer('What is the MTBF for IV-21?')
 assert r['gaps']
 assert 'not stated' in r['answer'].lower()
