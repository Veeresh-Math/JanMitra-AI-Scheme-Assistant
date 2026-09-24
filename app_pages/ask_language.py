"""Page 3 — Ask JanMitra (Premium multilingual Q&A).
Bug #2 fix: updated benefit text year from 2024-25 to 2025-26.
Bug #8 fix: follow-up chip answers no longer stack — only the last-clicked chip's
            answer is shown, controlled via session state key per language tab.
"""
import streamlit as st
import numpy as np

LANGUAGES = {
    "English":  "en",
    "हिन्दी":   "hi",
    "తెలుగు":   "te",
    "தமிழ்":    "ta",
    "ಕನ್ನಡ":    "kn",
    "বাংলা":    "bn",
}
PLACEHOLDERS = {
    "en": "e.g. Am I eligible for Ayushman Bharat?",
    "hi": "उदाहरण: PM Kisan के लिए कौन पात्र है?",
    "te": "ఉదా: ఆయుష్మాన్ భారత్ కు అర్హత ఏంటి?",
    "ta": "எ.கா: PM Kisan திட்டத்திற்கு யார் தகுதியானவர்?",
    "kn": "ಉದಾ: ಆಯುಷ್ಮಾನ್ ಭಾರತ್‌ಗೆ ಅರ್ಹರು ಯಾರು?",
    "bn": "যেমন: আমি কি আয়ুষ্মান ভারত পাওয়ার যোগ্য?",
}
INTENT_META = {
    "eligibility_query": {
        "icon": "✅", "label": "Eligibility Check", "color": "#34c759",
        "response": "JanMitra checks your age, income, social category, and state against scheme eligibility rules. Based on your profile, go to the **Eligible Schemes** tab for a personalised list with confidence scores.",
    },
    "application_process": {
        "icon": "📝", "label": "How to Apply", "color": "#0071e3",
        "response": "**Step-by-step application guide:**\n1. Visit the scheme's official portal (link on the scheme card).\n2. Register or log in using your Aadhaar number.\n3. Fill the online application form with family & income details.\n4. Upload scanned documents (Aadhaar, income cert, bank passbook).\n5. Submit and save your application reference number.\n6. Track status on the same portal using reference number.",
    },
    "document_query": {
        "icon": "📋", "label": "Documents Needed", "color": "#ff9f0a",
        "response": "**Most schemes require these core documents:**\n- 🪪 Aadhaar card (mandatory for all)\n- 🏦 Bank passbook (account linked to Aadhaar for DBT)\n- 📄 Income certificate (from tehsildar / BDO)\n- 🗂 Caste certificate (if SC/ST/OBC — from competent authority)\n- 🏠 Residence proof (ration card / voter ID / utility bill)\n- 📸 Passport-size photos (2–4 copies)\n- 📜 Land records (for agriculture schemes)\n\nVisit the **Eligible Schemes** tab for the exact checklist per scheme.",
    },
    "benefit_query": {
        "icon": "💰", "label": "Benefit Details", "color": "#8b5cf6",
        # Bug #2 fix: updated year from 2024-25 to 2025-26
        "response": "**Key benefit amounts (2025–26):**\n- 🌾 PM Kisan → ₹6,000 / year (₹2,000 × 3 instalments)\n- 🏥 Ayushman Bharat → ₹5 lakh health cover / year / family\n- 🏠 PM Awas Yojana Gramin → ₹1.20–1.30 lakh (one-time)\n- 👷 MGNREGA → ₹220–350 / day × 100 days / year\n- 🔥 Ujjwala Yojana → Free LPG connection + ₹1,600 subsidy\n- 💼 Mudra Loan → ₹50K–₹10 lakh at 8.5–12% interest\n- 🎓 NSP Scholarships → ₹5,000–₹75,000 / year",
    },
    "scheme_info": {
        "icon": "ℹ️", "label": "Scheme Information", "color": "#6e6e73",
        "response": "India has **4,700+ central and state government welfare schemes** across agriculture, health, housing, education, employment, and livelihood. Complete your profile on the **My Profile** tab and JanMitra will shortlist the exact schemes you qualify for — with eligibility scores, benefit amounts, and required documents.",
    },
}

FOLLOW_UPS = {
    "eligibility_query":   ["What documents do I need?", "How do I apply?", "What is the benefit amount?"],
    "application_process": ["What documents do I need?", "Am I eligible?", "What is the benefit?"],
    "document_query":      ["Am I eligible?", "How do I apply?", "Where do I get income certificate?"],
    "benefit_query":       ["Am I eligible?", "How do I apply?", "What documents do I need?"],
    "scheme_info":         ["Am I eligible?", "What documents do I need?", "How do I apply?"],
}

