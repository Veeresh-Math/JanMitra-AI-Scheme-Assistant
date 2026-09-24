"""Page 2 — Eligible Schemes (Premium cards with tiers, docs, benefits).
Bug #1 fix: schemes only show after st.session_state.submitted is True.
Bug #3 fix: replaced st.bar_chart(horizontal=True) with st.altair_chart.
Bug #6 fix: "All N matched schemes" heading gated behind submitted flag.
Bug #7 fix: renamed "Match %" column to "Match_pct" to avoid Vega-Lite issues.
Bug #9 fix: helpful empty-state message when results are empty after submit.
"""
import streamlit as st
import pandas as pd
import altair as alt

# ── Full scheme knowledge base ────────────────────────────────────────────────
SCHEME_DB = {
    "PM Kisan Samman Nidhi": {
        "emoji": "🌾", "category": "Agriculture", "ministry": "Ministry of Agriculture & Farmers Welfare",
        "benefit_headline": "₹6,000 / year",
        "benefit_detail": "Paid in 3 instalments of ₹2,000 directly to your bank account every 4 months.",
        "eligibility_plain": "Small and marginal farmers with cultivable land. Income below ₹2.5 LPA.",
        "docs": ["Aadhaar card (mandatory)", "Land ownership records / Khata (Jamabandi)", "Bank account passbook (account must be linked to Aadhaar)", "Mobile number linked to Aadhaar"],
        "time_to_apply": "15–20 min online",
        "link": "https://pmkisan.gov.in",
    },
    "Ayushman Bharat – PM-JAY": {
        "emoji": "🏥", "category": "Health", "ministry": "Ministry of Health & Family Welfare",
        "benefit_headline": "₹5 lakh health cover / year",
        "benefit_detail": "Cashless hospitalisation at 25,000+ empanelled hospitals. Covers surgery, ICU, medicines, and follow-up care.",
        "eligibility_plain": "Families listed in SECC 2011 database. Annual income below ₹5 LPA (varies by state).",
        "docs": ["Aadhaar card", "Ration card (BPL / SECC listed)", "Ayushman card (generated after eligibility check)", "Passbook for bank-linked verification"],
        "time_to_apply": "10 min at nearest CSC or hospital Ayushman counter",
        "link": "https://pmjay.gov.in",
    },
    "PM Awas Yojana (Gramin)": {
        "emoji": "🏠", "category": "Housing", "ministry": "Ministry of Rural Development",
        "benefit_headline": "₹1.20–1.30 lakh grant",
        "benefit_detail": "One-time housing grant to construct a pucca house. ₹1.20 lakh in plains, ₹1.30 lakh in hilly/northeastern states. Plus free LPG & toilet under convergence.",
        "eligibility_plain": "Rural households without a pucca house. Household must be in SECC 2011 priority list or BPL.",
        "docs": ["Aadhaar card", "SECC 2011 proof / BPL card", "Bank account passbook (DBT transfer)", "Geo-tagged photo of existing housing", "Consent letter (gram sabha approval)"],
        "time_to_apply": "Apply via gram panchayat / block office",
        "link": "https://pmayg.nic.in",
    },
    "Pradhan Mantri Ujjwala Yojana": {
        "emoji": "🔥", "category": "Energy", "ministry": "Ministry of Petroleum & Natural Gas",
        "benefit_headline": "Free LPG connection + ₹1,600 subsidy",
        "benefit_detail": "Free 14.2kg LPG cylinder connection. Deposit waiver + first refill free. Ongoing refill subsidy through DBT.",
        "eligibility_plain": "BPL women aged 18+ without an existing LPG connection. Ration card holders (AAY/BPL).",
        "docs": ["Aadhaar card", "BPL ration card / AAY card", "Bank account passbook", "Passport-size photo", "Self-declaration of no LPG connection"],
        "time_to_apply": "20 min at nearest LPG distributor",
        "link": "https://pmuy.gov.in",
    },
    "MGNREGA": {
        "emoji": "👷", "category": "Employment", "ministry": "Ministry of Rural Development",
        "benefit_headline": "100 days guaranteed employment",
        "benefit_detail": "Minimum wage employment (₹220–₹350/day depending on state) guaranteed for 100 days per financial year per rural household.",
        "eligibility_plain": "Any adult member of a rural household willing to do unskilled manual work.",
        "docs": ["Aadhaar card", "Job card (issued by gram panchayat)", "Bank or post office account passbook", "Residence proof in rural area"],
        "time_to_apply": "Visit gram panchayat for job card enrollment",
        "link": "https://nrega.nic.in",
    },
    "PM Fasal Bima Yojana": {
        "emoji": "🌱", "category": "Agriculture", "ministry": "Ministry of Agriculture",
        "benefit_headline": "Crop insurance at 1.5–5% premium",
        "benefit_detail": "Coverage for crop loss due to natural calamities, pests, and diseases. Farmer pays 1.5% premium for Rabi, 2% for Kharif; government subsidises the rest.",
        "eligibility_plain": "All farmers (owner and tenant) growing notified crops. KCC loan holders are enrolled automatically.",
        "docs": ["Aadhaar card", "Land records / crop sowing certificate", "Bank account passbook", "Khasra / Khatoni number", "Sowing declaration form"],
        "time_to_apply": "Apply before crop cut-off date at nearest bank/CSC",
        "link": "https://pmfby.gov.in",
    },
    "National Scholarship Portal": {
        "emoji": "🎓", "category": "Education", "ministry": "Ministry of Education",
        "benefit_headline": "₹5,000 – ₹75,000 / year",
        "benefit_detail": "Over 100 scholarship schemes for pre-matric, post-matric, and merit-cum-means categories. SC/ST/OBC/EWS/minority students get priority.",
        "eligibility_plain": "Students aged 18–35, enrolled in recognised institution. Income below ₹2.5 LPA (varies by scheme). SC/ST/OBC/EWS/minorities eligible for broader pool.",
        "docs": ["Aadhaar card", "Income certificate (from tehsildar/BDO)", "Caste certificate (for reserved category)", "Mark sheets of last qualifying exam", "Bonafide certificate from institution", "Bank account passbook (DBT-linked)"],
        "time_to_apply": "30 min online at scholarships.gov.in",
        "link": "https://scholarships.gov.in",
    },
    "PM Mudra Yojana": {
        "emoji": "💼", "category": "Finance", "ministry": "Ministry of Finance",
        "benefit_headline": "Loans ₹50,000 – ₹10 lakh",
        "benefit_detail": "Shishu (up to ₹50K), Kishore (₹50K–5L), Tarun (₹5L–10L). Collateral-free. Interest rates 8.5–12%. Repayment 3–7 years.",
        "eligibility_plain": "Non-corporate, non-farm micro/small enterprises. Any Indian citizen with a viable business plan. No minimum income requirement.",
        "docs": ["Aadhaar card + PAN card", "Business proof / registration (if any)", "Bank statement (6 months)", "Business plan / project report", "2 passport-size photos", "Address proof (utility bill/rental agreement)"],
        "time_to_apply": "Visit nearest bank, NBFC, or MFI",
        "link": "https://mudra.org.in",
    },
    "Sukanya Samriddhi Yojana": {
        "emoji": "👧", "category": "Women & Child", "ministry": "Ministry of Finance",
        "benefit_headline": "8.2% interest (tax-free)",
        "benefit_detail": "High-interest savings account for girl child. Minimum ₹250/year deposit. Maturity at 21 years or marriage after 18. Tax exemption under 80C.",
        "eligibility_plain": "Girl child below 10 years of age. Account opened by parent/guardian. Max 2 accounts per family.",
        "docs": ["Girl child's birth certificate", "Parent/guardian Aadhaar", "Parent/guardian PAN card", "Address proof", "2 passport-size photos of parent"],
        "time_to_apply": "20 min at nearest post office or authorised bank",
        "link": "https://www.indiapost.gov.in",
    },
    "Atal Pension Yojana": {
        "emoji": "👴", "category": "Pension", "ministry": "PFRDA",
        "benefit_headline": "₹1,000 – ₹5,000 / month pension",
        "benefit_detail": "Guaranteed pension of ₹1K–₹5K/month after age 60. Contribution ranges ₹42–₹1,454/month depending on age and pension level chosen.",
        "eligibility_plain": "Indian citizens aged 18–40 with a bank/post office account and mobile number. Not covered under any statutory pension scheme.",
        "docs": ["Aadhaar card", "Bank/post office passbook", "Mobile number linked to Aadhaar", "Nominee details (Aadhaar of spouse/nominee)"],
        "time_to_apply": "10 min at nearest bank branch",
        "link": "https://npscra.nsdl.co.in",
    },
    "PM Jan Dhan Yojana": {
        "emoji": "🏦", "category": "Banking", "ministry": "Ministry of Finance",
        "benefit_headline": "Zero balance account + ₹2 lakh accident cover",
        "benefit_detail": "Zero-minimum-balance savings account with RuPay debit card. Accident insurance cover ₹2 lakh, life insurance ₹30,000. Overdraft facility up to ₹10,000.",
        "eligibility_plain": "Any Indian citizen without a bank account (unbanked). No minimum balance required.",
        "docs": ["Aadhaar card (primary KYC)", "Passport-size photo", "Address proof if Aadhaar address differs"],
        "time_to_apply": "15 min at nearest bank branch",
        "link": "https://pmjdy.gov.in",
    },
    "PM SVANidhi": {
        "emoji": "🛒", "category": "Urban Livelihood", "ministry": "Ministry of Housing & Urban Affairs",
        "benefit_headline": "Working capital loan ₹10,000 – ₹50,000",
        "benefit_detail": "Collateral-free loans: ₹10K (1st), ₹20K (2nd), ₹50K (3rd tranche). 7% interest subsidy. Digital transaction incentive ₹1,200/year.",
        "eligibility_plain": "Street vendors in urban areas with vending certificate or letter of recommendation from Urban Local Body.",
        "docs": ["Aadhaar card", "Vending certificate / Identity card from ULB", "Bank account passbook", "Mobile number for digital payments"],
        "time_to_apply": "Apply online at pmsvanidhi.mohua.gov.in",
        "link": "https://pmsvanidhi.mohua.gov.in",
    },
    "PM Garib Kalyan Anna Yojana": {
        "emoji": "🌾", "category": "Food Security", "ministry": "Ministry of Food & Public Distribution",
        "benefit_headline": "5 kg free grain / person / month",
        "benefit_detail": "5 kg rice or wheat per person per month free of cost under National Food Security Act. Delivered through ration shop (PDS).",
        "eligibility_plain": "Households listed under National Food Security Act. BPL / AAY ration card holders.",
        "docs": ["Ration card (BPL/AAY)", "Aadhaar card (eKYC at ration shop)", "Family member details"],
        "time_to_apply": "Automatic — visit your designated ration shop",
        "link": "https://dfpd.gov.in",
    },
    "PM Matru Vandana Yojana": {
        "emoji": "🤱", "category": "Women & Child", "ministry": "Ministry of Women & Child Development",
        "benefit_headline": "₹5,000 maternity benefit",
        "benefit_detail": "₹3,000 on early registration of pregnancy, ₹2,000 after 1st child's birth and immunisation. Paid directly to mother's bank account.",
        "eligibility_plain": "Pregnant and lactating women aged 19+ for first live birth. Annual income not specified — universally applicable.",
        "docs": ["Aadhaar card", "Mother's bank account passbook (DBT)", "MCP card (Mother & Child Protection card)", "Pregnancy registration certificate from ASHA/ANM"],
        "time_to_apply": "Register at nearest Anganwadi centre or health sub-centre",
        "link": "https://wcd.nic.in",
    },
    "Kisan Credit Card": {
        "emoji": "💳", "category": "Agriculture", "ministry": "Ministry of Agriculture",
        "benefit_headline": "Crop loan at 4% interest",
        "benefit_detail": "Short-term credit for crop cultivation, post-harvest, allied activities. Interest subvention reduces rate to 4%. Limit up to ₹3 lakh for KCC.",
        "eligibility_plain": "Farmers (owner cultivators, tenant farmers, sharecroppers, SHG members). Land ownership or tenancy proof needed.",
        "docs": ["Aadhaar card", "Land ownership / tenancy documents", "Bank account passbook", "Two passport-size photos", "Crop cultivation proof"],
        "time_to_apply": "Apply at nearest cooperative / nationalised bank",
        "link": "https://pmkisan.gov.in",
    },
}

