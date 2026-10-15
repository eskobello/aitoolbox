# 🚀 AI Toolbox

Aplikacja Streamlit z dwoma narzędziami opartymi na OpenAI:

- **Prompt Optimizer** - analizuje prompt, wykrywa dwuznaczności i niesprecyzowania, proponuje ulepszoną wersję.
- **Agent Creator** - na podstawie opisu zadania generuje gotowy system prompt dla agenta AI.

## ✨ Funkcjonalności

- **Wykrywanie dwuznaczności** - fragmenty tekstu, które można zrozumieć na wiele sposobów
- **Wychwytywanie niesprecyzowań** - brakujące parametry i niejasne kryteria
- **Propozycje ulepszeń** - sugerowana wersja tekstu wolna od problemów
- **Generowanie system promptów** - opis zadania → system prompt z założeniami i pytaniami doprecyzowującymi
- **Statystyki tokenów** - wejście, wyjście i łącznie dla każdego zapytania
- **Limit iteracji na sesję** - Prompt Optimizer: 3, Agent Creator: 5. Po wyczerpaniu przyciski są zablokowane, a komunikat pojawia się na ekranie głównym. Limit resetuje się po odświeżeniu strony.

Model jest ustawiony na stałe w `app.py` (stała `MODEL`). Nie ma wyboru modelu w interfejsie.

## 📋 Wymagania

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) (menedżer pakietów)
- Klucz OpenAI API z dostępem do modelu ustawionego w `app.py`

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
uv run streamlit run app.py
```

Aplikacja otworzy się w przeglądarce pod adresem `http://localhost:8501`.

## 📁 Struktura projektu

```
tokencount/
├── app.py                          # Punkt wejścia: przełącznik trybu, stały model, motyw
├── views/
│   ├── __init__.py
│   ├── common.py                   # Wspólne komponenty: nagłówek, limity, statystyki tokenów
│   ├── theme.py                    # CSS całej aplikacji
│   ├── prompt_optimizer.py         # Widok analizy promptu
│   └── agent_creator.py            # Widok generowania system promptu agenta
├── models/
│   ├── __init__.py
│   └── ai_prompt_enchancer.py      # Klasa wywołująca OpenAI przez LangChain
├── prompts/
│   ├── __init__.py
│   └── prompts.py                  # Prompty systemowe: TEXT_ENHANCER i AGENT_CREATOR
├── .streamlit/
│   └── config.toml                 # Konfiguracja Streamlit (kolory motywu)
├── .env                            # Zmienne środowiskowe (NIE COMMITOWAĆ!)
├── .env.example                    # Szablon dla .env
├── .gitignore
├── pyproject.toml                  # Nazwa, wersja (źródło wyświetlanej wersji) i zależności
├── uv.lock
└── README.md
```

## 🔧 Konfiguracja

W pliku `.env`:

```env
# Wymagane
OPENAI_API_KEY=sk-your-key-here

# Opcjonalne
OPENAI_API_BASE=https://api.openai.com/v1
```

Model zmieniasz w `app.py`, w stałej `MODEL`. Limity iteracji ustawiasz w `views/prompt_optimizer.py` (`MAX_ITERATIONS`) i `views/agent_creator.py` (`MAX_ITERATIONS`).

## 🏷️ Wersja

Wersja wyświetlana w nagłówku pochodzi z pola `version` w `[project]` w `pyproject.toml`. Podbij ją tam przed commitem ze zmianą wersji.

## 💡 Jak to działa

### Prompt Optimizer

1. Wklejasz prompt w lewym panelu i klikasz **Sprawdź prompt**.
2. Przycisk blokuje się do czasu odpowiedzi modelu.
3. Prompt systemowy (`TEXT_ENHANCER`) analizuje tekst pod kątem dwuznaczności i niesprecyzowań.
4. Wynik zawiera:
   - Listę problemów z wyjaśnieniami i liczbę problemów
   - Wskaźnik jakości (1-5) oraz porównanie z poprzednią analizą w tej sesji
   - Ulepszoną wersję tekstu
   - Statystyki tokenów

### Agent Creator

1. Opisujesz zadanie agenta w lewym panelu. Opcjonalnie ustawiasz język, ton, długość i ograniczenia.
2. Klikasz **Generuj system prompt**. Model zwraca system prompt, założenia i pytania doprecyzowujące (`AGENT_CREATOR`).
3. Jeśli chcesz poprawić wynik, wpisujesz uwagi w pole **Co poprawić** i klikasz **Popraw**. Poprzednia wersja i uwagi trafiają do modelu razem z opisem zadania.

Każde zapytanie wysyła do OpenAI tylko prompt systemowy i bieżący tekst. Poprzednie wyniki nie są przekazywane modelowi, chyba że są częścią uwag w Agent Creator.

## 🧪 Testowanie

Projekt nie ma automatycznych testów. Sprawdź ręcznie:

```bash
uv run streamlit run app.py
```

Następnie przetestuj oba tryby w przeglądarce, w tym blokowanie przycisków podczas zapytania i komunikat po wyczerpaniu limitu.
