# Claude AI CLI-Chatbot mit Kontext-Gedächtnis

Ein leichtgewichtiger und sicherer Kommandozeilen-Chatbot in Python, der auf der Anthropic Claude API (`claude-sonnet-4-6`) basiert. 

🎯 **Mein Meilenstein-Projekt:** Dies ist mein **allererstes eigenständiges Projekt im Umgang mit externen Web-APIs**! Als Student der Wirtschaftsinformatik nutze ich dieses Miniprojekt, um die Brücke von der universitären Theorie zur praktischen Entwicklung von KI-Anwendungen zu schlagen und moderne Software-Architekturen von Grund auf zu verstehen.

---

## 🚀 Kernfeatures

* **Kontextbewusste Konversation:** Implementierung eines dynamischen Sitzungsgedächtnisses (Chat-Historie) mittels Python-Datenstrukturen, sodass die KI den Kontext über mehrere Dialogschritte hinweg behält.
* **Sicherheit nach Industriestandard:** Strikte Trennung von Konfiguration und Code. API-Anmeldedaten werden lokal über Umgebungsvariablen mittels `python-dotenv` verwaltet und über die `.gitignore` vor versehentlichen Leaks im Versionskontrollsystem geschützt.
* **Robuste Eingabeverarbeitung:** Bereinigung und Normalisierung von Benutzereingaben (`.strip().upper()`), um fehlerhafte Eingaben bei der Abbruchbedingung abzufangen.

---

## 🛠️ Tech Stack & Architektur

* **Programmiersprache:** Python 3.13+
* **KI-Engine:** Anthropic Claude API (`claude-sonnet-4-6`)
* **Konfigurations-Management:** `python-dotenv`, `os`
* **Versionsverwaltung:** Git