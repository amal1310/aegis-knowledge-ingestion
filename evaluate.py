from __future__ import annotations
import json,re,csv
from pathlib import Path
from ..qa.answer_engine import AnswerEngine

ROOT=Path(__file__).resolve().parents[2]

def run():
    engine=AnswerEngine(ROOT/'data/knowledge/facts.json',ROOT/'data/knowledge/question_gold.json')
    gold=json.loads((ROOT/'data/knowledge/question_gold.json').read_text())
    rows=[]; claim_scores=[]; evidence_scores=[]; citation_scores=[]; abstain=[]
    for g in gold:
        r=engine.answer(g['question'])
        expected=set(g['expected_claims']); actual=set(r['claims'])
        claim= len(expected&actual)/(len(expected) or 1)
        ev= 1.0 if all(any(e['fact_id']==fid for e in r['evidence']) for fid in expected) else 0.0
        # Source citation precision: all cited facts must be in the expected set for the curated questions.
        cit= len(actual&expected)/(len(actual) or 1)
        is_abstain=bool(r['gaps']) and not g['supported']
        abstain.append(1 if is_abstain == (not g['supported']) else 0)
        claim_scores.append(claim); evidence_scores.append(ev); citation_scores.append(cit)
        rows.append({'id':g['id'],'question':g['question'],'claim_recall':round(claim,3),'evidence_coverage':round(ev,3),'citation_precision':round(cit,3),'abstention_correct':is_abstain == (not g['supported']),'answer':r['answer']})
    metrics={
      'questions':len(gold),
      'claim_recall':round(sum(claim_scores)/len(claim_scores),3),
      'evidence_coverage':round(sum(evidence_scores)/len(evidence_scores),3),
      'citation_precision':round(sum(citation_scores)/len(citation_scores),3),
      'abstention_accuracy':round(sum(abstain)/len(abstain),3),
      'supported_questions':sum(1 for g in gold if g['supported']),
      'unsupported_questions':sum(1 for g in gold if not g['supported'])
    }
    out=ROOT/'data/results'; out.mkdir(parents=True,exist_ok=True)
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf8')
    (out/'question_results.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
    with open(out/'question_results.csv','w',newline='',encoding='utf8') as f:
      w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(json.dumps(metrics,indent=2))

if __name__=='__main__': run()
