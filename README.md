# Claude AI Chatbot

Ein einfacher Kommandozeilen-Chatbot in Python, der die Anthropic Claude API nutzt.

Dies ist mein erstes eigenständiges Projekt im Umgang mit einer externen API – 
gebaut um den Einstieg in die praktische KI-Entwicklung zu lernen.

## Was das Programm macht

Du tippst eine Frage ins Terminal – Claude antwortet. Das Besondere: der Chatbot 
erinnert sich an den bisherigen Gesprächsverlauf, sodass du aufeinander aufbauende 
Fragen stellen kannst, genau wie in einem echten Chat. Mit "EXIT" beendest du 
das Programm.

## Was ich dabei gelernt habe

- Wie man eine externe API (Anthropic Claude) in Python anspricht
- API-Keys sicher über Umgebungsvariablen verwalten (.env + python-dotenv)
- Gesprächsverlauf als Datenstruktur speichern und an die API weitergeben

## Tech Stack

- Python 3.13
- Anthropic Claude API (claude-sonnet-4-6)
- python-dotenv

## Setup

1. Repository klonen
2. Virtuelle Umgebung erstellen: `python3 -m venv venv`
3. Aktivieren: `source venv/bin/activate`
4. Abhängigkeiten installieren: `pip install -r requirements.txt`
5. `.env` Datei erstellen mit: `ANTHROPIC_API_KEY=dein-key`
6. Starten: `python chatbot.py`