def tier_config(confidence):
    if confidence >= 0.80:
        return "Excellent Match", "#34c759", "#f0fdf4", "★★★"
    if confidence >= 0.60:
        return "Good Match",      "#0071e3", "#eff6ff", "★★☆"
    if confidence >= 0.40:
        return "Possible Match",  "#ff9f0a", "#fffbeb", "★☆☆"
    return "Review Required",     "#8e8e93", "#f5f5f7", "☆☆☆"

# ── Bug #1 fix: gate on both profile AND submitted flag ───────────────────────
profile   = st.session_state.get("profile", {})
submitted = st.session_state.get("submitted", False)
results   = st.session_state.get("results", [])
score     = st.session_state.get("score", 0)

if not profile or not profile.get("age") or not submitted:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px">
      <div style="font-size:48px;margin-bottom:16px">🇮🇳</div>
      <h2 style="color:#1d1d1f;margin-bottom:8px">Start with your profile</h2>
      <p style="color:#6e6e73;font-size:16px;max-width:400px;margin:0 auto">
        Go to <strong>My Profile</strong> and fill in your details.
        JanMitra will find every scheme you qualify for.
      </p>
    </div>""", unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("Quick-start sample profile")
        sample_profile = {
            "age": 30,
            "gender": "Female",
            "marital": "Married",
            "family_size": 4,
            "disability": False,
            "state": "Karnataka",
            "social_category": "General",
            "area_type": "Urban",
            "occupation": "Student",
            "ration_card": "None",
            "monthly_income": 0,
            "other_income": 0,
            "annual_income": 0,
            "land_acres": 0.0,
            "has_bank": True,
            "has_aadhaar": True,
            "has_house": False,
            "has_lpg": False,
            "has_kcc": False,
        }

        sample_score = (
            0.38 * (1 - min(sample_profile["annual_income"] / 1_000_000, 1))
            + 0.26 * min(abs(sample_profile["age"] - 40) / 40, 1)
            + 0.24 * {"SC": 1.0, "ST": 1.0, "OBC": 0.7, "EWS": 0.8, "General": 0.2}.get(
                sample_profile["social_category"], 0.5
            )
        )
        sample_score = min(int(sample_score * 100), 99)

        st.metric("Sample eligibility score", f"{sample_score}%")
        st.caption("Use this non-sensitive demo profile to preview all three pages.")
        if st.button("Load Sample Profile", type="primary"):
            st.session_state.profile = sample_profile
            st.session_state.score = sample_score
            st.session_state.results = [
                {"scheme": "PM Kisan Samman Nidhi", "confidence": 0.91},
                {"scheme": "Ayushman Bharat – PM-JAY", "confidence": 0.88},
                {"scheme": "PM Awas Yojana (Gramin)", "confidence": 0.83},
                {"scheme": "Pradhan Mantri Ujjwala Yojana", "confidence": 0.79},
                {"scheme": "MGNREGA", "confidence": 0.75},
                {"scheme": "National Scholarship Portal", "confidence": 0.63},
                {"scheme": "PM Jan Dhan Yojana", "confidence": 0.51},
            ]
            st.session_state.submitted = True
            st.rerun()

    st.stop()

# ── Score hero banner ──────────────────────────────────────────────────────────
if score >= 80:   s_color, s_label, s_bg = "#34c759", "Excellent", "#f0fdf4"
elif score >= 60: s_color, s_label, s_bg = "#0071e3", "Good",      "#eff6ff"
elif score >= 40: s_color, s_label, s_bg = "#ff9f0a", "Moderate",  "#fffbeb"
else:             s_color, s_label, s_bg = "#8e8e93", "Basic",     "#f5f5f7"

st.markdown(f"""
<div style="background:{s_bg};border:1.5px solid {s_color}30;border-radius:20px;
            padding:24px 28px;margin-bottom:28px;display:flex;align-items:center;gap:24px">
  <div style="background:{s_color};border-radius:50%;width:68px;height:68px;
              display:flex;align-items:center;justify-content:center;
              color:#fff;font-size:26px;font-weight:800;flex-shrink:0">{score}</div>
  <div style="flex:1">
    <div style="font-size:22px;font-weight:700;color:#1d1d1f;letter-spacing:-0.02em">
      JanMitra Score: <span style="color:{s_color}">{s_label}</span>
    </div>
    <div style="font-size:14px;color:#6e6e73;margin-top:4px">
      {len(results)} schemes matched &nbsp;·&nbsp;
      {profile.get("state","—")} &nbsp;·&nbsp;
      ₹{profile.get("annual_income",0):,} annual income &nbsp;·&nbsp;
      {profile.get("social_category","—")} category
    </div>
  </div>
  <div style="text-align:right;flex-shrink:0">
    <div style="font-size:12px;color:#6e6e73;margin-bottom:4px">Eligibility potential</div>
    <div style="font-size:28px;font-weight:700;color:{s_color}">{score}%</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Profile summary ────────────────────────────────────────────────────────────
