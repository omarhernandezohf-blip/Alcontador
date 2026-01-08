import google.generativeai as genai
import toml
import os

try:
    secrets = toml.load(".streamlit/secrets.toml")
    if "general" in secrets and "api_key_google" in secrets["general"]:
        api_key = secrets["general"]["api_key_google"]
        print(f"API Key found: {api_key[:5]}...")
    else:
        print("API Key not found in secrets.toml")
        exit(1)
except Exception as e:
    print(f"Error reading secrets: {e}")
    # Fallback to try reading manually if toml fails (though streamlit has it)
    exit(1)

genai.configure(api_key=api_key)

print("\n--- Listing Available Models ---")
try:
    found_flash = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            if 'gemini-1.5-flash' in m.name:
                found_flash = True
except Exception as e:
    print(f"Error listing models: {e}")

print("\n--- Testing gemini-1.5-flash-001 ---")
try:
    model = genai.GenerativeModel('gemini-1.5-flash-001')
    response = model.generate_content("Hello, can you hear me?")
    print(f"Success! Response: {response.text[:50]}...")
except Exception as e:
    print(f"Error testing gemini-1.5-flash-001: {e}")

print("\n--- Testing gemini-1.5-flash ---")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, can you hear me?")
    print(f"Success! Response: {response.text[:50]}...")
except Exception as e:
    print(f"Error testing gemini-1.5-flash: {e}")
