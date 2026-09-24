"""Full diagnostic test suite for JanMitra project."""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
all_ok = True

def check(label, ok, detail=""):
    global all_ok
    sym = PASS if ok else FAIL
    if not ok: all_ok = False
    print(f"  {sym}  {label:<45} {detail}")

# ══ 1. SYNTAX CHECK ══════════════════════════════════════════════════════════
print("\n[1] SYNTAX CHECK")
import ast
files = [
    "app.py",
    "app_pages/citizen_input.py",
    "app_pages/eligible_schemes.py",
    "app_pages/ask_language.py",
    "src/download_data.py",
    "src/capture_screenshots.py",
]
for f in files:
    try:
        with open(f, encoding="utf-8") as fh:
            compile(fh.read(), f, "exec")
        check(f, True)
    except SyntaxError as e:
        check(f, False, str(e))

# ══ 2. REQUIRED LIBRARIES ═════════════════════════════════════════════════════
print("\n[2] REQUIRED LIBRARIES")
required = ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "joblib", "streamlit"]
for lib in required:
    try:
        m = __import__(lib)
        ver = getattr(m, "__version__", "ok")
        check(lib, True, ver)
    except ImportError as e:
        check(lib, False, str(e))

print("\n[3] OPTIONAL LIBRARIES (fallbacks active if missing)")
optional = ["xgboost", "torch", "transformers", "datasets", "plotly", "kaggle"]
for lib in optional:
    try:
        m = __import__(lib)
        ver = getattr(m, "__version__", "ok")
        print(f"  OK    {lib:<20} {ver}")
    except ImportError:
        print(f"  --    {lib:<20} not installed — fallback will be used")

# ══ 3. FILE STRUCTURE CHECK ════════════════════════════════════════════════════
print("\n[4] FILE STRUCTURE")
must_exist = [
    "app.py", "requirements.txt", "README.md",
    "app_pages/citizen_input.py",
    "app_pages/eligible_schemes.py",
    "app_pages/ask_language.py",
    "src/download_data.py",
    "notebooks/VeereshMath_JanMitra_AI_Scheme_Assistant.ipynb",
    "VeereshMath_ProjectReport.docx",
    "data/raw/schemes", "data/raw/citizens", "data/raw/nlp",
    "data/processed", "models", "reports/figures",
]
for p in must_exist:
    exists = os.path.exists(p)
    check(p, exists)

# ══ 4. FEATURE ENGINEERING LOGIC ══════════════════════════════════════════════
print("\n[5] FEATURE ENGINEERING UNIT TESTS")
import numpy as np
income_bins = [0, 100_000, 300_000, 500_000, 800_000, 1_200_000, 1e9]
age_bins    = [0, 18, 35, 55, 70, 120]
soc_vul_map = {"SC": 1.0, "ST": 1.0, "OBC": 0.7, "EWS": 0.8, "General": 0.2}

test_profiles = [
    (25, 80_000,  "SC",      0, "BPL young SC farmer"),
    (40, 600_000, "General", 2, "Mid-income salaried"),
    (70, 50_000,  "ST",      0, "Elderly tribal"),
    (18, 0,       "ST",      5, "Young unemployed ST"),
    (35, 1_500_000,"General",3, "High-income professional"),
]
for age, inc, cat, occ, label in test_profiles:
    ab   = max(0, int(np.digitize(age, age_bins[1:])) - 1)
    ib   = max(0, int(np.digitize(inc, income_bins[1:])) - 1)
    iv   = 1 - min(inc / 1_000_000, 1)
    av   = min(abs(age - 40) / 40, 1)
    sv   = soc_vul_map.get(cat, 0.5)
    vuln = round(0.4 * iv + 0.3 * av + 0.3 * sv, 4)
    X    = np.array([[ab, ib, occ, vuln]])
    ok   = (X.shape == (1, 4)) and (0.0 <= vuln <= 1.0)
    check(label, ok, f"vuln={vuln:.3f}  X={X.tolist()}")

