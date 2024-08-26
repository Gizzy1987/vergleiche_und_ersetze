import requests
from googletrans import Translator
import openai

# Google Translate
def google_translate(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# OpenAI ChatGPT
def chatgpt_translate(text, target_language='en', api_key='YOUR_OPENAI_API_KEY'):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following text to {target_language}: {text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Copilot API
def copilot_translate(text, target_language='en'):
    api_url = "https://api.copilot.com/translate"
    api_key = "YOUR_COPILOT_API_KEY"  # Ersetze durch deinen Copilot API-Schlüssel
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "target_language": target_language
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("translated_text")
    else:
        raise Exception(f"Fehler bei der Copilot-Übersetzung: {response.status_code} - {response.text}")
