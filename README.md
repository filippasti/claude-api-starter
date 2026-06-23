# Claude AI CLI-Chatbot

Ein interaktiver Kommandozeilen-Chatbot in Python, der die Anthropic Claude API nutzt.
Dies war mein erstes eigenständiges Projekt im Umgang mit einer externen API – 
inzwischen habe ich es um mehrere praktische Features erweitert, um tiefer in die 
Möglichkeiten der LLM-Integration einzutauchen.

## Features

- **Live-Streaming** – Claudes Antworten erscheinen Wort für Wort in Echtzeit
- **Gesprächsgedächtnis** – der Bot merkt sich den Verlauf für zusammenhängende Dialoge
- **Token- & Kostentracking** – zeigt nach jeder Anfrage den Verbrauch und die exakten API-Kosten an
- **Dateien einlesen** (`/read <pfad> <frage>`) – Claude kann lokale Dateien analysieren
- **Zwischenablage** (`/copy`) – kopiert die letzte Antwort direkt zum Einfügen
- **Themes** (`/theme <name>`) – wechselbare Farbschemata (cyberpunk, matrix, deepspace)
- **Session-Infos** (`/info`) – Statistiken zur aktuellen Sitzung
- **Sauberes Error-Handling** – fängt API- und Eingabefehler ab

## Befehlsübersicht

| Befehl | Funktion |
|--------|----------|
| `/read <pfad> <frage>` | Datei einlesen und an Claude übergeben |
| `/copy` | Letzte Antwort in die Zwischenablage kopieren |
| `/theme <name>` | Design wechseln |
| `/info` | Statistiken & Kosten der Session anzeigen |
| `/clear` | Bildschirm leeren & Gedächtnis zurücksetzen |
| `/exit` | Programm beenden |

## Tech Stack

- Python 3.13
- Anthropic Claude API (claude-sonnet-4-6, mit Streaming)
- rich (Terminal-Formatierung)
- pyperclip (Zwischenablage)
- python-dotenv (sicheres API-Key-Management)

## Setup

1. Repository klonen
2. Virtuelle Umgebung erstellen: `python3 -m venv venv`
3. Aktivieren: `source venv/bin/activate`
4. Abhängigkeiten installieren: `pip install -r requirements.txt`
5. `.env` Datei erstellen mit: `ANTHROPIC_API_KEY=dein-key`
6. Starten: `python chatbot.py`