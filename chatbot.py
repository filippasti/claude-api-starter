import anthropic
from dotenv import load_dotenv
import os
import pyperclip  # Für den Zugriff auf die Zwischenablage
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel
from rich.table import Table  # Für die strukturierte Feature-Übersicht

# Initialisierung
load_dotenv()
verlauf = []
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()

# Offizielle API-Preise für Claude Sonnet (pro 1 Million Tokens)
PRICE_INPUT_PER_TOKEN = 3.00 / 1_000_000
PRICE_OUTPUT_PER_TOKEN = 15.00 / 1_000_000

# Globale Variablen für Statistiken und Zustand
total_input_tokens = 0
total_output_tokens = 0
letzte_antwort = ""  # Speichert die jeweils letzte Antwort für den /copy Befehl

# Farb-Themen Konfiguration
THEMES = {
    "cyberpunk": {"sys": "magenta", "bot": "cyan", "box": "rounded"},
    "matrix": {"sys": "bold green", "bot": "green", "box": "ascii"},
    "deepspace": {"sys": "blue", "bot": "purple4", "box": "double"}
}
current_theme = "cyberpunk"

sys_color = THEMES[current_theme]["sys"]
bot_color = THEMES[current_theme]["bot"]

# Detaillierte Feature-Tabelle für den Startbildschirm erstellen
feature_table = Table(box=None, padding=(0, 2))
feature_table.add_column("[bold white]Befehl[/bold white]", style="cyan", justify="left")
feature_table.add_column("[bold white]Nutzung & Erklärung[/bold white]", style="dim", justify="left")

feature_table.add_row(
    "/read <pfad> <frage>", 
    "Liest eine Datei ein (z. B. /read main.py Refaktoriere das) und übergibt sie an Claude."
)
feature_table.add_row(
    "/copy", 
    "Kopiert Claudes letzte Antwort direkt in deine Zwischenablage zum Einfügen mit Cmd+V."
)
feature_table.add_row(
    "/theme <name>", 
    "Wechselt das Design im laufenden Betrieb. Verfügbar: classic, matrix, dracula."
)
feature_table.add_row(
    "/info", 
    "Zeigt detaillierte Statistiken der aktuellen Sitzung sowie die exakten API-Kosten an."
)
feature_table.add_row(
    "/clear", 
    "Leert den kompletten Bildschirm und löscht das Gedächtnis der KI für ein neues Thema."
)
feature_table.add_row(
    "/exit", 
    "Beendet das Programm sauber und sicher."
)

# UI: Begrüßungs-Banner mit der neuen Feature-Tabelle
console.print(Panel(
    feature_table,
    title=f"[bold {sys_color}]🤖 CLAUDE AI CLI-CHATBOT ACTIVE[/bold {sys_color}]",
    subtitle="[dim]Version 1.2 | Bereit für deine Fragen[/dim]",
    border_style=sys_color,
    expand=False
))

