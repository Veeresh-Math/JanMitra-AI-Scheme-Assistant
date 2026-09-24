"""Page 1 — My Profile (Advanced citizen input with eligibility pre-scoring).
Bug #4 fix: replaced st.form(border=False) with plain container + manual submit button.
Bug #5 fix: live score preview is now outside the form inputs so it renders cleanly.
"""
import streamlit as st
import numpy as np

# ── Constants ──────────────────────────────────────────────────────────────────
STATES_UTS = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
    "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
    "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
    "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu",
    "Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
    "Andaman & Nicobar Islands","Chandigarh",
    "Dadra & Nagar Haveli and Daman & Diu","Delhi",
    "Jammu & Kashmir","Ladakh","Lakshadweep","Puducherry",
]
OCCUPATIONS = [
    "Farmer / Agricultural worker","Daily-wage labourer",
    "Self-employed / Small business","Salaried (government)",
    "Salaried (private)","Student","Homemaker",
    "Unemployed","Retired / Senior citizen","Other",
]
SOCIAL_CATS = ["General","OBC","SC","ST","EWS"]

SOC_VUL = {"SC":1.0,"ST":1.0,"OBC":0.7,"EWS":0.8,"General":0.2}

def compute_score(age, annual_income, social_category, occupation,
                  disability, land_acres, family_size):
    """Return 0-100 JanMitra Eligibility Score."""
    inc_vul  = 1 - min(annual_income / 1_000_000, 1)
    age_vul  = min(abs(age - 40) / 40, 1)
    soc_vul  = SOC_VUL.get(social_category, 0.5)
    dis_bon  = 0.1 if disability else 0
    land_bon = min(land_acres / 10, 0.1) if occupation == "Farmer / Agricultural worker" else 0
    fam_bon  = min((family_size - 1) * 0.01, 0.05)
    raw = 0.38*inc_vul + 0.26*age_vul + 0.24*soc_vul + dis_bon + land_bon + fam_bon
    return min(int(raw * 100), 99)

def score_label(score):
    if score >= 80: return "Excellent", "#34c759", "🟢"
    if score >= 60: return "Good",      "#0071e3", "🔵"
    if score >= 40: return "Moderate",  "#ff9f0a", "🟡"
    return "Basic", "#8e8e93", "⚪"

# ── Hero header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:32px 0 8px">
  <p style="font-size:13px;color:#0071e3;font-weight:600;letter-spacing:.06em;
             text-transform:uppercase;margin-bottom:6px">JanMitra</p>
  <h1 style="font-size:38px;font-weight:700;letter-spacing:-0.03em;
              color:#1d1d1f;margin:0 0 10px">Find your government benefits.</h1>
  <p style="font-size:17px;color:#6e6e73;margin:0 0 28px;max-width:560px">
    Tell JanMitra about yourself. In seconds, it matches you with every
    central and state scheme you qualify for — with eligibility scores,
    benefit amounts, and exact documents needed.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Form inputs (plain container — no grey box) ────────────────────────────────
