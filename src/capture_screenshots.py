"""
src/capture_screenshots.py
───────────────────────────────────────────────────────────────────────────────
Captures the two dashboard screenshots (11_dashboard_screenshot.png and
12_multilingual_demo.png) needed for the README visual teasers.

Prerequisites
─────────────
  pip install playwright
  playwright install chromium

Usage
─────
  # In one terminal — start the Streamlit app:
  streamlit run app.py --server.headless true --server.port 8501

  # In a second terminal — run this script:
  python src/capture_screenshots.py

The script waits for the app to be ready, navigates to each page,
and saves 1280×800 screenshots to reports/figures/.
"""
import os, time, subprocess, sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed.")
    print("Run:  pip install playwright && playwright install chromium")
    sys.exit(1)

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES = os.path.join(BASE, "reports", "figures")
os.makedirs(FIGURES, exist_ok=True)

APP_URL = "http://localhost:8501"

def wait_for_app(timeout=30):
    import urllib.request, urllib.error
    for _ in range(timeout):
        try:
            urllib.request.urlopen(APP_URL, timeout=2)
            return True
        except Exception:
            time.sleep(1)
    return False

print("Waiting for Streamlit app at", APP_URL, "...")
if not wait_for_app():
    print("ERROR: App not reachable after 30 s.")
    print("Start it with:  streamlit run app.py --server.headless true")
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page    = browser.new_page(viewport={"width": 1280, "height": 800})

    # ── Page 1: fill citizen profile and submit ──────────────────────────────
    print("Loading Page 1 — Citizen profile input ...")
    page.goto(APP_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Click "Find my schemes" button (navigate to Page 2 via session state)
    try:
        page.locator("button:has-text('Find my schemes')").click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)
    except Exception:
        pass  # button may not be visible if form not filled — navigate directly

    # ── Page 2: Eligible Schemes ──────────────────────────────────────────────
    print("Navigating to Page 2 — Eligible schemes ...")
    # Click the top-nav tab (Streamlit 1.35+ st.navigation renders as tab bar)
    try:
        page.locator("a:has-text('Eligible schemes')").first.click()
        page.wait_for_load_state("networkidle")
        time.sleep(3)
    except Exception:
        pass

    out2 = os.path.join(FIGURES, "11_dashboard_screenshot.png")
    page.screenshot(path=out2, full_page=False)
    print(f"  Saved: {out2}")

    # ── Page 3: Multilingual demo ─────────────────────────────────────────────
    print("Navigating to Page 3 — Ask in your language ...")
    try:
        page.locator("a:has-text('Ask in your language')").first.click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Type a Hindi eligibility query and submit
        page.locator("input[data-testid='stTextInput']").first.fill(
            "PM Kisan ke liye eligibility kya hai?"
        )
        page.locator("button:has-text('Ask JanMitra')").first.click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)
    except Exception as e:
        print(f"  Note: could not auto-fill query ({e}) — taking blank screenshot")

    out3 = os.path.join(FIGURES, "12_multilingual_demo.png")
    page.screenshot(path=out3, full_page=False)
    print(f"  Saved: {out3}")

    browser.close()

print("\nScreenshots saved to reports/figures/")
print("  11_dashboard_screenshot.png")
print("  12_multilingual_demo.png")
print("\nYou can now push these files to GitHub and they will render in README.md.")
