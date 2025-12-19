import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_PRIVATE_KEY")

# The IDs we created earlier
ASSISTANT_ID = "e176f568-48e8-4711-8bc2-cc003b3d5504" 
PHONE_ID = "02bda657-7a2b-445d-aff6-e3d4ccd19832"

# Your number (+33...)
CUSTOMER_NUMBER = "+33780768781" 

headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "assistantId": ASSISTANT_ID,
    "phoneNumberId": PHONE_ID,
    "customer": {
        "number": CUSTOMER_NUMBER
    }
}

print(f"📞 Dialing {CUSTOMER_NUMBER}...")

response = requests.post(
    "https://api.vapi.ai/call/phone",
    headers=headers,
    json=payload
)

if response.status_code == 201:
    print("\n✅ CALL INITIATED! Pick up your phone!")
else:
    print("\n❌ ERROR:")
    print(response.text)