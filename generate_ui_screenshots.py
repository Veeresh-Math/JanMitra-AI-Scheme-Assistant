"""
Generate synthetic but realistic UI screenshots of the 3 JanMitra pages.
Uses matplotlib to render pixel-perfect UI mockups that look like the real app.
Saves to reports/figures/ as 11_ui_page1_profile.png, 12_ui_page2_schemes.png, 13_ui_page3_ask.png
"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np

FIGDIR = os.path.join(os.path.dirname(__file__), "reports", "figures")
DPI = 150

# colour palette
BG       = "#f5f5f7"
WHITE    = "#ffffff"
BLUE     = "#0071e3"
GREEN    = "#34c759"
AMBER    = "#ff9f0a"
GRAY     = "#6e6e73"
DARK     = "#1d1d1f"
BORDER   = "#e5e5ea"
BLUE_LT  = "#eff6ff"

def nav_bar(ax, active=0):
    """Draw navigation bar."""
    ax.add_patch(FancyBboxPatch((0, 0.935), 1, 0.065,
        boxstyle="square,pad=0", fc=WHITE, ec=BORDER, lw=0.8,
        transform=ax.transAxes, clip_on=False))
    ax.text(0.03, 0.968, "JanMitra", transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=BLUE, va="center")
    pages = ["My Profile", "Eligible Schemes", "Ask JanMitra"]
    xs = [0.22, 0.42, 0.62]
    for i, (x, pg) in enumerate(zip(xs, pages)):
        if i == active:
            ax.add_patch(FancyBboxPatch((x-0.07, 0.942), 0.14, 0.052,
                boxstyle="round,pad=0.01", fc=BLUE_LT, ec=BORDER, lw=0.6,
                transform=ax.transAxes))
            ax.text(x, 0.968, pg, transform=ax.transAxes, fontsize=8,
                    fontweight="bold", color=BLUE, va="center", ha="center")
        else:
            ax.text(x, 0.968, pg, transform=ax.transAxes, fontsize=8,
                    color=GRAY, va="center", ha="center")

def input_box(ax, x, y, w, h, label, value, transform):
    """Draw a labelled input field."""
    ax.text(x, y+h+0.008, label, transform=transform, fontsize=7,
            color=DARK, fontweight="600", va="bottom")
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.005", fc=WHITE, ec="#d2d2d7", lw=0.8,
        transform=transform))
    ax.text(x+0.015, y+h*0.5, value, transform=transform, fontsize=8,
            color=DARK, va="center")

def card(ax, x, y, w, h, transform, fc=WHITE, ec=BORDER, lw=0.8, radius=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad={radius}", fc=fc, ec=ec, lw=lw, transform=transform))

def progress_bar(ax, x, y, w, h, pct, color, transform):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0", fc="#e5e5ea", ec="none", transform=transform))
    ax.add_patch(FancyBboxPatch((x, y), w*pct, h,
        boxstyle="round,pad=0", fc=color, ec="none", transform=transform))

# ═══════════════════════════════════════════════════════════════════
# PAGE 1 — My Profile
# ═══════════════════════════════════════════════════════════════════
print("Generating 11_ui_page1_profile.png ...")
fig, ax = plt.subplots(figsize=(10, 13))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.axis("off")
t = ax.transAxes

nav_bar(ax, active=0)

# Hero text
ax.text(0.05, 0.91, "JANMITRA", transform=t, fontsize=8, fontweight="bold",
        color=BLUE)
ax.text(0.05, 0.87, "Find your government benefits.", transform=t,
        fontsize=16, fontweight="bold", color=DARK)
ax.text(0.05, 0.83, "Tell JanMitra about yourself — it matches you with every scheme you qualify for.",
        transform=t, fontsize=9, color=GRAY)

# Section A
ax.text(0.05, 0.800, "A · PERSONAL DETAILS", transform=t,
        fontsize=7, fontweight="bold", color=GRAY, alpha=0.9)
input_box(ax, 0.05, 0.745, 0.27, 0.038, "Age", "30 years", t)
input_box(ax, 0.36, 0.745, 0.27, 0.038, "Gender", "Male", t)
input_box(ax, 0.67, 0.745, 0.27, 0.038, "Marital Status", "Married", t)
input_box(ax, 0.05, 0.688, 0.27, 0.038, "Family Size", "4 members", t)

# Checkbox
ax.add_patch(FancyBboxPatch((0.36, 0.695), 0.022, 0.022,
    boxstyle="round,pad=0.003", fc=WHITE, ec="#d2d2d7", lw=0.8, transform=t))
ax.text(0.39, 0.707, "Person with disability (PwD)", transform=t, fontsize=8, color=DARK, va="center")

# Section B
ax.text(0.05, 0.665, "B · LOCATION & CATEGORY", transform=t,
        fontsize=7, fontweight="bold", color=GRAY, alpha=0.9)
input_box(ax, 0.05, 0.610, 0.36, 0.038, "State / Union Territory", "Karnataka", t)
input_box(ax, 0.44, 0.610, 0.25, 0.038, "Social Category", "OBC", t)
input_box(ax, 0.72, 0.610, 0.22, 0.038, "Area Type", "Rural", t)

# Section C
ax.text(0.05, 0.585, "C · OCCUPATION & EARNINGS", transform=t,
        fontsize=7, fontweight="bold", color=GRAY, alpha=0.9)
input_box(ax, 0.05, 0.530, 0.42, 0.038, "Primary Occupation", "Farmer / Agricultural worker", t)
input_box(ax, 0.51, 0.530, 0.42, 0.038, "Ration Card Type", "BPL (Below Poverty Line)", t)
input_box(ax, 0.05, 0.473, 0.27, 0.038, "Monthly Income (Rs.)", "12,000", t)
input_box(ax, 0.36, 0.473, 0.27, 0.038, "Other Annual Income", "0", t)
input_box(ax, 0.67, 0.473, 0.27, 0.038, "Land Holding (acres)", "2.5", t)

# Section D
ax.text(0.05, 0.445, "D · EXISTING ASSETS & ENTITLEMENTS", transform=t,
        fontsize=7, fontweight="bold", color=GRAY, alpha=0.9)
for i, (label, checked) in enumerate([
    ("Has bank account", True), ("Has Aadhaar card", True),
    ("Owns house", False), ("Has LPG connection", False), ("Has Kisan Credit Card", False)
]):
    xp = 0.05 + (i % 3) * 0.31
    yp = 0.415 - (i // 3) * 0.042
    fc = BLUE if checked else WHITE
    ec = BLUE if checked else "#d2d2d7"
    ax.add_patch(FancyBboxPatch((xp, yp), 0.020, 0.020,
        boxstyle="round,pad=0.003", fc=fc, ec=ec, lw=0.8, transform=t))
    if checked:
        ax.text(xp+0.010, yp+0.010, "✓", transform=t, fontsize=6,
                color=WHITE, ha="center", va="center", fontweight="bold")
    ax.text(xp+0.028, yp+0.010, label, transform=t, fontsize=8, color=DARK, va="center")

# Live Score Preview Card
card(ax, 0.05, 0.280, 0.90, 0.090, t, fc=WHITE, ec="#e0e0e8", lw=0.6)
# Score circle
circle = plt.Circle((0.13, 0.325), 0.040, transform=t,
                     color=GREEN, zorder=5)
ax.add_patch(circle)
ax.text(0.130, 0.325, "72", transform=t, fontsize=13, fontweight="bold",
        color=WHITE, ha="center", va="center", zorder=6)
ax.text(0.21, 0.342, "JanMitra Score: Good", transform=t,
        fontsize=10, fontweight="bold", color=GREEN, va="center")
ax.text(0.21, 0.315, "Based on your inputs, you likely qualify for 5 or more government schemes.",
        transform=t, fontsize=8.5, color=GRAY, va="center")
ax.text(0.21, 0.298, "Click below to see your full personalised list.",
        transform=t, fontsize=8.5, color=GRAY, va="center")

# Submit button
ax.add_patch(FancyBboxPatch((0.05, 0.235), 0.90, 0.040,
    boxstyle="round,pad=0.01", fc=BLUE, ec="none", transform=t))
ax.text(0.50, 0.256, "Find My Schemes  →", transform=t,
        fontsize=11, fontweight="bold", color=WHITE, ha="center", va="center")

# footer
ax.plot([0,1], [0.020, 0.020], color=BORDER, lw=0.8, transform=t)
ax.text(0.50, 0.010, "Built by VeereshMath  ·  AICTE  ·  IBM SkillsBuild  ·  BharatCares  ·  2026",
        transform=t, fontsize=7, color=GRAY, ha="center", va="center")

plt.tight_layout(rect=[0,0,1,1])
fig.savefig(os.path.join(FIGDIR, "11_ui_page1_profile.png"), dpi=DPI,
            bbox_inches="tight", facecolor=BG)
plt.close()

# ═══════════════════════════════════════════════════════════════════
# PAGE 2 — Eligible Schemes
# ═══════════════════════════════════════════════════════════════════
print("Generating 12_ui_page2_schemes.png ...")
fig, ax = plt.subplots(figsize=(10, 15))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.axis("off")
t = ax.transAxes

nav_bar(ax, active=1)

# Score hero banner
card(ax, 0.04, 0.895, 0.92, 0.082, t, fc="#f0fdf4", ec="#34c75930", lw=1.2)
circle2 = plt.Circle((0.11, 0.936), 0.040, transform=t, color=GREEN, zorder=5)
ax.add_patch(circle2)
ax.text(0.110, 0.936, "72", transform=t, fontsize=14, fontweight="bold",
        color=WHITE, ha="center", va="center", zorder=6)
ax.text(0.20, 0.950, "JanMitra Score:", transform=t, fontsize=12,
        fontweight="bold", color=DARK, va="center")
ax.text(0.41, 0.950, "Good", transform=t, fontsize=12,
        fontweight="bold", color=GREEN, va="center")
ax.text(0.20, 0.924, "8 schemes matched  ·  Karnataka  ·  Rs.1,44,000 annual income  ·  OBC category",
        transform=t, fontsize=8.5, color=GRAY, va="center")
ax.text(0.88, 0.960, "72%", transform=t, fontsize=18, fontweight="bold",
        color=GREEN, ha="center", va="center")
ax.text(0.88, 0.910, "Eligibility", transform=t, fontsize=8,
        color=GRAY, ha="center", va="center")

# Profile summary expander
card(ax, 0.04, 0.848, 0.92, 0.040, t, fc=WHITE, ec=BORDER, lw=0.7)
ax.text(0.08, 0.868, "Your profile summary  ▾", transform=t, fontsize=9,
        fontweight="bold", color=DARK, va="center")

# Top-5 chart card
card(ax, 0.04, 0.765, 0.92, 0.078, t, fc=WHITE, ec=BORDER, lw=0.7)
ax.text(0.07, 0.832, "Top 5 by match confidence", transform=t,
        fontsize=9, fontweight="bold", color=DARK)

schemes_top5 = [
    ("PM Kisan Samman Nidhi",   0.91),
    ("Ayushman Bharat - PM-JAY",0.88),
    ("PM Awas Yojana (Gramin)", 0.83),
    ("Pradhan Mantri Ujjwala",  0.79),
    ("MGNREGA",                 0.75),
]
for i, (name, conf) in enumerate(schemes_top5):
    yrow = 0.818 - i*0.011
    ax.text(0.07, yrow - 0.004, name, transform=t, fontsize=7.5, color=DARK, va="center")
    progress_bar(ax, 0.30, yrow-0.006, 0.52, 0.007, conf, BLUE, t)
    ax.text(0.84, yrow-0.002, f"{int(conf*100)}%", transform=t, fontsize=7.5,
            fontweight="bold", color=BLUE, va="center")

ax.text(0.05, 0.748, f"All 8 matched schemes", transform=t,
        fontsize=11, fontweight="bold", color=DARK)

# Scheme card 1 — PM Kisan
SCHEMES = [
    ("PM Kisan Samman Nidhi",        "Rs.6,000/year",       0.91, GREEN, "Agriculture", "Excellent Match",  "★★★"),
    ("Ayushman Bharat - PM-JAY",     "Rs.5 lakh cover/yr",  0.88, GREEN, "Health",      "Excellent Match",  "★★★"),
    ("PM Awas Yojana (Gramin)",      "Rs.1.20-1.30L grant", 0.83, GREEN, "Housing",     "Excellent Match",  "★★★"),
    ("MGNREGA",                       "100 days employment", 0.75, BLUE,  "Employment",  "Good Match",       "★★☆"),
]
card_heights = [0.145, 0.145, 0.145, 0.145]
card_tops    = [0.730, 0.570, 0.410, 0.250]

for (name, benefit, conf, col, cat, tier, stars), top in zip(SCHEMES, card_tops):
    h = 0.148
    card(ax, 0.04, top-h+0.010, 0.92, h, t, fc=WHITE, ec=BORDER, lw=0.7)

    # Scheme title row
    ax.text(0.08, top-0.010, name, transform=t, fontsize=10,
            fontweight="bold", color=DARK, va="top")
    ax.text(0.08, top-0.028, f"{cat}", transform=t, fontsize=8, color=GRAY, va="top")

    # Tier badge
    ax.add_patch(FancyBboxPatch((0.74, top-0.025), 0.17, 0.020,
        boxstyle="round,pad=0.004", fc=f"{col}18", ec=f"{col}40", lw=0.6, transform=t))
    ax.text(0.825, top-0.015, f"{stars} {tier}", transform=t, fontsize=7,
            fontweight="bold", color=col, ha="center", va="center")
    ax.text(0.895, top-0.042, f"{int(conf*100)}%", transform=t, fontsize=13,
            fontweight="bold", color=col, ha="center", va="center")

    # Progress bar
    progress_bar(ax, 0.05, top-0.052, 0.89, 0.006, conf, col, t)

    # 3 info boxes
    bx_data = [
        ("BENEFIT",          f"{benefit}",                                 "#f5f5f7"),
        ("ELIGIBILITY",      "As per scheme criteria",                     "#f5f5f7"),
        ("DOCUMENTS",        "Aadhaar  •  Bank passbook  •  Land records", "#f5f5f7"),
    ]
    for bi, (blabel, bval, bfc) in enumerate(bx_data):
        bx = 0.05 + bi*0.307
        bw = 0.29
        by = top - 0.135
        bh = 0.075
        card(ax, bx, by, bw, bh, t, fc=bfc, ec="none", lw=0, radius=0.008)
        ax.text(bx+0.015, by+bh-0.010, blabel, transform=t, fontsize=6.5,
                fontweight="bold", color=GRAY)
        ax.text(bx+0.015, by+bh-0.030, bval, transform=t, fontsize=8,
                fontweight="bold", color=DARK)

    # Apply button
    ax.add_patch(FancyBboxPatch((0.05, top-0.148), 0.22, 0.022,
        boxstyle="round,pad=0.005", fc=BLUE, ec="none", transform=t))
    ax.text(0.16, top-0.137, "Apply on official portal  →", transform=t,
            fontsize=7.5, fontweight="bold", color=WHITE, ha="center", va="center")

# Footer
ax.plot([0,1], [0.015, 0.015], color=BORDER, lw=0.8, transform=t)
ax.text(0.50, 0.007, "Built by VeereshMath  ·  AICTE  ·  IBM SkillsBuild  ·  BharatCares  ·  2026",
        transform=t, fontsize=7, color=GRAY, ha="center", va="center")

plt.tight_layout(rect=[0,0,1,1])
fig.savefig(os.path.join(FIGDIR, "12_ui_page2_schemes.png"), dpi=DPI,
            bbox_inches="tight", facecolor=BG)
plt.close()

# ═══════════════════════════════════════════════════════════════════
# PAGE 3 — Ask JanMitra
# ═══════════════════════════════════════════════════════════════════
print("Generating 13_ui_page3_ask.png ...")
fig, ax = plt.subplots(figsize=(10, 11))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.axis("off")
t = ax.transAxes

nav_bar(ax, active=2)

# Hero
ax.text(0.05, 0.895, "JANMITRA", transform=t, fontsize=8, fontweight="bold", color=BLUE)
ax.text(0.05, 0.860, "Ask in your language.", transform=t,
        fontsize=16, fontweight="bold", color=DARK)
ax.text(0.05, 0.832, "Type any question about government schemes in Hindi, English, or 6 supported languages.",
        transform=t, fontsize=9, color=GRAY)

# Language tab bar
card(ax, 0.04, 0.790, 0.92, 0.038, t, fc="#e5e5ea", ec="none", lw=0, radius=0.01)
langs = ["English", "हिन्दी", "తెలుగు", "தமிழ்", "ಕನ್ನಡ", "বাংলা"]
tab_w = 0.92/6
for i, lang in enumerate(langs):
    tx = 0.04 + i * tab_w + tab_w/2
    if i == 0:
        ax.add_patch(FancyBboxPatch((0.04 + i*tab_w + 0.003, 0.793),
            tab_w - 0.006, 0.031, boxstyle="round,pad=0.005",
            fc=WHITE, ec=BORDER, lw=0.5, transform=t))
        ax.text(tx, 0.808, lang, transform=t, fontsize=9,
                fontweight="bold", color=BLUE, ha="center", va="center")
    else:
        ax.text(tx, 0.808, lang, transform=t, fontsize=8.5,
                color=GRAY, ha="center", va="center")

# Query input card
card(ax, 0.04, 0.730, 0.92, 0.052, t, fc=WHITE, ec=BORDER, lw=0.7)
ax.text(0.07, 0.770, "Ask about eligibility, documents, benefits — in English", transform=t,
        fontsize=8, color=GRAY)
card(ax, 0.06, 0.736, 0.68, 0.032, t, fc=WHITE, ec="#d2d2d7", lw=0.8, radius=0.005)
ax.text(0.09, 0.752, "Am I eligible for Ayushman Bharat?", transform=t,
        fontsize=9, color=DARK, va="center")
ax.add_patch(FancyBboxPatch((0.76, 0.736), 0.17, 0.032,
    boxstyle="round,pad=0.005", fc=BLUE, ec="none", transform=t))
ax.text(0.845, 0.752, "Ask JanMitra", transform=t,
        fontsize=9, fontweight="bold", color=WHITE, ha="center", va="center")

# Intent badge row
ax.add_patch(FancyBboxPatch((0.04, 0.694), 0.22, 0.026,
    boxstyle="round,pad=0.006", fc=f"{GREEN}18", ec=f"{GREEN}40", lw=0.6, transform=t))
ax.text(0.15, 0.707, "Eligibility Check", transform=t,
        fontsize=9, fontweight="bold", color=GREEN, ha="center", va="center")
ax.text(0.29, 0.707, "Confidence:", transform=t, fontsize=9, color=GRAY, va="center")
ax.text(0.39, 0.707, "88%", transform=t, fontsize=9, fontweight="bold", color=DARK, va="center")
ax.text(0.80, 0.707, "Model: keyword heuristic", transform=t,
        fontsize=8, color=GRAY, va="center")

progress_bar(ax, 0.04, 0.685, 0.92, 0.007, 0.88, GREEN, t)

# Response card
card(ax, 0.04, 0.580, 0.92, 0.098, t, fc=WHITE, ec=BORDER, lw=0.7)
ax.text(0.07, 0.668, "JANMITRA SAYS", transform=t,
        fontsize=7.5, fontweight="bold", color=GRAY)
ax.text(0.07, 0.650, "JanMitra checks your age, income, social category, and state against",
        transform=t, fontsize=9, color=DARK)
ax.text(0.07, 0.634, "scheme eligibility rules. Based on your profile, go to the",
        transform=t, fontsize=9, color=DARK)
ax.text(0.07, 0.618, "Eligible Schemes", transform=t,
        fontsize=9, fontweight="bold", color=BLUE)
ax.text(0.26, 0.618, "tab for a personalised list with confidence scores.",
        transform=t, fontsize=9, color=DARK)
ax.text(0.07, 0.598, "Intent detected in < 1ms  ·  TF-IDF character n-gram model  ·  random_state=42",
        transform=t, fontsize=8, color=GRAY)

# Follow-up chips
ax.text(0.04, 0.558, "You might also want to know:", transform=t,
        fontsize=9, color=GRAY)
chips = ["What documents do I need?", "How do I apply?", "What is the benefit amount?"]
chip_colors = [AMBER, BLUE, "#8b5cf6"]
cx_start = 0.04
for chip, cc in zip(chips, chip_colors):
    chip_w = len(chip)*0.008 + 0.04
    ax.add_patch(FancyBboxPatch((cx_start, 0.520), chip_w, 0.028,
        boxstyle="round,pad=0.006", fc=WHITE, ec="#d2d2d7", lw=0.7, transform=t))
    ax.text(cx_start + chip_w/2, 0.534, chip, transform=t,
            fontsize=8.5, color=DARK, ha="center", va="center")
    cx_start += chip_w + 0.018

# Active chip response card (documents chip clicked)
card(ax, 0.04, 0.370, 0.92, 0.140, t, fc=WHITE, ec=BORDER, lw=0.7)
ax.add_patch(mpatches.FancyBboxPatch((0.04, 0.370), 0.004, 0.140,
    boxstyle="square,pad=0", fc=AMBER, ec="none", transform=t))
ax.text(0.07, 0.498, "Documents Needed", transform=t,
        fontsize=10, fontweight="bold", color=AMBER)
docs = [
    "Aadhaar card (mandatory for all)",
    "Bank passbook (linked to Aadhaar for DBT)",
    "Income certificate (from tehsildar / BDO)",
    "Caste certificate (if SC/ST/OBC)",
    "Residence proof (ration card / voter ID / utility bill)",
    "Passport-size photos (2–4 copies)",
]
for i, doc in enumerate(docs):
    ax.text(0.07, 0.480 - i*0.018, f"  {doc}", transform=t,
            fontsize=8.5, color=DARK, va="center")

# Footer
ax.plot([0,1], [0.020, 0.020], color=BORDER, lw=0.8, transform=t)
ax.text(0.50, 0.010, "Built by VeereshMath  ·  AICTE  ·  IBM SkillsBuild  ·  BharatCares  ·  2026",
        transform=t, fontsize=7, color=GRAY, ha="center", va="center")

plt.tight_layout(rect=[0,0,1,1])
fig.savefig(os.path.join(FIGDIR, "13_ui_page3_ask.png"), dpi=DPI,
            bbox_inches="tight", facecolor=BG)
plt.close()

print("All UI screenshots saved.")
for f in ["11_ui_page1_profile.png","12_ui_page2_schemes.png","13_ui_page3_ask.png"]:
    path = os.path.join(FIGDIR, f)
    size = os.path.getsize(path)
    sys.stdout.write(f"  {f}  ({size//1024} KB)\n")
