from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import streamlit as st

REQUIRED_CATEGORIES={('MONOT','Gate_10'),('MONOT','Gate_25'),('MONOT','Morphed'),('ONOT','digital'),('ONOT','print-scan')}

def project_root() -> Path:
    return Path(__file__).parents[2]

@st.cache_data(show_spinner=False)
def load_audit():
    root=project_root(); meta=root/'data'/'metadata'; summary={}
    summary_file=meta/'dataset_summary.json'
    if summary_file.exists():
        try: summary=json.loads(summary_file.read_text(encoding='utf-8'))
        except (OSError,ValueError): summary={"_invalid_summary":True}
    tables={}
    for name in ('monot_inventory','onot_inventory','class_distribution','corrupted_images','duplicate_images'):
        path=meta/f'{name}.csv'
        try: tables[name]=pd.read_csv(path) if path.exists() and path.stat().st_size else pd.DataFrame()
        except (OSError,ValueError,pd.errors.ParserError): tables[name]=pd.DataFrame()
    counts=pd.DataFrame(summary.get('image_counts',[]))
    return summary,tables,counts

def audit_status(summary, tables, counts):
    """Return an honest metadata state; missing metadata is never a zero-record success."""
    if not summary and counts.empty:
        return {'state':'missing','label':'AUDIT METADATA MISSING','tone':'blocked','message':'Audit metadata was not packaged or mounted. No dataset totals are available.'}
    if counts.empty or not {'dataset','category','count'}.issubset(counts.columns):
        return {'state':'invalid','label':'AUDIT METADATA INVALID','tone':'blocked','message':'The audit summary exists but does not match the expected schema.'}
    observed={(str(r.dataset),str(r.category)) for r in counts.itertuples()}
    total=int(counts['count'].sum())
    if total<=0:
        return {'state':'incomplete','label':'AUDIT INCOMPLETE','tone':'pending','message':'Audit metadata is present but contains no valid records.'}
    if not REQUIRED_CATEGORIES.issubset(observed):
        return {'state':'incomplete','label':'AUDIT INCOMPLETE','tone':'pending','message':'Audit metadata is present but one or more expected categories are missing.'}
    return {'state':'complete','label':'AUDIT COMPLETE','tone':'ok','message':f'{total:,} audited records loaded from packaged metadata.'}

@st.cache_data(show_spinner=False)
def load_metrics():
    root=project_root(); rows=[]
    for path in (root/'results'/'metrics').glob('*.json'):
        try: rows.append(json.loads(path.read_text(encoding='utf-8'))|{'model':path.stem})
        except (OSError,ValueError): pass
    return pd.DataFrame(rows)
