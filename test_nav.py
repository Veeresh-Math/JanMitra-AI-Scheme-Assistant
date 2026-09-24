from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", timeout=30)

# Find the My Profile page elements
print("Available pages:", [p.title for p in at.pages])
print("Current page:", at.pages[0].title if at.pages else "None")

# Check if citizen_input elements exist
print("Number of elements:", len(at.session_state))
print("Session state keys:", list(at.session_state.keys()))