import re

import streamlit as st

from models import AIEnchancer
from prompts import TEXT_ENHANCER
from views.common import draft_value, save_draft, limit_reached, count_iteration, start_request, render_token_stats

MAX_ITERATIONS = 3
IMPROVED_MARKER = "### 2. Tekst poprawiony"
PROBLEM_PATTERN = re.compile(r"^### (\d+)\.\s+", re.MULTILINE)


def quality_score(problems_count):
    return max(1, 5 - (problems_count // 2))


def split_analysis(content):
    analysis, _, improved = content.partition(IMPROVED_MARKER)
    return analysis.strip(), improved.strip() or None


def render(model):
    left, right = st.columns((1, 1.3), gap="large")

    with left:
        st.markdown('<p class="section-label">01 · Prompt</p>', unsafe_allow_html=True)
        user_prompt = st.text_area(
            "Prompt",
            height=320,
            key="tc_prompt",
            label_visibility="collapsed",
            placeholder="Wklej prompt, który chcesz sprawdzić...",
            value=draft_value("tc_prompt"),
            on_change=save_draft,
            args=("tc_prompt",),
        )
        exhausted = limit_reached("used_tc", MAX_ITERATIONS)
        busy = st.session_state.get("busy_tc", False)
        st.button(
            "Sprawdź prompt",
            key="tc_check",
            type="primary",
            disabled=exhausted or busy,
            on_click=start_request,
            args=("busy_tc", "tc_prompt"),
        )

    with right:
        st.markdown('<p class="section-label">02 · Analiza</p>', unsafe_allow_html=True)
        if busy:
            try:
                error = analyze(model, user_prompt)
            finally:
                st.session_state.busy_tc = False
            st.session_state.tc_error = error
            st.rerun()

        error = st.session_state.pop("tc_error", None)
        if error:
            st.error(error)
        result = st.session_state.get("tc_result")
        if result:
            show_result(result)


def analyze(model, user_prompt):
    with st.spinner("Analizuję prompt..."):
        try:
            response = AIEnchancer(model=model, sys_prompt=TEXT_ENHANCER).run(user_prompt)
        except Exception as e:
            return f"Błąd: {e}"

    content = response["content"]
    problems_count = len(PROBLEM_PATTERN.findall(content))
    previous = st.session_state.get("tc_result")

    st.session_state.tc_result = {
        "content": content,
        "tokens": response["tokens"],
        "problems_count": problems_count,
        "quality_score": quality_score(problems_count),
        "prev_problems": previous["problems_count"] if previous else None,
    }
    count_iteration("used_tc")
    return None


def show_result(result):
    analysis, improved = split_analysis(result["content"])
    count, score, prev = result["problems_count"], result["quality_score"], result["prev_problems"]

    st.markdown(
        f'<div class="score"><span class="stars">{"★" * score}{"☆" * (5 - score)}</span>'
        f'<small>wskaźnik jakości {score}/5</small></div>',
        unsafe_allow_html=True,
    )
    if prev is None:
        st.info(f"Znaleziono {count} problemów.")
    elif prev > count:
        st.success(f"Poprawa: o {prev - count} mniej problemów niż poprzednio.")
    elif prev < count:
        st.warning(f"Pogorszenie: o {count - prev} problemów więcej niż poprzednio.")
    else:
        st.info("Bez zmian w liczbie problemów.")

    with st.expander("Analiza", expanded=True):
        st.markdown(analysis)

    if improved:
        st.markdown('<p class="section-label">Ulepszona wersja</p>', unsafe_allow_html=True)
        st.code(improved, language="markdown")

    render_token_stats(result["tokens"])