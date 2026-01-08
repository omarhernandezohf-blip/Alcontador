import google.generativeai as genai
import toml

try:
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets["general"]["api_key_google"]
except:
    exit(1)

genai.configure(api_key=api_key)

models_to_test = ['gemini-2.0-flash', 'gemini-flash-latest', 'gemini-2.5-flash']

for m in models_to_test:
    print(f"\n--- Testing {m} ---")
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content("Hello, are you working?")
        print(f"Success ({m}): {response.text[:50]}...")
    except Exception as e:
        print(f"Error ({m}): {e}")
