
import os

# Read the file
with open("app.py", "r") as f:
    content = f.read()

# Verification Steps
errors = []

# 1. Check Translations
spanish_title = "Asistente Contable <span style='color: var(--primary)'>PRO</span>"
spanish_subtitle = "v14.5 Suite Empresarial • Sistema En Línea"

if spanish_title not in content:
    errors.append("MISSING: Spanish Login Title")
if spanish_subtitle not in content:
    errors.append("MISSING: Spanish Login Subtitle")

# 2. Check English Translations (consistency)
english_title = "Accounting Assistant <span style='color: var(--primary)'>PRO</span>"
if english_title not in content:
    errors.append("MISSING: English Login Title")

# 3. Check Sidebar Order
# "lang = st.selectbox" should appear BEFORE "if not st.session_state.get('logged_in', False):"
# and specifically inside the global sidebar block we added.

login_check_snippet = "if not st.session_state.get('logged_in', False):"
login_check_idx = content.find(login_check_snippet)

# Search for the specific added block
# "with st.sidebar:\n    # Language selector accessible even on Login Page\n    lang = st.selectbox"
# We'll just look for the selectbox call before the login check.

first_selectbox_idx = content.find('lang = st.selectbox("Language / Idioma"')

if first_selectbox_idx == -1:
    errors.append("MISSING: Language Selector code")
elif login_check_idx != -1 and first_selectbox_idx > login_check_idx:
    errors.append(f"ORDER ERROR: Language selector (idx {first_selectbox_idx}) appears AFTER login check (idx {login_check_idx})")

# 4. Check for Duplicates
count_selectbox = content.count('lang = st.selectbox("Language / Idioma"')
if count_selectbox > 1:
    errors.append(f"DUPLICATE ERROR: Found {count_selectbox} instances of language selector.")

# Report
if errors:
    print("VERIFICATION FAILED:")
    for e in errors:
        print(f"- {e}")
    exit(1)
else:
    print("VERIFICATION SUCCESS: All checks passed.")