# ══ 5. INTENT HEURISTIC TESTS ══════════════════════════════════════════════════
print("\n[6] INTENT HEURISTIC TESTS")
def classify_heuristic(text):
    t = text.lower()
    if any(w in t for w in ["eligible", "qualify", "patra", "yogya", "అర్హ"]):
        return "eligibility_query"
    elif any(w in t for w in ["apply", "application", "avedan", "దరఖాస్తు"]):
        return "application_process"
    elif any(w in t for w in ["document", "dastavez", "kagaz"]):
        return "document_query"
    elif any(w in t for w in ["benefit", "amount", "kitna", "rupay", "money"]):
        return "benefit_query"
    else:
        return "scheme_info"

intent_tests = [
    ("Am I eligible for PM Kisan?",           "eligibility_query"),
    ("How to apply for Ayushman Bharat?",      "application_process"),
    ("What documents are needed for PMAY?",    "document_query"),
    ("How much money under MGNREGA?",          "benefit_query"),
    ("Tell me about PM Ujjwala Yojana",        "scheme_info"),
    ("PM Kisan ke liye patra kaun hai?",       "eligibility_query"),
    ("Ayushman Bharat apply kaise karein?",    "application_process"),
    ("PMAY ke liye kaun se documents chahiye?","document_query"),
]
for q, expected in intent_tests:
    got = classify_heuristic(q)
    check(f'"{q[:45]}"', got == expected, f"{got}")

# ══ 6. NOTEBOOK JSON VALIDITY ══════════════════════════════════════════════════
print("\n[7] NOTEBOOK VALIDITY")
import json
nb_path = "notebooks/VeereshMath_JanMitra_AI_Scheme_Assistant.ipynb"
try:
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)
    cells      = nb["cells"]
    md_cells   = sum(1 for c in cells if c["cell_type"] == "markdown")
    code_cells = sum(1 for c in cells if c["cell_type"] == "code")
    check("Valid JSON",          True,      f"{len(cells)} cells total")
    check("Markdown cells >= 14", md_cells >= 14, f"{md_cells} found")
    check("Code cells >= 10",    code_cells >= 10, f"{code_cells} found")
    # source can be str or list-of-str depending on nbformat version
    def cell_src(c):
        s = c["source"]
        return "".join(s) if isinstance(s, list) else s
    src_all = " ".join(cell_src(c) for c in cells)
    for marker in ["VeereshMath", "03_scheme_coverage_heatmap", "vulnerability_score",
                   "RandomForest", "Pipeline complete"]:
        check(f"Contains '{marker}'", marker in src_all)
except Exception as e:
    check(nb_path, False, str(e))

# ══ 7. REQUIREMENTS.TXT ════════════════════════════════════════════════════════
print("\n[8] REQUIREMENTS.TXT")
try:
    lines = [l.strip() for l in open("requirements.txt") if l.strip() and not l.startswith("#")]
    check("File readable", True, f"{len(lines)} packages listed")
    for pkg in ["pandas", "numpy", "streamlit", "scikit-learn"]:
        found = any(pkg in l.lower() for l in lines)
        check(f"  {pkg} listed", found)
except Exception as e:
    check("requirements.txt", False, str(e))

# ══ 8. DOCX REPORT ═════════════════════════════════════════════════════════════
print("\n[9] PROJECT REPORT")
try:
    from docx import Document
    doc    = Document("VeereshMath_ProjectReport.docx")
    words  = sum(len(p.text.split()) for p in doc.paragraphs)
    tables = len(doc.tables)
    check("VeereshMath_ProjectReport.docx readable", True, f"{words} words, {tables} tables")
    check("Word count >= 4000", words >= 4000, f"{words} words")
    check("Tables >= 8", tables >= 8, f"{tables} tables")
except ImportError:
    print("  --  python-docx not installed — report check skipped")
except Exception as e:
    check("Project report", False, str(e))

# ══ SUMMARY ════════════════════════════════════════════════════════════════════
print()
print("="*60)
print("OVERALL:", "ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED — see FAIL lines above")
print("="*60)
