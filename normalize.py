from __future__ import annotations
import re

ALIASES={
    'hydraulic power unit':'HPU','hydraulic unit':'HPU','hp unit':'HPU','hydraulic power pack':'HPU','hydraulic pack':'HPU','the unit':'HPU',
    'isolation valve':'IV-21','iv21':'IV-21',
    'pressure sensor 04':'PS-04','pressure sensor 04a':'PS-04A','ps04':'PS-04','p04':'PS-04','ps04a':'PS-04A','p04a':'PS-04A','p.s.04-a':'PS-04A',
    'pressure sensor 40':'PS-40','ps40':'PS-40','p40':'PS-40',
    'hcs controller':'PLC-03','aegis controller':'PLC-03','controller':'PLC-03',
}

def norm_identifier(s:str):
    x=re.sub(r'[^a-z0-9]+','',s.lower())
    if x in {'ps04','p04','pressuresensor04'}: return 'PS-04'
    if x in {'ps04a','p04a','pressuresensor04a'}: return 'PS-04A'
    if x in {'ps40','p40','pressuresensor40'}: return 'PS-40'
    if x in {'iv21','isolationvalve21'}: return 'IV-21'
    if x in {'plc03'}: return 'PLC-03'
    return s
