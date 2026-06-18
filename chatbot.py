import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
verlauf = []
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

while True:

    frage = input("(Exit eingeben um das Programm zu beenden)\nStelle eine Frage: " )

    if frage.strip().upper() == "EXIT" :
        break
    
    verlauf.append({"role": "user", "content": frage})
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=verlauf
    )

    print("Claude sagt:", message.content[0].text)
    verlauf.append({"role": "assistant", "content": message.content[0].text})