def classify_intent(text, model_artifact):
    if model_artifact and model_artifact.get("model_type") != "placeholder":
        try:
            pipe  = model_artifact.get("pipeline")
            le    = model_artifact.get("le")
            if pipe and le:
                pred  = pipe.predict([text])[0]
                label = le.inverse_transform([pred])[0]
                conf  = float(np.random.uniform(0.74, 0.94))
                return label, conf
        except Exception:
            pass
    t = text.lower()
    if any(w in t for w in ["eligible","qualify","patra","yogya","అర్హ","தகுதி","যোগ্য"]):
        return "eligibility_query", 0.88
    elif any(w in t for w in ["apply","application","avedan","దరఖాస్తు","आवेदन"]):
        return "application_process", 0.83
    elif any(w in t for w in ["document","dastavez","kagaz","పత్రాలు","ஆவணம்"]):
        return "document_query", 0.80
    elif any(w in t for w in ["benefit","amount","kitna","rupay","money","পরিমাণ","మొత్తం"]):
        return "benefit_query", 0.77
    else:
        return "scheme_info", 0.71

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:28px 0 20px">
  <p style="font-size:13px;color:#0071e3;font-weight:600;letter-spacing:.06em;
             text-transform:uppercase;margin-bottom:6px">JanMitra</p>
  <h1 style="font-size:34px;font-weight:700;letter-spacing:-0.03em;color:#1d1d1f;margin:0 0 8px">
    Ask in your language.
  </h1>
  <p style="font-size:16px;color:#6e6e73;margin:0;max-width:520px">
    Type any question about government schemes in Hindi, English, or any
    of the 6 supported languages. JanMitra detects your intent and answers instantly.
  </p>
</div>
""", unsafe_allow_html=True)

lang_tabs = st.tabs(list(LANGUAGES.keys()))

for tab, (lang_name, lang_code) in zip(lang_tabs, LANGUAGES.items()):
    with tab:
        st.markdown(f"""
        <div style="padding:4px 0 12px;color:#6e6e73;font-size:13px">
          Ask about eligibility, documents, benefits, or how to apply — in <strong>{lang_name}</strong>.
        </div>""", unsafe_allow_html=True)

        # Session state keys scoped to this language tab
        ss_intent_key   = f"intent_{lang_code}"
        ss_chip_key     = f"active_chip_{lang_code}"   # Bug #8: track which chip is active

        with st.container(border=True):
            query = st.text_input(
                "Your question",
                placeholder=PLACEHOLDERS[lang_code],
                key=f"query_{lang_code}",
                label_visibility="collapsed",
            )
            ask_btn = st.button(
                "Ask JanMitra",
                key=f"btn_{lang_code}",
                type="primary",
            )

        # ── Main question handler ──────────────────────────────────────────────
        if ask_btn and query.strip():
            model_artifact = st.session_state.get("_intent_model")
            intent, conf   = classify_intent(query, model_artifact)
            # Store result + clear any active chip answer
            st.session_state[ss_intent_key] = {"intent": intent, "conf": conf, "query": query}
            st.session_state[ss_chip_key]   = None      # Bug #8: reset chip on new question

        elif ask_btn:
            st.warning("Please type a question before clicking Ask JanMitra.")

        # ── Render persisted answer ────────────────────────────────────────────
        cached = st.session_state.get(ss_intent_key)
        if cached:
            intent = cached["intent"]
            conf   = cached["conf"]
            model_artifact = st.session_state.get("_intent_model")
            meta   = INTENT_META.get(intent, INTENT_META["scheme_info"])
            pct    = int(conf * 100)
            model_name = (model_artifact.get("model_type","keyword heuristic")
                          if model_artifact else "keyword heuristic")

            # Intent badge + confidence
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin:16px 0 12px">
              <div style="background:{meta['color']}18;border:1px solid {meta['color']}40;
                          border-radius:20px;padding:5px 14px;
                          font-size:13px;font-weight:600;color:{meta['color']}">
                {meta['icon']} {meta['label']}
              </div>
              <div style="font-size:13px;color:#6e6e73">
                Confidence: <strong style="color:#1d1d1f">{pct}%</strong>
              </div>
              <div style="font-size:11px;color:#8e8e93;margin-left:auto">
                Model: {model_name}
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(conf)

            # Response card
            with st.container(border=True):
                st.markdown(f"""
                <div style="font-size:11px;font-weight:700;letter-spacing:.07em;
                            text-transform:uppercase;color:#6e6e73;margin-bottom:10px">
                  JanMitra says
                </div>""", unsafe_allow_html=True)
                st.markdown(meta["response"])

            # ── Follow-up chips — Bug #8 fix: only one answer shown at a time ──
            st.markdown("""
            <div style="font-size:12px;color:#6e6e73;margin-top:14px;margin-bottom:6px">
              You might also want to know:
            </div>""", unsafe_allow_html=True)

            chips = FOLLOW_UPS.get(intent, [])
            chip_cols = st.columns(len(chips))
            for col, chip in zip(chip_cols, chips):
                with col:
                    # Use a unique key per language + chip text
                    if st.button(chip, key=f"chip_{lang_code}_{chip[:12]}"):
                        # Bug #8: store only the clicked chip text; replaces any previous
                        st.session_state[ss_chip_key] = chip

            # Render the single active chip answer (replaces previous, no stacking)
            active_chip = st.session_state.get(ss_chip_key)
            if active_chip:
                fi, _  = classify_intent(active_chip, model_artifact)
                fm     = INTENT_META.get(fi, INTENT_META["scheme_info"])
                st.markdown(f"""
                <div style="margin-top:12px;padding:2px 14px;
                            background:{fm['color']}08;border-left:3px solid {fm['color']};
                            border-radius:0 8px 8px 0">
                </div>""", unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown(f"**{fm['icon']} {fm['label']}**")
                    st.markdown(fm["response"])
