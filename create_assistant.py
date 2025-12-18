import os
import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_PRIVATE_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


system_prompt = """
You are Clara, a helpful AI assistant for HI Solutions. 
Your goal is to schedule a 30-minute 'Annual Review' appointment with existing customers.

RULES:
1. TRANSPARENCY: You must immediately disclose that you are an AI assistant in your first sentence.
2. TONE: Professional, warm, and concise. Do not use flowery language.
3. LATENCY: Keep your responses short (under 2 sentences) to prevent audio lag.
4. PERMISSION: Ask if now is a good time to talk before pitching.

FLOW:
1. Verify you are speaking to the correct person.
2. State you are an AI calling to book their annual review.
3. Propose a time (e.g., "Tuesday at 2 PM?").
4. If they agree, confirm and say goodbye.
5. If they ask a complex question (billing, complaints, technical support), say:
   "I am just a scheduling assistant, but I can connect you to a specialist." 
   Then use the 'transferCall' tool.

GUARDRAILS:
- If the user says "No" or is not interested, politely thank them and end the call.
- Do not try to answer billing questions yourself. Always transfer.
"""


assistant_config = {
    "name": "Clara - Appointment Setter",
    "transcriber": {
        "provider": "deepgram",
        "model": "nova-2",
        "language": "en"
    },
    "model": {
        "provider": "groq",
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
    },
    "voice": {
        "provider": "11labs",
        "voiceId": "sarah",
        "stability": 0.5,
        "similarityBoost": 0.75
    },
    "firstMessage": "Hi, am I speaking with the account holder? This is Clara, an AI assistant."
}

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.vapi.ai/assistant",
    headers=headers,
    json=assistant_config
)

if response.status_code == 201:
    data = response.json()
    print("\nSUCCESS! Assistant Created.")
    print(f"Assistant ID: {data['id']}")
    print("SAVE THIS ID. You will need it for the phone call.")
else:
    print("\nERROR:")
    print(response.text)