# Bug #4: using st.container instead of st.form to avoid the grey background
with st.container():

    # ── Section A: Personal Details ────────────────────────────────────────
    st.markdown("""
    <div style="font-size:11px;font-weight:700;letter-spacing:.08em;
                text-transform:uppercase;color:#6e6e73;margin-bottom:12px">
      A · Personal Details
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        age = st.slider("Age", 18, 80, 30, help="Your current age in years")
    with col2:
        gender = st.selectbox("Gender", ["Male","Female","Other / Prefer not to say"])
    with col3:
        marital = st.selectbox("Marital status", ["Single","Married","Widowed","Divorced"])

    col4, col5 = st.columns([1, 1])
    with col4:
        family_size = st.number_input("Family size (members)", 1, 15, 4)
    with col5:
        disability = st.checkbox("Person with disability (PwD)",
                                  help="Tick if you or a household member has a disability")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Section B: Location & Category ────────────────────────────────────────
    st.markdown("""
    <div style="font-size:11px;font-weight:700;letter-spacing:.08em;
                text-transform:uppercase;color:#6e6e73;margin-bottom:12px">
      B · Location &amp; Category
    </div>""", unsafe_allow_html=True)

    col6, col7, col8 = st.columns([1.2, 0.9, 0.9])
    with col6:
        state = st.selectbox("State / Union Territory",
                              STATES_UTS, index=STATES_UTS.index("Karnataka"))
    with col7:
        social_category = st.selectbox("Social category", SOCIAL_CATS,
                                        help="As per Indian reservation classification")
    with col8:
        area_type = st.selectbox("Area type", ["Rural","Urban","Semi-Urban"])

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Section C: Occupation & Earnings ──────────────────────────────────────
    st.markdown("""
    <div style="font-size:11px;font-weight:700;letter-spacing:.08em;
                text-transform:uppercase;color:#6e6e73;margin-bottom:12px">
      C · Occupation &amp; Earnings
    </div>""", unsafe_allow_html=True)

    col9, col10 = st.columns([1, 1])
    with col9:
        occupation = st.selectbox("Primary occupation", OCCUPATIONS)
    with col10:
        ration_card = st.selectbox("Ration card type",
                                    ["None","APL (Above Poverty Line)",
                                     "BPL (Below Poverty Line)",
                                     "AAY (Antyodaya Anna Yojana)"])

    col11, col12, col13 = st.columns([1, 1, 1])
    with col11:
        monthly_income = st.number_input(
            "Monthly household income (₹)",
            min_value=0, max_value=500_000, value=12_000, step=500,
            help="Total earnings (income) of all earning members per month. Enter the monthly amount, not yearly.")
    with col12:
        other_income = st.number_input(
            "Other annual income (₹)",
            min_value=0, max_value=2_000_000, value=0, step=5_000,
            help="Rental, pension, agriculture, interest income etc.")
    with col13:
        land_acres = st.number_input(
            "Land holding (acres)",
            min_value=0.0, max_value=100.0, value=0.0, step=0.5,
            help="Agricultural land owned by household (0 if none)")

    # Computed annual income
    annual_income = monthly_income * 12 + other_income

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Section D: Existing Assets & Schemes ──────────────────────────────────
    st.markdown("""
    <div style="font-size:11px;font-weight:700;letter-spacing:.08em;
                text-transform:uppercase;color:#6e6e73;margin-bottom:12px">
      D · Existing Assets &amp; Entitlements
    </div>""", unsafe_allow_html=True)

    col14, col15, col16 = st.columns(3)
    with col14:
        has_bank = st.checkbox("Has bank account", value=True)
    with col15:
        has_aadhaar = st.checkbox("Has Aadhaar card", value=True)
    with col16:
        has_house = st.checkbox("Owns house / pucca building")

    col17, col18 = st.columns(2)
    with col17:
        has_lpg = st.checkbox("Has LPG connection")
    with col18:
        is_farmer = occupation == "Farmer / Agricultural worker"
        if is_farmer:
            has_kcc = st.checkbox("Has Kisan Credit Card")
        else:
            has_kcc = False

# ── Live score preview (Bug #5 fix: now inside form for reactivity) ─────────────────────────────────
with st.container(border=True):
    st.markdown("**Live eligibility score**")
    
    # Compute preview score inside form container
    preview_score = compute_score(age, annual_income, social_category,
                                 occupation, disability, land_acres, family_size)
    tier, color, dot = score_label(preview_score)
    
    # Score display with visual feedback
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"""
        <div style="background:{color};color:#fff;border-radius:50%;width:52px;height:52px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:20px;font-weight:800;margin:auto">
            {preview_score}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div>
            <div style="font-size:13px;font-weight:700;color:{color};margin-bottom:4px">
                {dot} JanMitra Score: {tier}
            </div>
            <div style="font-size:12px;color:#6e6e73">
                Based on your inputs, you likely qualify for
                <strong style="color:#1d1d1f">{max(2, preview_score//14)} or more</strong>
                government schemes.
            </div>
            <div style="font-size:11px;color:#6e6e73;margin-top:4px">
                <em>Adjust any field to see real-time changes</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Submit button (Bug #4: outside form, primary style applied via CSS)
submitted = st.button("Find My Schemes →", type="primary", key="submit_profile")

# ── On submit ──────────────────────────────────────────────────────────────────
if submitted:
    profile = {
        "age": age, "gender": gender, "marital": marital,
        "family_size": int(family_size),
        "disability": disability,
        "state": state, "social_category": social_category, "area_type": area_type,
        "occupation": occupation, "ration_card": ration_card,
        "monthly_income": int(monthly_income),
        "other_income": int(other_income),
        "annual_income": int(annual_income),
        "land_acres": float(land_acres),
        "has_bank": has_bank, "has_aadhaar": has_aadhaar,
        "has_house": has_house, "has_lpg": has_lpg, "has_kcc": has_kcc,
    }
    st.session_state.profile   = profile
    st.session_state.submitted = True          # Bug #1 fix: explicit submitted flag
    st.session_state.score     = compute_score(
        age, annual_income, social_category, occupation,
        disability, land_acres, family_size
    )

    # ── Run recommender ────────────────────────────────────────────────────────
    artifact   = st.session_state.get("_recommender")
    schemes_df = st.session_state.get("_schemes_df")

    income_bins = [0,100_000,300_000,500_000,800_000,1_200_000,1e9]
    age_bins    = [0,18,35,55,70,120]
    occ_map     = {o:i for i,o in enumerate(OCCUPATIONS)}

    ab   = max(0, int(np.digitize(age, age_bins[1:])) - 1)
    ib   = max(0, int(np.digitize(annual_income, income_bins[1:])) - 1)
    oe   = occ_map.get(occupation, 0)
    iv   = 1 - min(annual_income/1_000_000, 1)
    av   = min(abs(age-40)/40, 1)
    sv   = SOC_VUL.get(social_category, 0.5)
    vuln = round(0.38*iv + 0.26*av + 0.24*sv + (0.1 if disability else 0), 4)
    X    = np.array([[ab, ib, oe, vuln]])

    results = []
    if artifact and artifact.get("model") and artifact["model"] is not None:
        try:
            model  = artifact["model"]
            mlb    = artifact["mlb"]
            scores = [e.predict_proba(X)[0][1] for e in model.estimators_]
            top_idx = np.argsort(scores)[::-1]
            for idx in top_idx:
                if scores[idx] > 0.08:
                    results.append({
                        "scheme":     mlb.classes_[idx],
                        "confidence": float(scores[idx]),
                    })
        except Exception:
            pass

    # Fallback to hardcoded
    if not results:
        FALLBACK = [
            {"scheme":"PM Kisan Samman Nidhi",          "confidence":0.91},
            {"scheme":"Ayushman Bharat – PM-JAY",        "confidence":0.88},
            {"scheme":"PM Awas Yojana (Gramin)",         "confidence":0.83},
            {"scheme":"Pradhan Mantri Ujjwala Yojana",   "confidence":0.79},
            {"scheme":"MGNREGA",                         "confidence":0.75},
            {"scheme":"PM Fasal Bima Yojana",            "confidence":0.69},
            {"scheme":"National Scholarship Portal",     "confidence":0.63},
            {"scheme":"PM Mudra Yojana",                 "confidence":0.58},
            {"scheme":"Atal Pension Yojana",             "confidence":0.54},
            {"scheme":"PM Jan Dhan Yojana",              "confidence":0.51},
        ]
        filtered = []
        for r in FALLBACK:
            s = r["scheme"]
            skip = False
            if "Kisan" in s and occupation not in ("Farmer / Agricultural worker","Self-employed / Small business"):
                skip = True
            if "Ujjwala" in s and has_lpg:
                skip = True
            if "Scholarship" in s and age > 35:
                skip = True
            if "Mudra" in s and occupation in ("Salaried (government)","Salaried (private)","Retired / Senior citizen"):
                skip = True
            if not skip:
                filtered.append(r)
        results = filtered or FALLBACK[:5]

    results.sort(key=lambda r: r["confidence"], reverse=True)
    st.session_state.results = results

    tier, color, dot = score_label(st.session_state.score)
    st.success(
        f"{dot} **Profile saved.** JanMitra Score: **{st.session_state.score} — {tier}**  "
        f"· {len(results)} schemes matched. "
        f"Go to **Eligible Schemes** to view your personalised list."
    )

    # ── Navigate to Eligible Schemes page ──────────────────────────────────
    st.switch_page("app_pages/eligible_schemes.py")
