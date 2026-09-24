"""
src/download_data.py
Downloads all three JanMitra datasets to the correct local paths.

Prerequisites
-------------
1. Kaggle API token at ~/.kaggle/kaggle.json (chmod 600 on macOS/Linux)
   Windows: %USERPROFILE%\\.kaggle\\kaggle.json
   NEVER commit this file. It is listed in .gitignore.

2. HuggingFace `datasets` library installed (pip install datasets).

Usage
-----
    python src/download_data.py

The script is idempotent — re-running skips files that already exist.
"""
import os, sys

BASE   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEME = os.path.join(BASE, "data", "raw", "schemes")
CITZ   = os.path.join(BASE, "data", "raw", "citizens")
NLP    = os.path.join(BASE, "data", "raw", "nlp")

for d in [SCHEME, CITZ, NLP]:
    os.makedirs(d, exist_ok=True)

# ── Dataset 1: Government Schemes (Kaggle) ────────────────────────────────────
scheme_file = os.path.join(SCHEME, "indian_government_schemes.csv")
if not os.path.exists(scheme_file):
    print("Downloading Dataset 1 (Government Schemes) from Kaggle ...")
    try:
        import kaggle
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            "datasciencedisciple/indian-government-schemes",
            path=SCHEME, unzip=True
        )
        print(f"  Saved to {SCHEME}")
    except Exception as e:
        print(f"  ERROR: {e}")
        print("  Place kaggle.json in ~/.kaggle/ and retry.")
        sys.exit(1)
else:
    print(f"  Dataset 1 already present: {scheme_file}")

# ── Dataset 2: Citizen Eligibility (Kaggle) ───────────────────────────────────
citizen_file = os.path.join(CITZ, "Indian_Government_Scheme_Eligibility_Dataset.csv")
if not os.path.exists(citizen_file):
    print("Downloading Dataset 2 (Citizen Eligibility) from Kaggle ...")
    try:
        import kaggle
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            "datasciencedisciple/indian-government-scheme-eligibility",
            path=CITZ, unzip=True
        )
        print(f"  Saved to {CITZ}")
    except Exception as e:
        print(f"  ERROR: {e}")
        sys.exit(1)
else:
    print(f"  Dataset 2 already present: {citizen_file}")

# ── Dataset 3: Multilingual QA (HuggingFace) ─────────────────────────────────
qa_file = os.path.join(NLP, "qa_dataset.csv")
if not os.path.exists(qa_file):
    print("Downloading Dataset 3 (Multilingual QA) from HuggingFace ...")
    try:
        from datasets import load_dataset
        ds  = load_dataset("Aditipatil56/adaption-india-govt-schemes-qa",
                           trust_remote_code=True)
        key = list(ds.keys())[0]
        ds[key].to_pandas().to_csv(qa_file, index=False)
        print(f"  Saved to {qa_file}")
    except Exception as e:
        print(f"  ERROR: {e}")
        sys.exit(1)
else:
    print(f"  Dataset 3 already present: {qa_file}")

print("\nAll datasets ready.")
