import streamlit as st
from dotenv import load_dotenv

from views import agent_creator, prompt_optimizer
from views.theme import apply_theme
from views.common import render_masthead

MODEL = "gpt-6-luna"
PROMPT_OPTIMIZER = "Prompt Optimizer"
AGENT_CREATOR = "Agent Creator"

load_dotenv()
st.set_page_config(page_title="AI Toolbox", layout="wide")
apply_theme()

_, switch_col, _ = st.columns((1, 2, 1))
with switch_col:
    mode = st.segmented_control(
        "Tryb",
        [PROMPT_OPTIMIZER, AGENT_CREATOR],
        default=PROMPT_OPTIMIZER,
        key="mode",
        required=True,
        label_visibility="collapsed",
        width="stretch",
    )

render_masthead(mode == AGENT_CREATOR)

if mode == AGENT_CREATOR:
    agent_creator.render(MODEL)
else:
    prompt_optimizer.render(MODEL)
