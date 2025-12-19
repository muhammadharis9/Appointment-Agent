import os
import requests
import json
from dotenv import load_dotenv

#Loading the environment
load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_PRIVATE_KEY")
ASSISTANT_ID = "e176f568-48e8-4711-8bc2-cc003b3d5504" 
SERVER_URL = "https://multifid-sophie-queenly.ngrok-free.dev" 

tools = [
    {
        "type": "function",
        "function": {
            "name": "checkCalendar",
            "description": "Check if a specific date/time is available for an appointment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "The date and time to check (e.g., 'next Tuesday at 2pm')."
                    }
                },
                "required": ["date"]
            }
        },
        "server": {
            "url": SERVER_URL
        }
    },
    {
        "type": "transferCall",
        "destinations": [
            {
                "type": "number",
                "number": "+16402034070",
                "message": "Transferring you to a specialist now."
            }
        ]
    }
]

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": {
        "provider": "groq", 
        "model": "llama3-8b-8192",
        "tools": tools
    }
}

print(f"Updating Assistant {ASSISTANT_ID}...")
print(f"Linking to Server: {SERVER_URL}")

response = requests.patch(
    f"https://api.vapi.ai/assistant/{ASSISTANT_ID}",
    headers=headers,
    json=payload
)

if response.status_code == 200:
    print("\n SUCCESS! Clara is now connected to your tools.")
else:
    print("\n ERROR:")
    print(response.text)