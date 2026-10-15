import streamlit as st

FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400"
    "&family=JetBrains+Mono:wght@400;500;600"
    "&family=Instrument+Sans:wght@400;500;600&display=swap"
)

CSS = f"<style>@import url('{FONTS_URL}');" + """
:root {
  --paper: #F3EFE6;
  --paper-2: #EAE4D6;
  --field: #FBF9F3;
  --ink: #17160F;
  --muted: #6E6A5C;
  --rule: #17160F;
  --accent: #E0501C;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: var(--paper) !important;
  color: var(--ink);
  font-family: 'Instrument Sans', system-ui, sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stDecoration"] { visibility: hidden; }
[data-testid="stSidebar"] { background: var(--paper-2) !important; border-right: 1px solid var(--rule); }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1280px; }
h1, h2, h3 { font-family: 'Fraunces', serif !important; font-weight: 600; letter-spacing: -0.01em; }

/* mode switch */
[data-testid="stSegmentedControl"] { justify-content: center; }
[data-testid="stSegmentedControl"] > div {
  border: 2.8px solid var(--ink) !important; border-radius: 999px !important; background: var(--field) !important; padding: .49rem !important;
}
[data-testid="stSegmentedControl"] button {
  min-height: 5.04rem !important; padding: .84rem 2.8rem !important; border: none !important; border-radius: 999px !important;
  background: transparent !important; color: var(--ink) !important; font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.4rem !important; text-transform: uppercase; letter-spacing: .08em; font-weight: 500 !important;
}
[data-testid="stSegmentedControl"] button[aria-checked="true"] { background: var(--ink) !important; color: var(--paper) !important; }
[data-testid="stSegmentedControl"] button:hover { color: var(--accent) !important; }
[data-testid="stSegmentedControl"] button[aria-checked="true"]:hover { color: var(--paper) !important; background: var(--accent) !important; }

/* masthead */
.masthead { border-top: 4px solid var(--ink); padding-top: .9rem; text-align: center; margin-bottom: 1.5rem; }
.masthead .deck { margin: 0 auto; }
.kicker { font-family: 'JetBrains Mono', monospace; font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); }
.masthead h1 { font-family: 'Fraunces', serif; font-size: 3.4rem; font-weight: 600; line-height: .95; margin: .35rem 0 .5rem; letter-spacing: -.02em; }
.masthead h1 em { color: var(--accent); font-weight: 400; }
.deck { color: var(--muted); font-size: 1.02rem; max-width: 52ch; margin: 0; }

/* section labels */
.section-label { font-family: 'JetBrains Mono', monospace; font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); border-bottom: 1px solid var(--rule); padding-bottom: .4rem; margin: .4rem 0 .9rem; }

/* inputs */
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
  background: var(--field) !important; border: 1px solid var(--rule) !important; border-radius: 0 !important;
  font-family: 'JetBrains Mono', monospace !important; font-size: .9rem !important; line-height: 1.55 !important; box-shadow: none !important;
}
[data-testid="stTextArea"] textarea:focus, [data-testid="stTextInput"] input:focus { border-color: var(--accent) !important; }
[data-testid="stSelectbox"] > div > div { background: var(--field) !important; border: 1px solid var(--rule) !important; border-radius: 0 !important; }

/* buttons */
.stButton button, [data-testid^="stBaseButton"] {
  border-radius: 0 !important; border: 1px solid var(--ink) !important; background: transparent !important; color: var(--ink) !important;
  font-family: 'JetBrains Mono', monospace !important; text-transform: uppercase; letter-spacing: .1em; font-size: .78rem !important;
  padding: .65rem 1.1rem !important; transition: all .15s ease;
}
.stButton button:hover { background: var(--ink) !important; color: var(--paper) !important; }
.stButton button[kind="primary"], [data-testid="stBaseButton-primary"] { background: var(--ink) !important; color: var(--paper) !important; }
.stButton button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover { background: var(--accent) !important; border-color: var(--accent) !important; }
.stButton button:disabled { opacity: .35; }

/* token stats */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); margin: 1.2rem 0; }
.stat { padding: .8rem .9rem; border-right: 1px solid var(--rule); }
.stat:last-child { border-right: none; }
.stat .label { font-family: 'JetBrains Mono', monospace; font-size: .68rem; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.stat .num { font-family: 'Fraunces', serif; font-size: 2.3rem; line-height: 1.1; font-variant-numeric: tabular-nums; }
.stat.total .num { color: var(--accent); }

/* quality score */
.score { display: flex; align-items: baseline; gap: .8rem; margin-bottom: .6rem; }
.stars { font-size: 1.5rem; color: var(--accent); letter-spacing: .15em; }
.score small { font-family: 'JetBrains Mono', monospace; font-size: .75rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }

/* expanders, alerts, code */
[data-testid="stExpander"] { border: 1px solid var(--rule) !important; border-radius: 0 !important; background: transparent; }
[data-testid="stExpander"] summary { font-family: 'JetBrains Mono', monospace; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; }
[data-testid="stAlert"] { border-radius: 0 !important; }
pre { border-radius: 0 !important; border: 1px solid var(--rule) !important; }
pre, pre code { white-space: pre-wrap !important; word-break: break-word; }
</style>"""


def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)
