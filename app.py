import streamlit as st
from dotenv import load_dotenv
from models import AIEnchancer
from prompts import TEXT_ENHANCER
import re
from datetime import datetime

load_dotenv()

st.set_page_config(page_title="Prompt Optimizer", layout="wide")
st.title("🚀 Prompt Optimizer")
st.write("Analizuj i ulepszaj swoje prompty do AI")

if "history" not in st.session_state:
    st.session_state.history = []

MAX_ITERATIONS = 3
current_iterations = len(st.session_state.history)

SELECTED_MODEL = st.sidebar.selectbox(
    "Wybierz model:",
    options=["gpt-4o-mini", "gpt-5.6-luna"],
    index=0
)

with st.sidebar:
    st.subheader("📊 Limity")
    st.metric("Iteracje", f"{current_iterations}/{MAX_ITERATIONS}")
    if current_iterations >= MAX_ITERATIONS:
        st.warning("⚠️ Osiągnięto limit iteracji w tej sesji")
    st.divider()

    if st.session_state.history:
        st.subheader("📜 Historia")
        for i, entry in enumerate(reversed(st.session_state.history), 1):
            with st.expander(f"Iteracja {len(st.session_state.history) - i + 1} - {entry['time']}"):
                st.write(f"**Problemy:** {entry['problems_count']}")
                st.write(f"**Tokeny:** {entry['tokens']['total_tokens']}")
                st.text_area("Prompt", value=entry['original_prompt'], height=100, disabled=True, key=f"hist_{i}_orig")
                st.text_area("Wynik", value=entry['improved_prompt'], height=100, disabled=True, key=f"hist_{i}_imp")

st.sidebar.divider()

col1, col2 = st.columns((1, 2))

with col1:
    st.subheader("📝 Wpisz swój prompt:")
    user_prompt = st.text_area("Prompt", height=250, placeholder="Wpisz tutaj swój prompt...", label_visibility="collapsed")

with col2:
    st.subheader("✨ Analiza:")

    can_analyze = current_iterations < MAX_ITERATIONS

    if st.button("🔍 Check", disabled=not can_analyze):
        if user_prompt.strip():
            with st.spinner("Analizuję..."):
                try:
                    enchancer = AIEnchancer(model=SELECTED_MODEL, sys_prompt=TEXT_ENHANCER)
                    result = enchancer.run(user_prompt)

                    problems_match = re.findall(r'^### (\d+)\.\s+', result["content"], re.MULTILINE)
                    problems_count = len(problems_match)

                    st.markdown(result["content"])

                    st.divider()

                    quality_score = max(1, 5 - (problems_count // 2))
                    if st.session_state.history:
                        prev_problems = st.session_state.history[-1]['problems_count']
                        improvement = prev_problems - problems_count
                        st.subheader(f"⭐ Wskaźnik jakości: {quality_score}/5")
                        if improvement > 0:
                            st.success(f"✅ Poprawa! Zmniejszono problemy o {improvement}")
                        elif improvement < 0:
                            st.warning(f"⚠️ Pogorszenie! Przybyło {abs(improvement)} problemów")
                        else:
                            st.info("➡️ Bez zmian w liczbie problemów")
                    else:
                        st.subheader(f"⭐ Wskaźnik jakości: {quality_score}/5")
                        st.info(f"📈 Znaleziono {problems_count} problemów")

                    st.divider()
                    marker = "### 2. Tekst poprawiony"
                    if marker in result["content"]:
                        st.subheader("✨ Ulepszona wersja do skopiowania")
                        text_to_copy = result["content"].split(marker, 1)[1].strip()
                        st.code(text_to_copy, language="markdown")

                    st.divider()
                    col_tokens = st.columns(3)
                    with col_tokens[0]:
                        st.metric("Wejście", result["tokens"]["prompt_tokens"])
                    with col_tokens[1]:
                        st.metric("Wyjście", result["tokens"]["completion_tokens"])
                    with col_tokens[2]:
                        st.metric("Łącznie", result["tokens"]["total_tokens"])

                    st.session_state.history.append({
                        "original_prompt": user_prompt,
                        "improved_prompt": result["content"],
                        "tokens": result["tokens"],
                        "problems_count": problems_count,
                        "quality_score": quality_score,
                        "time": datetime.now().strftime("%H:%M:%S")
                    })

                except Exception as e:
                    st.error(f"❌ Błąd: {str(e)}")
        else:
            st.warning("⚠️ Wpisz prompt przed kliknięciem Check!")