while True:
    # Aktuelle Theme-Farben für diesen Schleifendurchlauf laden
    sys_color = THEMES[current_theme]["sys"]
    bot_color = THEMES[current_theme]["bot"]

    print()  
    frage = input("👤 Du: ")
    cmd = frage.strip().lower()

    # --- Slash-Commands verarbeiten ---
    if cmd in ["/exit", "exit"]:
        console.print("\n[bold red]Programm beendet. Bis zum nächsten Mal![/bold red]")
        break
        
    elif cmd == "/clear":
        verlauf = []
        console.clear()
        console.print(f"[bold {sys_color}]✔ Chat-Gedächtnis gelöscht und Bildschirm geleert![/bold {sys_color}]\n")
        continue
        
    elif cmd == "/info":
        session_cost = (total_input_tokens * PRICE_INPUT_PER_TOKEN) + (total_output_tokens * PRICE_OUTPUT_PER_TOKEN)
        console.print(Panel(
            f"[bold {bot_color}]Modell:[/bold {bot_color}] claude-sonnet-4-6\n"
            f"[bold {bot_color}]Nachrichten im Gedächtnis:[/bold {bot_color}] {len(verlauf)}\n"
            f"[bold {bot_color}]Aktuelles Theme:[/bold {bot_color}] {current_theme}\n"
            f"[bold {bot_color}]Token-Verbrauch gesamt:[/bold {bot_color}] {total_input_tokens} In / {total_output_tokens} Out\n"
            f"[bold {bot_color}]Gesamtkosten dieser Session:[/bold {bot_color}] ${session_cost:.5f}",
            title=f"[bold {sys_color}]ℹ System-Informationen[/bold {sys_color}]",
            border_style=sys_color,
            expand=False
        ))
        continue

    # In die Zwischenablage kopieren
    elif cmd == "/copy":
        if letzte_antwort:
            pyperclip.copy(letzte_antwort)
            console.print(f"[bold {bot_color}]✔ Die letzte Antwort wurde in die Zwischenablage kopiert![/bold {bot_color}]\n")
        else:
            console.print("[bold red]⚠ Es gibt noch keine Antwort zum Kopieren.[/bold red]\n")
        continue

    # Theme wechseln
    elif cmd.startswith("/theme"):
        parts = frage.strip().split()
        if len(parts) < 2:
            console.print(f"[bold {sys_color}]Verfügbare Themes: cyberpunk, matrix, deepspace. Nutzung: /theme <name>[/bold {sys_color}]\n")
            continue
        theme_name = parts[1].lower()
        if theme_name in THEMES:
            current_theme = theme_name
            console.print(f"[bold {THEMES[current_theme]['sys']}]✔ Theme erfolgreich auf '{theme_name}' gewechselt![/bold {THEMES[current_theme]['sys']}]\n")
        else:
            console.print(f"[bold red]⚠ Theme '{theme_name}' existiert nicht. (cyberpunk, matrix, deepspace)[/bold red]\n")
        continue

    # Lokale Dateien einlesen
    elif frage.strip().startswith("/read"):
        parts = frage.strip().split(maxsplit=2)
        if len(parts) < 2:
            console.print("[bold red]⚠ Fehler: Bitte gib einen Dateipfad an. Syntax: /read <dateipfad> <deine frage>[/bold red]\n")
            continue
        filepath = parts[1]
        user_prompt = parts[2] if len(parts) > 2 else "Analysiere den Inhalt dieser Datei."
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                file_content = f.read()
            # Verpackt die Datei elegant als Markdown-Codeblock für Claude
            frage = f"Hier ist der Inhalt der Datei `{filepath}`:\n\n```\n{file_content}\n```\n\n{user_prompt}"
        except Exception as e:
            console.print(f"[bold red]⚠ Fehler beim Lesen der Datei: {e}[/bold red]\n")
            continue
        
    elif frage.strip() == "":
        continue

    # --- API-Kommunikation ---
    verlauf.append({"role": "user", "content": frage})
    komplette_antwort = ""

    try:
        # Animierter Lade-Spinner während die API anfragt
        with console.status(f"[bold {bot_color}]Verbindung zu Anthropic wird hergestellt...[/bold {bot_color}]", spinner="dots") as status:
            
            with Live(Markdown(""), refresh_per_second=12, transient=True) as live:
                with client.messages.stream(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    system="Du bist ein minimalistischer CLI-Assistent. Nutze NIEMALS LaTeX-Formatierungen (wie $ oder $$) für mathematische Formeln. Nutze stattdessen einfache Textzeichen (z. B. * oder ^2), da das Terminal kein LaTeX darstellen kann.",
                    messages=verlauf
                ) as stream:
                    
                    status.stop()  # Spinner ausblenden, sobald Daten fließen
                    
                    for text_chunk in stream.text_stream:
                        komplette_antwort += text_chunk
                        live.update(Markdown(komplette_antwort))
        
        # Token-Metriken nach dem Stream auslesen
        final_message = stream.get_final_message()
        in_tokens = final_message.usage.input_tokens
        out_tokens = final_message.usage.output_tokens
        
        msg_cost = (in_tokens * PRICE_INPUT_PER_TOKEN) + (out_tokens * PRICE_OUTPUT_PER_TOKEN)
        
        total_input_tokens += in_tokens
        total_output_tokens += out_tokens
        letzte_antwort = komplette_antwort  # Antwort im Zustand für /copy merken

        # Die Antwort im aktuellen Theme-Stil anzeigen
        console.print(Panel(
            Markdown(komplette_antwort),
            title=f"[bold {bot_color}]🤖 Claude 4.6 Sonnet[/bold {bot_color}]",
            border_style=bot_color,
            expand=False
        ))
        
        # Token- und Kostenzeile
        console.print(f"   [dim]⚡ Tokens: {in_tokens} In / {out_tokens} Out  |  Kosten: ${msg_cost:.5f}[/dim]")
        
        verlauf.append({"role": "assistant", "content": komplette_antwort})

    # Error-Handling im aktuellen Theme-Look
    except anthropic.APIStatusError as e:
        console.print(Panel(f"[bold red]Die Anthropic-Server sind überlastet (Status {e.status_code}). Bitte gleich nochmal versuchen![/bold red]", title="Fehler", border_style="red"))
    except Exception as e:
        console.print(Panel(f"[bold red]Ein unerwarteter Fehler ist aufgetreten: {e}[/bold red]", title="Fehler", border_style="red"))