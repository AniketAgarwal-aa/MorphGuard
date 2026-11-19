import streamlit as st

def get_current_theme() -> str:
    """Retrieve currently active theme from session_state, defaulting to 'dark'."""
    return st.session_state.get('theme', 'dark')

def get_accent_color() -> str:
    """Return primary accent color based on active theme."""
    return '#35d1c4' if get_current_theme() == 'dark' else '#0284c7'

def inject_css(theme: str = None):
    """Inject application-wide CSS styling supporting complete Dark and Light modes."""
    if theme is None:
        theme = get_current_theme()

    if theme == 'light':
        # ── LIGHT MODE STYLING ──
        st.markdown('''<style>
        /* Light mode application container */
        .stApp {
            background-color: #f8fafc;
            background-image: radial-gradient(circle at 15% 0%, #e0f2fe 0%, #f8fafc 40%, #ffffff 100%);
            color: #0f172a;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #f1f5f9;
            border-right: 1px solid #cbd5e1;
        }
        [data-testid="stSidebar"] * {
            color: #1e293b;
        }
        [data-testid="stSidebarNav"] a {
            color: #334155 !important;
            font-size: 0.9rem;
            border-radius: 8px;
            margin: 2px 0;
            padding: 6px 12px;
            transition: all 0.15s ease-in-out;
        }
        [data-testid="stSidebarNav"] a:hover {
            background-color: rgba(2, 132, 199, 0.08) !important;
            color: #0284c7 !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: rgba(2, 132, 199, 0.14) !important;
            border-left: 4px solid #0284c7 !important;
            color: #0284c7 !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebarNavSeparator"] {
            border-top: 1px solid #cbd5e1 !important;
            margin: 12px 0 6px 0 !important;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #334155;
        }

        /* Typography & Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #0f172a !important;
            font-weight: 750;
            letter-spacing: -0.02em;
        }
        p, span, label {
            color: #1e293b;
        }

        /* Brand / Header */
        .brand {
            font-size: 2.2rem;
            font-weight: 850;
            letter-spacing: -0.05em;
            color: #0f172a;
            margin: 0.2rem 0 0;
        }
        .brand span { color: #0284c7; }
        .eyebrow {
            color: #0284c7;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 0.72rem;
            font-weight: 700;
        }
        .subtitle {
            color: #475569;
            font-size: 0.98rem;
            margin-bottom: 1.2rem;
        }

        /* Cards & Panels */
        .card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            min-height: 105px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
            transition: box-shadow 0.2s, border-color 0.2s;
        }
        .card:hover {
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.09);
            border-color: #0284c7;
        }
        .card .label {
            color: #64748b;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }
        .card .value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #0f172a;
            margin-top: 0.35rem;
        }
        .card .hint {
            color: #0284c7;
            font-size: 0.78rem;
            margin-top: 0.25rem;
            font-weight: 500;
        }
        .panel {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.2rem;
            margin: 0.6rem 0;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
        }
        .progress-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            margin: 0.8rem 0;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
        }

        /* Metric overrides */
        div[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 800; }
        div[data-testid="stMetricLabel"] { color: #475569 !important; font-weight: 600; }

        /* Buttons */
        .stButton>button {
            border-radius: 10px;
            border: 1px solid #0284c7;
            background: #0284c7;
            color: #ffffff !important;
            font-weight: 600;
            transition: background 0.2s;
        }
        .stButton>button:hover {
            background: #0369a1 !important;
            border-color: #0369a1 !important;
            color: #ffffff !important;
        }
        .stDownloadButton>button {
            border-radius: 10px;
            border: 1px solid #0284c7;
            background: #0284c7;
            color: #ffffff !important;
            font-weight: 600;
        }
        .stDownloadButton>button:hover {
            background: #0369a1 !important;
            color: #ffffff !important;
        }

        /* Tables */
        table { border-collapse: collapse; width: 100%; }
        thead tr { background: #f1f5f9; }
        thead th {
            color: #0369a1;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 0.55rem 0.8rem;
            border-bottom: 2px solid #cbd5e1;
            text-align: left;
        }
        tbody tr { border-bottom: 1px solid #e2e8f0; }
        tbody tr:hover { background: rgba(2, 132, 199, 0.04); }
        tbody td { color: #1e293b; font-size: 0.88rem; padding: 0.5rem 0.8rem; }

        /* Expanders */
        div[data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            margin-bottom: 0.6rem;
        }
        div[data-testid="stExpander"] summary {
            color: #0f172a !important;
            font-weight: 600;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            color: #475569 !important;
            font-weight: 600;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #0284c7 !important;
            border-bottom-color: #0284c7 !important;
        }

        /* Badges */
        .badge {
            display: inline-block;
            border-radius: 999px;
            padding: 0.28rem 0.68rem;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }
        .ok      { background: #dcfce7; color: #15803d; }
        .pending { background: #fef3c7; color: #b45309; }
        .blocked { background: #fee2e2; color: #b91c1c; }
        .neutral { background: #e2e8f0; color: #334155; }

        /* Status indicator dot */
        .status-dot {
            display: inline-block;
            width: 10px; height: 10px;
            border-radius: 50%;
            margin-right: 6px;
            vertical-align: middle;
        }
        .status-dot.active  { background: #0284c7; box-shadow: 0 0 0 0 rgba(2,132,199,0.7); animation: pulse-active 1.8s ease-in-out infinite; }
        .status-dot.warning { background: #f59e0b; }
        .status-dot.error   { background: #ef4444; }

        /* Footer */
        .mg-footer {
            margin-top: 2.5rem;
            padding: 0.8rem 0;
            border-top: 1px solid #e2e8f0;
            color: #64748b;
            font-size: 0.75rem;
            text-align: center;
            letter-spacing: 0.06em;
        }
        </style>''', unsafe_allow_html=True)
    else:
        # ── DARK MODE STYLING (DEFAULT) ──
        st.markdown('''<style>
        /* Dark mode application container */
        .stApp {
            background-color: #08121f;
            background-image: radial-gradient(circle at 10% 0%, #12304a 0%, #08121f 38%, #070d16 100%);
            color: #e8f0f7;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #07111d;
            border-right: 1px solid #1e3a4d;
        }
        [data-testid="stSidebar"] * {
            color: #c8dce9;
        }
        [data-testid="stSidebarNav"] a {
            color: #9bb0c2 !important;
            font-size: 0.9rem;
            border-radius: 8px;
            margin: 2px 0;
            padding: 6px 12px;
            transition: all 0.15s ease-in-out;
        }
        [data-testid="stSidebarNav"] a:hover {
            background-color: rgba(53, 209, 196, 0.08) !important;
            color: #35d1c4 !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: rgba(53, 209, 196, 0.14) !important;
            border-left: 4px solid #35d1c4 !important;
            color: #35d1c4 !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebarNavSeparator"] {
            border-top: 1px solid #1e3a4d !important;
            margin: 12px 0 6px 0 !important;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #9bb0c2;
        }

        /* Typography & Headings */
        h1, h2, h3, h4, h5, h6 {
            color: #f3fbff !important;
            font-weight: 750;
            letter-spacing: -0.02em;
        }
        p, span, label {
            color: #c8dce9;
        }

        /* Brand / Header */
        .brand {
            font-size: 2.2rem;
            font-weight: 850;
            letter-spacing: -0.05em;
            color: #e8fbff;
            margin: 0.2rem 0 0;
        }
        .brand span { color: #35d1c4; }
        .eyebrow {
            color: #6de3d8;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 0.72rem;
            font-weight: 700;
        }
        .subtitle {
            color: #9bb0c2;
            font-size: 0.98rem;
            margin-bottom: 1.2rem;
        }

        /* Cards & Panels */
        .card {
            background: linear-gradient(145deg, rgba(18, 42, 61, 0.9), rgba(11, 25, 39, 0.92));
            border: 1px solid #21465b;
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            min-height: 105px;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.22);
            transition: box-shadow 0.2s, border-color 0.2s;
        }
        .card:hover {
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.32);
            border-color: #35d1c4;
        }
        .card .label {
            color: #91a8ba;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }
        .card .value {
            font-size: 1.75rem;
            font-weight: 800;
            color: #f3fbff;
            margin-top: 0.35rem;
        }
        .card .hint {
            color: #6de3d8;
            font-size: 0.78rem;
            margin-top: 0.25rem;
            font-weight: 500;
        }
        .panel {
            background: rgba(11, 29, 44, 0.85);
            border: 1px solid #1b3d50;
            border-radius: 14px;
            padding: 1.2rem;
            margin: 0.6rem 0;
        }
        .progress-card {
            background: rgba(14, 34, 52, 0.88);
            border: 1px solid #1e4a60;
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            margin: 0.8rem 0;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.16);
        }

        /* Metric overrides */
        div[data-testid="stMetricValue"] { color: #eafcff !important; font-weight: 800; }
        div[data-testid="stMetricLabel"] { color: #9bb0c2 !important; font-weight: 600; }

        /* Buttons */
        .stButton>button {
            border-radius: 10px;
            border: 1px solid #2c6b79;
            background: #103443;
            color: #e9ffff !important;
            font-weight: 600;
            transition: all 0.2s;
        }
        .stButton>button:hover {
            border-color: #5ee4d6 !important;
            background: #154558 !important;
            color: #ffffff !important;
        }
        .stDownloadButton>button {
            border-radius: 10px;
            border: 1px solid #2c6b79;
            background: #103443;
            color: #e9ffff !important;
            font-weight: 600;
        }
        .stDownloadButton>button:hover {
            border-color: #5ee4d6 !important;
            background: #154558 !important;
            color: #ffffff !important;
        }

        /* Tables */
        table { border-collapse: collapse; width: 100%; }
        thead tr { background: rgba(18, 48, 74, 0.95); }
        thead th {
            color: #6de3d8;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 0.55rem 0.8rem;
            border-bottom: 2px solid #1e4a60;
            text-align: left;
        }
        tbody tr { border-bottom: 1px solid #142434; }
        tbody tr:hover { background: rgba(53, 209, 196, 0.06); }
        tbody td { color: #c8dce9; font-size: 0.88rem; padding: 0.5rem 0.8rem; }

        /* Expanders */
        div[data-testid="stExpander"] {
            background: rgba(11, 29, 44, 0.75) !important;
            border: 1px solid #1b3d50 !important;
            border-radius: 12px !important;
            margin-bottom: 0.6rem;
        }
        div[data-testid="stExpander"] summary {
            color: #f3fbff !important;
            font-weight: 600;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            color: #9bb0c2 !important;
            font-weight: 600;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #35d1c4 !important;
            border-bottom-color: #35d1c4 !important;
        }

        /* Badges */
        .badge {
            display: inline-block;
            border-radius: 999px;
            padding: 0.28rem 0.68rem;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
        }
        .ok      { background: #123f3d; color: #70f0d6; }
        .pending { background: #4a3516; color: #ffd27b; }
        .blocked { background: #48222a; color: #ff9ca9; }
        .neutral { background: #203746; color: #b6d0df; }

        /* Status indicator dot */
        .status-dot {
            display: inline-block;
            width: 10px; height: 10px;
            border-radius: 50%;
            margin-right: 6px;
            vertical-align: middle;
        }
        .status-dot.active  { background: #35d1c4; box-shadow: 0 0 0 0 rgba(53,209,196,0.7); animation: pulse-active 1.8s ease-in-out infinite; }
        .status-dot.warning { background: #ffd27b; }
        .status-dot.error   { background: #ff9ca9; }

        /* Footer */
        .mg-footer {
            margin-top: 2.5rem;
            padding: 0.8rem 0;
            border-top: 1px solid #1b3d50;
            color: #4a7488;
            font-size: 0.75rem;
            text-align: center;
            letter-spacing: 0.06em;
        }
        </style>''', unsafe_allow_html=True)

    # Keyframes common to both
    st.markdown('''<style>
    @keyframes pulse-active {
        0%   { box-shadow: 0 0 0 0 rgba(53,209,196,0.7); }
        70%  { box-shadow: 0 0 0 8px rgba(53,209,196,0); }
        100% { box-shadow: 0 0 0 0 rgba(53,209,196,0); }
    }
    </style>''', unsafe_allow_html=True)


