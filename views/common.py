import tomllib
from pathlib import Path

import streamlit as st

# Wersja z [project] w pyproject.toml (jedyne źródło prawdy)
with (Path(__file__).resolve().parents[1] / "pyproject.toml").open("rb") as _f:
    __version__ = tomllib.load(_f)["project"]["version"]


def render_masthead(agent_mode):
    if agent_mode:
        title = 'Agent <em>Creator</em>'
        deck = "Opisz rolę i dziedzinę - dostań gotowy system prompt dopasowany do zadania."
    else:
        title = 'Prompt <em>Optimizer</em>'
        deck = "Ulepszaj prompty, zanim wyczerpiesz tokeny. Wyłap niejasności i ukryte założenia."
    st.markdown(
        f'<div class="masthead"><div class="kicker">AI Toolbox · V{__version__}</div>'
        f'<h1>{title}</h1><p class="deck">{deck}</p></div>',
        unsafe_allow_html=True,
    )


def draft_value(widget_key, default=""):
    """Wartość startowa widgetu. Streamlit czyści stan widgetu, który nie był renderowany, więc trzymamy kopię."""
    return st.session_state.setdefault(f"draft_{widget_key}", default)


def save_draft(widget_key):
    st.session_state[f"draft_{widget_key}"] = st.session_state[widget_key]


def fmt_number(value):
    return f"{value:,}".replace(",", " ")


def render_token_stats(tokens):
    cells = [
        ("Wejście", tokens["prompt_tokens"], ""),
        ("Wyjście", tokens["completion_tokens"], ""),
        ("Łącznie", tokens["total_tokens"], "total"),
    ]
    html = "".join(
        f'<div class="stat {css}"><div class="label">{label}</div>'
        f'<div class="num">{fmt_number(value)}</div></div>'
        for label, value, css in cells
    )
    st.markdown(f'<div class="stats">{html}</div>', unsafe_allow_html=True)


def limit_reached(counter_key, max_iterations):
    """Pokazuje komunikat dopiero po wyczerpaniu limitu i zwraca True, gdy limit jest wyczerpany."""
    if st.session_state.get(counter_key, 0) < max_iterations:
        return False
    st.warning("Osiągnięto limit iteracji w tej sesji. Odśwież stronę, aby zacząć od nowa.")
    return True


def count_iteration(counter_key):
    st.session_state[counter_key] = st.session_state.get(counter_key, 0) + 1


def start_request(busy_key, text_key):
    """on_click przycisku: blokuje go do odpowiedzi LLM, ale tylko gdy pole nie jest puste."""
    if st.session_state.get(text_key, "").strip():
        st.session_state[busy_key] = True
