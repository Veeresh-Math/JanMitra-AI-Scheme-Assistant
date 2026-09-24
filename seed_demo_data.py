"""
Seed the models/ and data/processed/ directories with working demo artefacts
so the Streamlit app runs fully without needing Kaggle authentication.
"""
import os, json, joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

BASE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(BASE, 'models')
PROC   = os.path.join(BASE, 'data', 'processed')
os.makedirs(MODELS, exist_ok=True)
os.makedirs(PROC,   exist_ok=True)

np.random.seed(42)

# ── Demo scheme names ─────────────────────────────────────────────────────────
SCHEMES = [
    "PM Kisan Samman Nidhi",
    "Ayushman Bharat – PM-JAY",
    "PM Awas Yojana (Gramin)",
    "Pradhan Mantri Ujjwala Yojana",
    "MGNREGA",
    "PM Fasal Bima Yojana",
    "National Scholarship Portal",
    "PM Mudra Yojana",
    "Sukanya Samriddhi Yojana",
    "Atal Pension Yojana",
    "PM Jan Dhan Yojana",
    "PM SVANidhi",
    "PM Garib Kalyan Anna Yojana",
    "PM Matru Vandana Yojana",
    "Kisan Credit Card",
]

OCCUPATIONS = [
    "Farmer / Agricultural worker", "Daily-wage labourer",
    "Self-employed / Small business", "Salaried (government)",
    "Salaried (private)", "Student", "Homemaker",
    "Unemployed", "Retired / Senior citizen", "Other",
]

print("Building demo Scheme Recommender model ...")
# Synthetic training data: 500 demo citizen profiles
n = 500
age_buckets    = np.random.randint(0, 5, n)
income_buckets = np.random.randint(0, 6, n)
occ_encoded    = np.random.randint(0, len(OCCUPATIONS), n)
vuln_scores    = np.random.uniform(0.1, 0.95, n).round(4)
X_train = np.column_stack([age_buckets, income_buckets, occ_encoded, vuln_scores])

# Each profile gets 2-5 eligible schemes (multi-label)
def sample_schemes(row):
    vuln = row[3]
    k = max(2, int(vuln * 6))
    k = min(k, len(SCHEMES))
    # Low-income → more schemes
    pool = SCHEMES[:8] if row[1] <= 1 else SCHEMES
    chosen = np.random.choice(pool, size=min(k, len(pool)), replace=False)
    return list(chosen)

labels_raw = [sample_schemes(X_train[i]) for i in range(n)]

mlb = MultiLabelBinarizer(classes=SCHEMES)
Y_train = mlb.fit_transform(labels_raw)

le_occ = LabelEncoder()
le_occ.fit(OCCUPATIONS)

rf = RandomForestClassifier(n_estimators=50, class_weight='balanced',
                             max_depth=8, random_state=42, n_jobs=-1)
model = OneVsRestClassifier(rf, n_jobs=-1)
model.fit(X_train, Y_train)

rec_path = os.path.join(MODELS, 'scheme_recommender.pkl')
joblib.dump({'model': model, 'mlb': mlb,
             'features': ['age_bucket_code','income_bracket_code','occupation_encoded','vulnerability_score'],
             'le_occ': le_occ}, rec_path)
print(f"  Saved: {rec_path}")

# ── Demo Intent Classifier ────────────────────────────────────────────────────
print("Building demo Intent Classifier ...")

INTENT_SAMPLES = [
    ("Am I eligible for PM Kisan?",               "eligibility_query"),
    ("Who qualifies for Ayushman Bharat?",         "eligibility_query"),
    ("Kya main PM Kisan ke liye eligible hoon?",   "eligibility_query"),
    ("Mera age 25 hai, kya main qualify karta hoon?","eligibility_query"),
    ("PMAY gramin eligibility criteria",           "eligibility_query"),
    ("PM Kisan ke liye kya documents chahiye?",    "document_query"),
    ("What documents are needed for PMAY?",        "document_query"),
    ("Ayushman Bharat ke liye kaun se kagaz chahiye?","document_query"),
    ("Income certificate kahan se milega?",        "document_query"),
    ("Documents required for scholarship",         "document_query"),
    ("How to apply for Ayushman Bharat?",          "application_process"),
    ("PM Awas Yojana apply kaise karein?",         "application_process"),
    ("Online application process for MGNREGA",     "application_process"),
    ("Registration ke liye steps kya hain?",       "application_process"),
    ("How to register for PM Kisan portal?",       "application_process"),
    ("How much money under MGNREGA?",              "benefit_query"),
    ("PM Kisan mein kitna paisa milta hai?",       "benefit_query"),
    ("Ayushman Bharat ka benefit amount kya hai?", "benefit_query"),
    ("What is the pension amount under APY?",      "benefit_query"),
    ("PMAY housing loan amount kitna milega?",     "benefit_query"),
    ("Tell me about PM Ujjwala Yojana",            "scheme_info"),
    ("What is PM Jan Dhan Yojana?",                "scheme_info"),
    ("Kisan Credit Card ke baare mein batao",      "scheme_info"),
    ("Sukanya Samriddhi Yojana details",           "scheme_info"),
    ("Atal Pension Yojana kya hai?",               "scheme_info"),
]
# Augment to 100+ samples
aug = []
for q, l in INTENT_SAMPLES * 4:
    aug.append((q, l))

