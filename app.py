from pathlib import Path
import json
try:
 import streamlit as st
except ImportError:
 raise SystemExit('Install streamlit to run the optional UI: pip install streamlit')
from src.qa.answer_engine import AnswerEngine
ROOT=Path(__file__).parent
engine=AnswerEngine(ROOT/'data/knowledge/facts.json',ROOT/'data/knowledge/question_gold.json')
st.set_page_config(page_title='Aegis Knowledge QA',layout='wide')
st.title('Aegis Series-7 HCS — Evidence-first QA')
st.caption('Answers are grounded in the supplied package. Conflicts, scope and missing evidence are surfaced explicitly.')
q=st.text_area('Ask a question',height=100,placeholder='e.g. What is the current normal operating pressure for the HPU?')
if st.button('Answer') and q.strip():
 r=engine.answer(q)
 st.subheader('Answer')
 st.write(r['answer'])
 st.subheader('Evidence')
 for e in r['evidence']:
  with st.expander(f"{e['fact_id']} — {e['source']} — {e['location']}"):
   st.write({'value':e['value'],'trust':e['trust'],'confidence':e['confidence']})
 if r['gaps']:
  st.subheader('Uncertainty / gaps')
  for g in r['gaps']: st.warning(g)
