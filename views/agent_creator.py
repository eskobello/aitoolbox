import re

import streamlit as st

from models import AIEnchancer
from prompts import AGENT_CREATOR
from views.common import draft_value, save_draft, limit_reached, count_iteration, start_request, render_token_stats

MAX_ITERATIONS = 5
LANGUAGES = ["Polski", "Angielski"]
LENGTHS = ["Zwięzły", "Standardowy", "Rozbudowany"]
SYSTEM_PROMPT_PATTERN = re.compile(r"### 1\. System prompt\s*(.*?)(?=^### 2\.|\Z)", re.MULTILINE | re.DOTALL)
DETAILS_PATTERN = re.compile(r"^### 2\.", re.MULTILINE)


def extract_system_prompt(content):
    match = SYSTEM_PROMPT_PATTERN.search(content)
    return match.group(1).strip() if match else content.strip()


def extract_details(content):
    match = DETAILS_PATTERN.search(content)
    return content[match.start():].strip() if match else ""


def build_request(brief, options, previous=None, feedback=None):
    parts = [f"Opis zadania:\n{brief.strip()}"]
    settings = [f"- {name}: {value}" for name, value in options.items() if value]
    if settings:
        parts.append("Parametry:\n" + "\n".join(settings))
    if previous and feedback:
        parts.append(f"Poprzednia wersja system promptu:\n{previous}\n\nCo poprawić:\n{feedback.strip()}")
    return "\n\n".join(parts)


def render(model):
    result = st.session_state.get("ac_result")

    left, right = st.columns((1, 1.3), gap="large")

    with left:
        st.markdown('<p class="section-label">01 · Opis agenta</p>', unsafe_allow_html=True)
        brief = st.text_area(
            "Opis",
            height=180,
            key="ac_brief",
            label_visibility="collapsed",
            placeholder="Np. Agent od inwestowania, który tłumaczy początkującym, jak działa dywersyfikacja portfela...",
            value=draft_value("ac_brief"),
            on_change=save_draft,
            args=("ac_brief",),
        )

        with st.expander("Parametry (opcjonalnie)"):
            language = st.selectbox(
                "Język agenta",
                LANGUAGES,
                index=LANGUAGES.index(draft_value("ac_language", LANGUAGES[0])),
                key="ac_language",
                on_change=save_draft,
                args=("ac_language",),
            )
            tone = st.text_input(
                "Ton",
                value=draft_value("ac_tone", "rzeczowy"),
                key="ac_tone",
                on_change=save_draft,
                args=("ac_tone",),
            )
            length = st.selectbox(
                "Długość promptu",
                LENGTHS,
                index=LENGTHS.index(draft_value("ac_length", LENGTHS[1])),
                key="ac_length",
                on_change=save_draft,
                args=("ac_length",),
            )
            constraints = st.text_area(
                "Ograniczenia i zakazy",
                height=90,
                value=draft_value("ac_constraints"),
                key="ac_constraints",
                on_change=save_draft,
                args=("ac_constraints",),
            )

        feedback = ""
        if result:
            st.markdown('<p class="section-label">Doprecyzuj</p>', unsafe_allow_html=True)
            feedback = st.text_area(
                "Co poprawić",
                height=110,
                key="ac_feedback",
                placeholder="Np. Krótsze odpowiedzi, zakaz podawania konkretnych spółek...",
                value=draft_value("ac_feedback"),
                on_change=save_draft,
                args=("ac_feedback",),
            )

        exhausted = limit_reached("used_ac", MAX_ITERATIONS)
        busy = st.session_state.get("busy_ac", False)
        label = "Popraw" if result and feedback.strip() else "Generuj system prompt"
        st.button(
            label,
            key="ac_submit",
            type="primary",
            disabled=exhausted or busy,
            on_click=start_request,
            args=("busy_ac", "ac_brief"),
        )

    with right:
        st.markdown('<p class="section-label">02 · System prompt</p>', unsafe_allow_html=True)
        if busy:
            options = {"Język": language, "Ton": tone, "Długość": length, "Ograniczenia": constraints}
            previous = result["system_prompt"] if result and feedback.strip() else None
            try:
                error = generate(model, build_request(brief, options, previous, feedback))
            finally:
                st.session_state.busy_ac = False
            st.session_state.ac_error = error
            st.rerun()

        error = st.session_state.pop("ac_error", None)
        if error:
            st.error(error)
        result = st.session_state.get("ac_result")
        if result:
            show_result(result)


def generate(model, request):
    with st.spinner("Projektuję agenta..."):
        try:
            response = AIEnchancer(model=model, sys_prompt=AGENT_CREATOR).run(request)
        except Exception as e:
            return f"Błąd: {e}"

    content = response["content"]
    st.session_state.ac_result = {
        "content": content,
        "system_prompt": extract_system_prompt(content),
        "details": extract_details(content),
        "tokens": response["tokens"],
    }
    count_iteration("used_ac")
    return None


def show_result(result):
    st.code(result["system_prompt"], language="markdown")
    if result["details"]:
        with st.expander("Założenia i pytania", expanded=True):
            st.markdown(result["details"])
    render_token_stats(result["tokens"])