with st.expander("Your profile summary", expanded=False):
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Age",       f"{profile.get('age','—')} yrs")
    c2.metric("Income",    f"₹{profile.get('annual_income',0):,}")
    c3.metric("State",     profile.get("state","—"))
    c4.metric("Category",  profile.get("social_category","—"))
    c5.metric("Family",    f"{profile.get('family_size','—')} members")

# ── Bug #9: empty state after submit ─────────────────────────────────────────
if not results:
    st.info(
        "**No schemes matched your profile.** "
        "This can happen if the AI model returned no predictions. "
        "Try going back to **My Profile** and broadening your inputs, "
        "or check the **Ask JanMitra** tab for manual guidance."
    )
    st.stop()

# ── Confidence bar chart (top 5) — Bug #3 & #7 fix: altair + safe column name ─
top5 = results[:5]
chart_df = pd.DataFrame({
    "Scheme":    [r["scheme"][:32] + ("…" if len(r["scheme"]) > 32 else "") for r in top5],
    "Match_pct": [round(r["confidence"] * 100, 1) for r in top5],         # Bug #7: no %
})

with st.container(border=True):
    st.markdown("**Top 5 by match confidence**")
    # Bug #3 fix: altair chart instead of st.bar_chart for reliable horizontal bars
    chart = (
        alt.Chart(chart_df)
        .mark_bar(color="#0071e3", cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            y=alt.Y("Scheme:N", sort="-x", axis=alt.Axis(labelLimit=200), title=None),
            x=alt.X("Match_pct:Q", scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(title="Match confidence (%)", grid=False)),
            tooltip=[
                alt.Tooltip("Scheme:N", title="Scheme"),
                alt.Tooltip("Match_pct:Q", title="Match %", format=".1f"),
            ],
        )
        .properties(height=max(150, 40 * len(top5)), background="#ffffff")
        .configure_view(stroke=None)
        .configure_axis(labelFontSize=12, titleFontSize=12)
    )
    st.altair_chart(chart, use_container_width=True)

