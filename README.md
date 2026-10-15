# 🚀 AI Toolbox

Aplikacja Streamlit do analizy i optymalizacji promptów dla AI. Identyfikuje dwuznaczności, niesprecyzowane kwestie oraz proponuje ulepszone wersje tekstów.

## ✨ Funkcjonalności

- **Analiza promptów** - identyfikacja problemów z precyzją i jednoznacznością
- **Wykrywanie dwuznaczności** - fragmenty tekstu które można interpretować na wiele sposobów
- **Wychwytywanie niesprecyzowań** - brakujące parametry i niejasne kryteria
- **Propozycje ulepszeń** - sugerowana wersja tekstu wolna od problemów
- **Liczenie tokenów** - widok na koszt i zdatność promptu
- **Optymalizacja kosztów** - domyślnie używa najtańszego modelu (gpt-4o-mini)

## 📋 Wymagania

- Python 3.8+
- `uv` (Python package manager)
- OpenAI API key

## 🚀 Instalacja

1. **Sklonuj repozytorium:**
```bash
git clone <repo-url>
cd tokencount
```

2. **Zainstaluj zależności:**
```bash
uv sync
```

3. **Stwórz plik `.env`:**
```bash
cp .env.example .env
```

4. **Dodaj swój OpenAI API key do `.env`:**
```env
OPENAI_API_KEY=sk-your-key-here
```

## ▶️ Uruchomienie

```bash
streamlit run app.py
```

Aplikacja otworzy się w przeglądarce na `http://localhost:8501`

## 📁 Struktura projektu

```
tokencount/
├── app.py                          # Główna aplikacja Streamlit
├── models/
│   ├── __init__.py
│   └── ai_prompt_enchancer.py     # Klasa do analizy promptów
├── prompts/
│   ├── __init__.py
│   └── prompts.py                  # Prompt systemowy do analizy
├── .env                            # Zmienne środowiskowe (NIE COMMITOWAĆ!)
├── .env.example                    # Szablon dla .env
├── .gitignore
├── pyproject.toml
└── README.md
```

## 🔧 Konfiguracja

W pliku `.env` możesz dostosować:

```env
# Obowiązkowe
OPENAI_API_KEY=sk-your-key-here

# Opcjonalne
SELECTED_MODEL=gpt-4o-mini         # Model OpenAI (domyślnie: gpt-4o-mini)
OPENAI_API_BASE=https://api.openai.com/v1
```

## 💡 Jak to działa

1. Użytkownik wpisuje prompt w lewym panelu
2. Kliknięcie "Check" wysyła prompt do OpenAI
3. System prompt (`TEXT_ENHANCER`) analizuje tekst pod kątem:
   - **Dwuznaczności** - wieloznaczne słowa, niejasne odniesienia
   - **Niesprecyzowań** - brakujące parametry, niezdefiniowane kryteria
4. Wynik zawiera:
   - Listę problemów z wyjaśnieniami
   - Podsumowanie ilości problemów
   - Ulepszoną wersję tekstu
5. Wyświetlane są też statystyki tokenów (wejście/wyjście/razem)

## 🧪 Testowanie

```bash
streamlit run app.py
```