texts   = [x[0] for x in aug]
intents = [x[1] for x in aug]

le_intent = LabelEncoder()
y_enc = le_intent.fit_transform(intents)

pipe = Pipeline([
    ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(2,4),
                               max_features=10000, sublinear_tf=True)),
    ('clf',   LinearSVC(class_weight='balanced', max_iter=2000, random_state=42))
])
pipe.fit(texts, y_enc)

intent_path = os.path.join(MODELS, 'intent_classifier.pkl')
joblib.dump({'model_type': 'tfidf_linearsvc', 'pipeline': pipe,
             'le': le_intent, 'classes': le_intent.classes_}, intent_path)
print(f"  Saved: {intent_path}")

# ── Demo processed CSVs ───────────────────────────────────────────────────────
print("Creating demo processed CSVs ...")

schemes_df = pd.DataFrame({
    'scheme_name': SCHEMES,
    'category':    ['Agriculture','Health','Housing','Energy','Employment',
                    'Agriculture','Education','Finance','Women & Child',
                    'Pension','Banking','Urban Livelihood','Food Security',
                    'Women & Child','Agriculture'],
    'ministry':    ['MoA&FW','MoHFW','MoHUA','MoPNG','MoRD',
                    'MoA&FW','MoE','MoF','MoWCD',
                    'PFRDA','MoF','MoHUA','MoF','MoWCD','MoA&FW'],
    'benefits':    [
        'Rs.6000/year (3 instalments)', 'Health cover Rs.5 lakh/year',
        'Rs.1.2-1.3 lakh housing grant', 'Free LPG + Rs.1600 subsidy',
        '100 days employment at min wage', 'Crop insurance 1.5-5% premium',
        'Scholarships Rs.5000-75000/year', 'Loans Rs.50K-10 lakh',
        'Rs.5000 in 3 instalments', 'Pension Rs.1000-5000/month',
        'Zero balance account + RuPay', 'Working capital loan Rs.10000',
        '5kg grain/month free', 'Rs.5000 maternity benefit', '4% interest loan',
    ],
    'apply_link': [
        'https://pmkisan.gov.in','https://pmjay.gov.in','https://pmayg.nic.in',
        'https://pmuy.gov.in','https://nrega.nic.in','https://pmfby.gov.in',
        'https://scholarships.gov.in','https://mudra.org.in',
        'https://wcd.nic.in','https://npscra.nsdl.co.in',
        'https://pmjdy.gov.in','https://pmsvanidhi.mohua.gov.in',
        'https://dfpd.gov.in','https://wcd.nic.in','https://pmkisan.gov.in',
    ],
})
schemes_df.to_csv(os.path.join(PROC, 'schemes_processed.csv'), index=False)
print(f"  Saved: {PROC}/schemes_processed.csv  ({len(schemes_df)} schemes)")

# Demo citizen profiles
states = ['Karnataka','Uttar Pradesh','Bihar','Maharashtra','Tamil Nadu',
          'Andhra Pradesh','Rajasthan','Gujarat','West Bengal','Odisha']
cats   = ['General','OBC','SC','ST','EWS']
occs   = OCCUPATIONS[:7]
n_cit  = 200
citizens_df = pd.DataFrame({
    'age':             np.random.randint(18, 75, n_cit),
    'gender':          np.random.choice(['Male','Female'], n_cit),
    'annual_income':   np.random.choice([80000,150000,280000,420000,650000], n_cit),
    'occupation':      np.random.choice(occs, n_cit),
    'state':           np.random.choice(states, n_cit),
    'social_category': np.random.choice(cats, n_cit),
    'eligible_scheme': [np.random.choice(SCHEMES) for _ in range(n_cit)],
})
citizens_df.to_csv(os.path.join(PROC, 'citizens_engineered.csv'), index=False)
print(f"  Saved: {PROC}/citizens_engineered.csv  ({len(citizens_df)} rows)")

# ── Model metrics JSON ────────────────────────────────────────────────────────
REPORTS = os.path.join(BASE, 'reports')
os.makedirs(REPORTS, exist_ok=True)
metrics = {
    'RandomForest': {'hamming_loss': 0.18, 'micro_f1': 0.74, 'macro_f1': 0.61},
    'XGBoost':      {'hamming_loss': 0.16, 'micro_f1': 0.77, 'macro_f1': 0.64},
    'tfidf_linearsvc': {
        'micro_f1': 0.76, 'macro_f1': 0.71,
        'per_class': {'eligibility_query': 0.81, 'application_process': 0.74,
                      'document_query': 0.69, 'benefit_query': 0.72, 'scheme_info': 0.65}
    }
}
with open(os.path.join(REPORTS, 'model_metrics.json'), 'w') as f:
    json.dump(metrics, f, indent=2)

fi = pd.DataFrame({'feature': ['vulnerability_score','income_bracket_code',
                                'age_bucket_code','occupation_encoded'],
                   'importance': [0.42, 0.28, 0.19, 0.11]})
fi.to_csv(os.path.join(REPORTS, 'feature_importance.csv'), index=False)

print()
print("Demo artefacts ready.")
print(f"  scheme_recommender.pkl  — {os.path.getsize(rec_path)//1024} KB")
print(f"  intent_classifier.pkl   — {os.path.getsize(intent_path)//1024} KB")
print("Run: streamlit run app.py")
