import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).parents[2]; sys.path.insert(0,str(ROOT)); from app.components import inject_css,page_header,load_audit,metric_card,section_title,audit_status
inject_css(); page_header('DATA INTELLIGENCE','Dataset Explorer','Cached audit outputs from MONOT and ONOT. Raw directories are never rescanned by this page.')
summary,tables,counts=load_audit(); total=int(counts['count'].sum()) if not counts.empty else 0; audit=audit_status(summary,tables,counts)
c1,c2,c3,c4=st.columns(4)
vals=(total,int(counts[counts.dataset=='MONOT']['count'].sum()) if not counts.empty else 0,int(counts[counts.dataset=='ONOT']['count'].sum()) if not counts.empty else 0,int(summary.get('corrupted_count',0)))
for c,label,val in zip((c1,c2,c3,c4),('Total records','MONOT','ONOT','Corrupted'),vals):
    with c: metric_card(label,f'{val:,}','Audit metadata')
if not counts.empty:
    section_title('Category distribution'); st.bar_chart(counts.assign(series=counts.dataset+' / '+counts.category).set_index('series')['count'],color='#35d1c4'); st.dataframe(counts,use_container_width=True,hide_index=True)
for name in ('monot_inventory','onot_inventory'):
    df=tables.get(name)
    if df is not None and not df.empty:
        with st.expander(f'{name.replace("_"," ").title()} sample'): st.dataframe(df.head(100),use_container_width=True,hide_index=True)
st.markdown(f"**{audit['label']}** — {audit['message']}")
st.info('Labels remain protocol-neutral in the audit. ONOT is not automatically treated as genuine, and MONOT gate strata are not attack classes.')
