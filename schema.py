from dataclasses import dataclass, asdict, field
from typing import Optional

@dataclass
class Fact:
    fact_id: str
    subject: str
    predicate: str
    value: str
    unit: Optional[str]=None
    applicability: Optional[str]=None
    source_id: str=''
    source_path: str=''
    location: str=''
    trust: str=''
    confidence: float=1.0
    evidence_type: str='native_text'
    note: str=''
    def asdict(self): return asdict(self)

@dataclass
class Conflict:
    conflict_id: str
    topic: str
    fact_ids: list[str]
    resolution: str
    rationale: str
    def asdict(self): return asdict(self)
