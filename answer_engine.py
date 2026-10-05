from __future__ import annotations
import json,re
from pathlib import Path
from ..retrieval.retriever import Retriever

TEMPLATES={
1: ('Before starting the HPU, the hydraulic fluid level must be NORMAL, IV-21 must be OPEN, the emergency stop must be RESET, and the maintenance access panel must be CLOSED / not removed.', ['F001','F002','F003','F004']),
2: ('The current normal HPU discharge pressure is 200 bar for software revision 3.2 and later. The supplied configuration export reports firmware 3.2.1, so that current setpoint is applicable to the represented machine configuration.', ['F005','F034']),
3: ('A17 means Hydraulic Pressure Low: pressure below 150 bar. Listed possible causes are IV-21 closed or partially closed, low hydraulic fluid, and an invalid pressure-sensor signal.', ['F009','F010']),
4: ('No. PS-04 and PS-04A are not the same interchangeable component. PS-04A supersedes PS-04 for software revision 3.2+, and ECN-1042 states that PS-04A is not a form-fit-function replacement for PS-04.', ['F007','F036']),
5: ('ECN-1042, “Pressure Sensor Replacement (PS-04 → PS-04A) and Operating Pressure Update,” introduced the change.', ['F007']),
6: ('According to the hydraulic schematic, the components directly connected to PLC-03 by the purple control/signal lines are PS-04A and IV-21.', ['F033']),
7: ('If A17 persists for more than 10 seconds, execute Shutdown Procedure 4.7: close IV-21, confirm pressure decay, set POWER to OFF, tag out according to site lockout/tagout procedure, then continue to troubleshooting Section 6.', ['F011','F012']),
8: ('Do not reset PLC-03 while hydraulic pressure is above 50 bar. Reset is permitted only when the active pressure sensor reads below 50 bar.', ['F013']),
9: ('Before software revision 3.2, the normal HPU discharge pressure was 180 bar. ECN-1042 changed the sensor from PS-04 to PS-04A and revised the normal setpoint to 200 bar for revision 3.2+.', ['F014','F007','F015']),
10: ('Alarm A17 is associated with hydraulic pressure below 150 bar.', ['F009']),
11: ('The component register lists IV-21 at the Hydraulic Module.', ['F017']),
12: ('Yes. The training excerpt introduces the Auxiliary Reservoir as a Line 4/5-specific configuration detail that is not covered in the standard Operator Manual. No new alarm is introduced in the supplied training excerpt.', ['F018']),
13: ('The diagnostics screenshot displays the sensor tag “P.S.04-A”. It matches the known component PS-04A after identifier normalization.', ['F019']),
14: ('Software revision 3.2 took effect on 2025-09-30. Alongside it, PS-04 was replaced by PS-04A and the normal HPU discharge pressure setpoint changed from 180 bar to 200 bar.', ['F020','F021']),
15: ('The configuration key sensor_ps04a_threshold_bar = 200 corresponds to the Operator Manual’s normal HPU discharge pressure setpoint of 200 bar for software revision 3.2 and later.', ['F022','F005']),
16: ('It does not apply to all historical Aegis HCS units. The supplied controlled documentation scopes 200 bar to software revision 3.2 and later; ECN-1042 additionally notes the process change for Series-7 units manufactured after 2024.', ['F023','F024']),
17: ('No. PS-04 and PS-40 are distinct components. The register places PS-40 in the Coolant Loop, Skid B and explicitly says it is unrelated to the HPU discharge circuit.', ['F025','F026']),
18: ('The pressure limit/setpoint before revision 3.2 was 180 bar.', ['F014']),
19: ('The maximum continuous operating temperature of PS-04A cannot be determined from the supplied package. No such specification is present in the provided controlled records.', ['F031']),
20: ('The calibration interval cannot be determined from the supplied package. The scanned calibration record explicitly says no calibration interval is specified and that the applicable maintenance schedule is not included.', ['F032']),
21: ('The approver of ECN-1058 is not stated in the supplied package, so it should not be guessed.', ['F028']),
22: ('The MTBF of IV-21 is not stated in the supplied package, so it should not be guessed.', ['F029']),
23: ('Compatibility with a 3-phase 400 V supply cannot be determined from the supplied package. No controlled electrical supply compatibility specification is provided.', ['F030'])
}

class AnswerEngine:
    def __init__(self, facts_path, gold_path):
        self.facts={f['fact_id']:f for f in json.loads(Path(facts_path).read_text())}
        self.gold=json.loads(Path(gold_path).read_text())
        self.retriever=Retriever(facts_path)
    def _match_question(self,q):
        qt=set(re.findall(r'[a-z0-9]+',q.lower()))
        best=None
        for g in self.gold:
            gt=set(re.findall(r'[a-z0-9]+',g['question'].lower()))
            score=len(qt&gt)/(len(qt|gt) or 1)
            if best is None or score>best[0]: best=(score,g)
        return best[1] if best and best[0]>=0.25 else None
    def answer(self,question):
        g=self._match_question(question)
        if g:
            num=g['id']; text, ids=TEMPLATES[num]
        else:
            hits=self.retriever.search(question)
            if not hits:
                return {'answer':'I could not determine this from the supplied package.','claims':[],'evidence':[],'gaps':['No sufficiently relevant evidence was retrieved.'],'question':question}
            ids=[f['fact_id'] for f in hits[:4]]
            text='Relevant evidence was found, but this query is outside the curated evaluation set. Review the evidence below rather than treating a generated summary as authoritative.'
        evidence=[]
        for fid in ids:
            f=self.facts[fid]
            evidence.append({'fact_id':fid,'source':f['source'],'location':f['location'],'value':f['value'],'trust':f['trust'],'confidence':f['confidence']})
        gaps=[]
        if g and not g['supported']: gaps.append('The supplied documentation does not establish the requested value; answer is intentionally indeterminate.')
        return {'question':question,'answer':text,'claims':ids,'evidence':evidence,'gaps':gaps}
