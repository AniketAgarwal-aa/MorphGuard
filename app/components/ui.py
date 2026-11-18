import streamlit as st

def inject_css():
    st.markdown('''<style>
    .stApp { background: radial-gradient(circle at 10% 0%, #12304a 0, #08121f 38%, #070d16 100%); color:#e8f0f7; }
    [data-testid="stSidebar"] { background:#07111d; border-right:1px solid #1e3a4d; }
    .brand {font-size:2.4rem;font-weight:800;letter-spacing:-.06em;color:#e8fbff;margin:.2rem 0 0}.brand span{color:#35d1c4}
    .eyebrow {color:#6de3d8;text-transform:uppercase;letter-spacing:.16em;font-size:.72rem;font-weight:700}
    .subtitle {color:#9bb0c2;font-size:1rem;margin-bottom:1rem}
    .card {background:linear-gradient(145deg,rgba(18,42,61,.9),rgba(11,25,39,.92));border:1px solid #21465b;border-radius:16px;padding:1.1rem 1.2rem;min-height:112px;box-shadow:0 12px 32px rgba(0,0,0,.16)}
    .card .label {color:#91a8ba;font-size:.78rem;text-transform:uppercase;letter-spacing:.1em}.card .value{font-size:1.75rem;font-weight:750;color:#f3fbff;margin-top:.35rem}.card .hint{color:#6de3d8;font-size:.78rem;margin-top:.25rem}
    .panel {background:rgba(11,29,44,.78);border:1px solid #1b3d50;border-radius:16px;padding:1.2rem;margin:.6rem 0}
    .badge {display:inline-block;border-radius:999px;padding:.28rem .65rem;font-size:.75rem;font-weight:700;letter-spacing:.04em}.ok{background:#123f3d;color:#70f0d6}.pending{background:#4a3516;color:#ffd27b}.blocked{background:#48222a;color:#ff9ca9}.neutral{background:#203746;color:#b6d0df}
    div[data-testid="stMetricValue"] {color:#eafcff}.stButton>button {border-radius:10px;border:1px solid #2c6b79;background:#103443;color:#e9ffff}.stButton>button:hover{border-color:#5ee4d6;color:#fff}
    </style>''',unsafe_allow_html=True)

def page_header(eyebrow,title,subtitle):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div><div class="brand">MORPH<span>GUARD</span></div><h1>{title}</h1><div class="subtitle">{subtitle}</div>',unsafe_allow_html=True)

def metric_card(label,value,hint='',tone='neutral'):
    st.markdown(f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div><div class="hint">{hint}</div></div>',unsafe_allow_html=True)

def status_badge(text,tone='neutral'):
    return f'<span class="badge {tone}">{text}</span>'

def empty_state(title,body):
    st.markdown(f'<div class="panel"><h3>{title}</h3><p style="color:#9bb0c2">{body}</p></div>',unsafe_allow_html=True)

def section_title(title,caption=''):
    st.subheader(title)
    if caption: st.caption(caption)
