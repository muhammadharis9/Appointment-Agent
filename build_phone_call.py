import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_PRIVATE_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "provider": "twilio",
    "number": TWILIO_NUMBER,
    "twilioAccountSid": TWILIO_ACCOUNT_SID,
    "twilioAuthToken": TWILIO_AUTH_TOKEN,
    "name": "My Twilio Number"
}

print(f"Connecting Twilio Number {TWILIO_NUMBER} to Vapi...")

response = requests.post(
    "https://api.vapi.ai/phone-number",
    headers=headers,
    json=payload
)

if response.status_code == 201:
    data = response.json()
    print("\n SUCCESS! Phone Number Connected.")
    print(f"Phone ID: {data['id']}")
    print("Vapi can now dial out using this line.")
elif response.status_code == 400 and "already exists" in response.text:
    print("\n NOTE: This number is already connected. You are good to go!")
else:
    print("\n ERROR:")
    print(response.text)