# ── Bug #6 fix: heading now only shown after submitted & results exist ─────────
st.markdown(f"### All {len(results)} matched schemes")

# ── Scheme cards ───────────────────────────────────────────────────────────────
for r in results:
    name       = r["scheme"]
    confidence = r["confidence"]
    db         = SCHEME_DB.get(name, {})
    tier_label, tier_color, tier_bg, stars = tier_config(confidence)
    pct        = int(confidence * 100)
    emoji      = db.get("emoji", "📋")
    cat        = db.get("category", "Government Scheme")
    ministry   = db.get("ministry", "Government of India")
    b_head     = db.get("benefit_headline", "—")
    b_detail   = db.get("benefit_detail", "Welfare benefit as per scheme guidelines.")
    e_plain    = db.get("eligibility_plain", "As per official eligibility criteria.")
    docs       = db.get("docs", ["Aadhaar card", "Bank account passbook", "Relevant certificates"])
    tat        = db.get("time_to_apply", "Varies")
    link       = db.get("link", "https://india.gov.in")

    with st.container(border=True):
        # Header row
        h1c, h2c = st.columns([4, 1])
        with h1c:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px">
              <span style="font-size:26px">{emoji}</span>
              <div>
                <div style="font-size:17px;font-weight:700;color:#1d1d1f;letter-spacing:-0.01em">{name}</div>
                <div style="font-size:12px;color:#6e6e73;margin-top:1px">{cat} &nbsp;·&nbsp; {ministry}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        with h2c:
            st.markdown(f"""
            <div style="text-align:right">
              <div style="display:inline-block;background:{tier_bg};color:{tier_color};
                          border:1px solid {tier_color}40;border-radius:20px;
                          padding:3px 12px;font-size:12px;font-weight:600;margin-bottom:6px">
                {stars} {tier_label}
              </div><br>
              <span style="font-size:24px;font-weight:800;color:{tier_color}">{pct}%</span>
              <span style="font-size:11px;color:#6e6e73"> match</span>
            </div>""", unsafe_allow_html=True)

        st.progress(confidence)

        # Three info columns
        col_b, col_e, col_t = st.columns(3)
        with col_b:
            st.markdown(f"""
            <div style="background:#f5f5f7;border-radius:12px;padding:12px 14px;height:100%">
              <div style="font-size:10px;font-weight:700;letter-spacing:.07em;
                          text-transform:uppercase;color:#6e6e73;margin-bottom:5px">💰 Benefit</div>
              <div style="font-size:16px;font-weight:700;color:#1d1d1f">{b_head}</div>
              <div style="font-size:12px;color:#6e6e73;margin-top:4px;line-height:1.5">{b_detail}</div>
            </div>""", unsafe_allow_html=True)
        with col_e:
            st.markdown(f"""
            <div style="background:#f5f5f7;border-radius:12px;padding:12px 14px;height:100%">
              <div style="font-size:10px;font-weight:700;letter-spacing:.07em;
                          text-transform:uppercase;color:#6e6e73;margin-bottom:5px">✅ Eligibility</div>
              <div style="font-size:12px;color:#1d1d1f;line-height:1.6">{e_plain}</div>
            </div>""", unsafe_allow_html=True)
        with col_t:
            docs_html = "".join(
                f'<div style="display:flex;align-items:flex-start;gap:6px;margin-bottom:3px">'
                f'<span style="color:#0071e3;flex-shrink:0;margin-top:1px">›</span>'
                f'<span style="font-size:11.5px;color:#1d1d1f">{d}</span></div>'
                for d in docs
            )
            st.markdown(f"""
            <div style="background:#f5f5f7;border-radius:12px;padding:12px 14px;height:100%">
              <div style="font-size:10px;font-weight:700;letter-spacing:.07em;
                          text-transform:uppercase;color:#6e6e73;margin-bottom:5px">📋 Documents needed</div>
              {docs_html}
              <div style="margin-top:8px;font-size:11px;color:#0071e3;font-weight:500">
                ⏱ {tat}
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.link_button(f"Apply on official portal →", link)
        st.markdown("<hr style='margin:12px 0 0'>", unsafe_allow_html=True)