def page_header(eyebrow: str, title: str, subtitle: str):
    """Render consistent page header with eyebrow, title, and subtitle."""
    st.markdown(
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<div class="brand">MORPH<span>GUARD</span></div>'
        f'<h1>{title}</h1>'
        f'<div class="subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, hint: str = '', tone: str = 'neutral'):
    """Render a clean responsive metric card."""
    st.markdown(
        f'<div class="card">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{value}</div>'
        f'<div class="hint">{hint}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def status_badge(text: str, tone: str = 'neutral') -> str:
    """Return HTML string for status pill badge."""
    return f'<span class="badge {tone}">{text}</span>'


def status_indicator(label: str, state: str = 'active') -> str:
    """Return inline pulsing dot + label. state: 'active' | 'warning' | 'error'."""
    return (
        f'<span class="status-dot {state}"></span>'
        f'<span style="vertical-align:middle;font-weight:600">{label}</span>'
    )


def empty_state(title: str, body: str):
    """Render a styled placeholder panel."""
    st.markdown(
        f'<div class="panel"><h3>{title}</h3>'
        f'<p style="margin-top:.4rem">{body}</p></div>',
        unsafe_allow_html=True,
    )


def section_title(title: str, caption: str = ''):
    """Render a styled section header with optional caption."""
    st.subheader(title)
    if caption:
        st.caption(caption)


def progress_section(title: str, body_html: str = '', caption: str = ''):
    """Render body_html inside a styled card with optional title/caption."""
    inner = f'<div style="font-weight:700;margin-bottom:.5rem">{title}</div>' if title else ''
    if caption:
        inner += f'<div style="font-size:.78rem;margin-bottom:.6rem">{caption}</div>'
    if body_html:
        inner += body_html
    st.markdown(f'<div class="progress-card">{inner}</div>', unsafe_allow_html=True)


def footer():
    """Render subtle footer at the bottom of the page."""
    st.markdown(
        '<div class="mg-footer">MorphGuard &nbsp;·&nbsp; Biometric Security Research &nbsp;·&nbsp; v3.2 Professional Edition</div>',
        unsafe_allow_html=True,
    )


def render_sidebar_controls():
    """Render persistent sidebar footer with branding, version, theme toggle, and status indicator."""
    with st.sidebar:
        st.markdown('---')
        
        # Current theme toggle
        current_theme = get_current_theme()
        theme_choice = st.radio(
            'Application Theme',
            options=['Dark Mode', 'Light Mode'],
            index=0 if current_theme == 'dark' else 1,
            horizontal=True,
            key='app_theme_radio'
        )
        new_theme = 'dark' if theme_choice == 'Dark Mode' else 'light'
        if new_theme != current_theme:
            st.session_state['theme'] = new_theme
            st.rerun()

        # Status & Version panel
        accent = '#35d1c4' if new_theme == 'dark' else '#0284c7'
        st.markdown(
            f'''<div style="background:rgba(2,132,199,0.08);border:1px solid rgba(2,132,199,0.22);border-radius:10px;padding:.75rem .85rem;margin-top:.5rem">
              <div style="font-size:.78rem;font-weight:750;letter-spacing:0.06em;color:{accent}">MORPHGUARD V3.2</div>
              <div style="font-size:.72rem;margin-top:3px;display:flex;align-items:center;gap:6px">
                <span class="status-dot active"></span>
                <span style="font-weight:600">Local Research Pipeline</span>
              </div>
              <div style="font-size:.68rem;opacity:.8;margin-top:4px">46,792 Images · 21 Calibrated Models</div>
            </div>''',
            unsafe_allow_html=True
        )
