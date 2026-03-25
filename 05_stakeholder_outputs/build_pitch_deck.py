"""
Build pitch_deck.pdf from scratch using reportlab + new business-palette charts.
8-slide executive presentation for CEO/COO audience.
"""
import os
import pandas as pd
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', '01_data', 'processed', 'eif_fund_managers_clean.csv')
CHARTS = os.path.join(BASE, '..', '03_powerbi', 'screenshots')
OUT = os.path.join(BASE, 'pitch_deck.pdf')

# ── Brand palette ──
NAVY     = (35/255, 60/255, 100/255)
STEEL    = (75/255, 100/255, 140/255)
COPPER   = (170/255, 125/255, 60/255)
COPPER_LT = (220/255, 195/255, 140/255)
SAGE     = (55/255, 125/255, 85/255)
ROSE     = (155/255, 80/255, 80/255)
TEAL     = (55/255, 120/255, 130/255)
TXT      = (30/255, 35/255, 50/255)
TXT_MED  = (90/255, 100/255, 120/255)
TXT_LT   = (140/255, 150/255, 170/255)
WHITE    = (1, 1, 1)
SURFACE  = (247/255, 248/255, 252/255)
SURF2    = (237/255, 240/255, 247/255)

# Page size: widescreen 16:9
PW = 13.33 * inch
PH = 7.5 * inch

# Load data
df = pd.read_csv(DATA, encoding='utf-8-sig')
df['eif_commitment_eur'] = pd.to_numeric(df['eif_commitment_eur'], errors='coerce')
df['fit_score_10'] = pd.to_numeric(df['fit_score_10'], errors='coerce')
df['solar_fit'] = pd.to_numeric(df['solar_fit'], errors='coerce').fillna(0).astype(int)
df['hydrogen_fit'] = pd.to_numeric(df['hydrogen_fit'], errors='coerce').fillna(0).astype(int)
df['desalination_fit'] = pd.to_numeric(df['desalination_fit'], errors='coerce').fillna(0).astype(int)
df['short_name'] = df['manager_name'].apply(lambda x: x[:38] + '...' if len(str(x)) > 38 else x)
df_sorted = df.sort_values('fit_score_10', ascending=False).reset_index(drop=True)


def draw_header(c, title, subtitle=None, full_height=False):
    """Navy header bar + copper accent line on each slide."""
    h = PH * 0.48 if full_height else 90
    c.setFillColorRGB(*NAVY)
    c.rect(0, PH - h, PW, h, fill=1, stroke=0)
    # Copper accent
    c.setFillColorRGB(*COPPER)
    c.rect(0, PH - h - 3, PW, 3, fill=1, stroke=0)
    # Title
    if full_height:
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 48)
        c.drawCentredString(PW/2, PH - 130, 'EU FUNDING')
        c.setFillColorRGB(*COPPER_LT)
        c.setFont('Helvetica-Bold', 48)
        c.drawCentredString(PW/2, PH - 190, 'INTELLIGENCE')
        if subtitle:
            c.setFillColorRGB(*TXT_LT)
            c.setFont('Helvetica', 14)
            c.drawCentredString(PW/2, PH - 230, subtitle)
    else:
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 28)
        c.drawString(55, PH - 55, title)
        if subtitle:
            c.setFillColorRGB(*TXT_LT)
            c.setFont('Helvetica', 11)
            c.drawString(55, PH - 75, subtitle)


def draw_footer(c, page_num):
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 7)
    c.drawRightString(PW - 40, 18, f'Page {page_num}')


def draw_kpi_card(c, x, y, w, h, value, label, accent):
    """KPI card with colored top accent bar."""
    # Card background
    c.setFillColorRGB(*SURFACE)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    # Top accent bar
    c.setFillColorRGB(*accent)
    c.rect(x, y + h - 5, w, 5, fill=1, stroke=0)
    # Value
    c.setFillColorRGB(*NAVY)
    c.setFont('Helvetica-Bold', 28)
    c.drawCentredString(x + w/2, y + h/2 - 5, value)
    # Label
    c.setFillColorRGB(*TXT_MED)
    c.setFont('Helvetica', 9)
    c.drawCentredString(x + w/2, y + 12, label)


# ================================================================
#  SLIDE 1 — Title
# ================================================================
def slide_title(c):
    draw_header(c, '', full_height=True)
    # Subtitle area (white)
    c.setFillColorRGB(*TXT)
    c.setFont('Helvetica-Bold', 15)
    c.drawCentredString(PW/2, PH * 0.35, 'Prepared for CEO, COO & Management Team')
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 11)
    c.drawCentredString(PW/2, PH * 0.26, 'European Commission  //  Your Europe Portal  //  Q1 2025')
    # Subtitle under title
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 14)
    y_sub = PH * 0.48 + 22
    c.drawCentredString(PW/2, y_sub, 'EIF Financial Intermediaries Research & Analysis')
    draw_footer(c, 1)


# ================================================================
#  SLIDE 2 — Key Metrics + Chart
# ================================================================
def slide_metrics(c):
    draw_header(c, 'Key Metrics', 'Portfolio overview')
    draw_footer(c, 2)

    total = len(df)
    countries = df['country_primary'].nunique()
    capital = f"EUR {df['eif_commitment_eur'].sum()/1e6:.0f}M"
    solar = str(int(df['solar_fit'].sum()))
    hydrogen = str(int(df['hydrogen_fit'].sum()))
    desal = str(int(df['desalination_fit'].sum()))

    kpis = [
        (str(total), 'Fund Managers', NAVY),
        (str(countries), 'Countries', STEEL),
        (capital, 'Total EIF Capital', COPPER),
        (solar, 'Solar Fit', SAGE),
        (hydrogen, 'Hydrogen Fit', TEAL),
        (desal, 'Desalination', ROSE),
    ]

    card_w = 135
    gap = 18
    total_w = 6 * card_w + 5 * gap
    start_x = (PW - total_w) / 2
    card_y = PH - 190

    for i, (val, lab, accent) in enumerate(kpis):
        x = start_x + i * (card_w + gap)
        draw_kpi_card(c, x, card_y, card_w, 75, val, lab, accent)

    # Embed project fit chart
    chart_path = os.path.join(CHARTS, 'project_fit_coverage.png')
    if os.path.exists(chart_path):
        cw = PW - 120
        ch = PH - 310
        c.drawImage(chart_path, 60, 30, cw, ch, preserveAspectRatio=True, mask='auto')


# ================================================================
#  SLIDE 3 — Fund Manager Rankings Table
# ================================================================
def slide_rankings(c):
    draw_header(c, 'Fund Manager Rankings', 'Sorted by strategic fit score')
    draw_footer(c, 3)

    # Table layout
    cols = ['FUND MANAGER', 'COUNTRY', 'TYPE', 'EIF COMMITMENT', 'SCORE', 'TIER']
    col_x = [55, 340, 510, 590, 730, 800]
    col_w = [285, 170, 80, 140, 70, 120]

    header_y = PH - 125
    row_h = 32

    # Header row
    c.setFillColorRGB(*NAVY)
    c.rect(50, header_y - 5, PW - 100, row_h, fill=1, stroke=0)
    c.setFillColorRGB(*WHITE)
    c.setFont('Helvetica-Bold', 8)
    for col_name, x in zip(cols, col_x):
        c.drawString(x, header_y + 7, col_name)

    # Data rows
    tier_colors = {'Tier 1 - Priority': SAGE, 'Tier 2 - Secondary': COPPER, 'Tier 3 - Monitor': ROSE}
    tier_labels = {'Tier 1 - Priority': 'PRIORITY', 'Tier 2 - Secondary': 'SECONDARY', 'Tier 3 - Monitor': 'MONITOR'}
    tier_bg = {
        'Tier 1 - Priority': (237/255, 245/255, 240/255),
        'Tier 2 - Secondary': (245/255, 240/255, 230/255),
        'Tier 3 - Monitor': (245/255, 237/255, 237/255),
    }

    for i, (_, row) in enumerate(df_sorted.iterrows()):
        y = header_y - (i + 1) * row_h - 5
        tier = row.get('priority_tier', '')

        # Row background
        bg = tier_bg.get(tier, SURFACE if i % 2 == 0 else WHITE)
        c.setFillColorRGB(*bg)
        c.rect(50, y, PW - 100, row_h, fill=1, stroke=0)

        # Grid line
        c.setStrokeColorRGB(*SURF2)
        c.setLineWidth(0.3)
        c.line(50, y, PW - 50, y)

        # Fund Manager
        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica', 8)
        name = row['short_name'] if len(str(row['short_name'])) <= 40 else str(row['short_name'])[:40] + '...'
        c.drawString(col_x[0], y + 10, name)

        # Country
        c.setFillColorRGB(*STEEL)
        c.drawString(col_x[1], y + 10, str(row['country_primary']))

        # Type
        c.setFillColorRGB(*TXT_MED)
        c.drawString(col_x[2], y + 10, str(row.get('fund_type', '')))

        # EIF Commitment
        eif = row['eif_commitment_eur']
        c.setFillColorRGB(*COPPER)
        c.setFont('Helvetica-Bold', 8)
        if pd.notna(eif) and eif > 0:
            c.drawString(col_x[3], y + 10, f"EUR {eif/1e6:.1f}M")
        else:
            c.setFillColorRGB(*TXT_LT)
            c.drawString(col_x[3], y + 10, '--')

        # Score
        score = row['fit_score_10']
        c.setFillColorRGB(*NAVY)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(col_x[4], y + 10, f"{score:.1f}")

        # Tier badge
        tc = tier_colors.get(tier, TXT_MED)
        tl = tier_labels.get(tier, '')
        c.setFillColorRGB(*tc)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(col_x[5], y + 10, tl)


# ================================================================
#  SLIDE 4 — EIF Commitment Chart
# ================================================================
def slide_eif(c):
    draw_header(c, 'EIF Commitment', 'Capital allocated per intermediary')
    draw_footer(c, 4)

    chart_path = os.path.join(CHARTS, 'eif_commitments.png')
    if os.path.exists(chart_path):
        margin = 55
        cw = PW - 2 * margin
        ch = PH - 160
        c.drawImage(chart_path, margin, 30, cw, ch, preserveAspectRatio=True, mask='auto')


# ================================================================
#  SLIDE 5 — Strategic Fit Scoring
# ================================================================
def slide_strategic(c):
    draw_header(c, 'Strategic Fit Scoring', 'Project Fit  //  EIF Commitment  //  SDG  //  Contact  //  Geography')
    draw_footer(c, 5)

    chart_path = os.path.join(CHARTS, 'strategic_scores.png')
    if os.path.exists(chart_path):
        margin = 55
        cw = PW - 2 * margin
        ch = PH - 160
        c.drawImage(chart_path, margin, 30, cw, ch, preserveAspectRatio=True, mask='auto')


# ================================================================
#  SLIDE 6 — Key Findings
# ================================================================
def slide_findings(c):
    draw_header(c, 'Key Findings')
    draw_footer(c, 6)

    findings = [
        ('SPAIN HUB', 'Spain dominates with 7 of 12 fund managers — strongest entry point.', NAVY),
        ('SOLAR COVERAGE', 'Broadest coverage of any project type, multiple funding options.', COPPER),
        ('DESALINATION GAP', 'No fund targets it directly. Best route: SDG 6/14 via Impact Bridge.', ROSE),
        ('HYDROGEN STRATEGY', 'Multi-fund: Suma Capital + Impact Bridge + Axon Partners.', TEAL),
        ('NORDIC SCALE', 'NIAM at EUR 51.8M — largest commitment, infrastructure scale.', SAGE),
        ('SDG READINESS', 'Impact funds require measurable metrics. Prepare data first.', STEEL),
    ]

    card_h = 68
    gap = 12
    start_y = PH - 140
    card_margin = 80

    for i, (title, desc, accent) in enumerate(findings):
        y = start_y - i * (card_h + gap)

        # Card background
        c.setFillColorRGB(*SURFACE)
        c.roundRect(card_margin, y, PW - 2 * card_margin, card_h, 4, fill=1, stroke=0)

        # Left accent bar
        c.setFillColorRGB(*accent)
        c.rect(card_margin, y, 4, card_h, fill=1, stroke=0)

        # Number circle
        c.setFillColorRGB(*SURF2)
        cx = card_margin + 35
        cy = y + card_h / 2
        c.circle(cx, cy, 18, fill=1, stroke=0)
        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica-Bold', 14)
        c.drawCentredString(cx, cy - 5, str(i + 1))

        # Title
        c.setFillColorRGB(*accent)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(card_margin + 65, y + card_h - 22, title)

        # Description
        c.setFillColorRGB(*TXT_MED)
        c.setFont('Helvetica', 10)
        c.drawString(card_margin + 65, y + 15, desc)


# ================================================================
#  SLIDE 7 — Decision Framework
# ================================================================
def slide_framework(c):
    draw_header(c, 'Decision Framework', 'Does EU funding apply to your company?')
    draw_footer(c, 7)

    steps = [
        ('01', 'LOCATION', 'EU27, EEA, outermost regions, associated countries?', NAVY),
        ('02', 'COMPANY', 'Startup, SME, mid-cap, or infrastructure project?', STEEL),
        ('03', 'FINANCE', 'Loans, venture capital, microfinance, or grants?', COPPER),
        ('04', 'PARTNER', 'EIF, EIB, InvestEU, or national promotional banks?', ROSE),
        ('05', 'AMOUNT', 'From under EUR 500K to EUR 50M+?', TEAL),
        ('06', 'SDG', 'Which sustainable development goals apply?', SAGE),
        ('07', 'OUTPUT', 'Your filtered shortlist with direct portal link.', NAVY),
    ]

    start_y = PH - 140
    row_h = 60
    margin = 80

    for i, (num, label, desc, accent) in enumerate(steps):
        y = start_y - i * (row_h + 8)

        # Number badge
        c.setFillColorRGB(*accent)
        c.roundRect(margin, y, 55, 45, 5, fill=1, stroke=0)
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 16)
        c.drawCentredString(margin + 27.5, y + 15, num)

        # Label badge
        c.setFillColorRGB(*SURF2)
        c.roundRect(margin + 65, y, 140, 45, 5, fill=1, stroke=0)
        c.setFillColorRGB(*accent)
        c.setFont('Helvetica-Bold', 11)
        c.drawCentredString(margin + 135, y + 15, label)

        # Arrow
        c.setFillColorRGB(*TXT_LT)
        c.setFont('Helvetica', 14)
        c.drawString(margin + 215, y + 15, '>>')

        # Description card
        c.setFillColorRGB(*SURFACE)
        c.roundRect(margin + 250, y, PW - 2 * margin - 250, 45, 5, fill=1, stroke=0)
        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica', 10)
        c.drawCentredString(margin + 250 + (PW - 2 * margin - 250) / 2, y + 15, desc)


# ================================================================
#  SLIDE 8 — Recommended Actions
# ================================================================
def slide_actions(c):
    draw_header(c, 'Recommended Actions', 'Prioritized by timeline')
    draw_footer(c, 8)

    actions = [
        ('IMMEDIATE', 'Outreach to Tier 1: Suma Capital (8.0/10) and Impact Bridge Global (7.0/10).', ROSE),
        ('Q2 2025', 'Prepare SDG-aligned pitch deck with measurable impact metrics.', COPPER),
        ('Q2 2025', 'Develop Portugal strategy for OXY Capital: solar + green hydrogen.', COPPER),
        ('Q3 2025', 'Apply to Norrsken Impact Accelerator 2026 cohort.', TEAL),
        ('ONGOING', 'Expand intermediary research across all 27 EU member states.', SAGE),
    ]

    start_y = PH - 155
    row_h = 78
    margin = 80

    for i, (timeline, desc, accent) in enumerate(actions):
        y = start_y - i * (row_h + 10)

        # Timeline badge
        c.setFillColorRGB(*accent)
        c.roundRect(margin, y, 150, 50, 6, fill=1, stroke=0)
        c.setFillColorRGB(*WHITE)
        c.setFont('Helvetica-Bold', 12)
        c.drawCentredString(margin + 75, y + 18, timeline)

        # Description card
        card_x = margin + 170
        card_w = PW - 2 * margin - 170
        c.setFillColorRGB(*SURFACE)
        c.roundRect(card_x, y, card_w, 50, 5, fill=1, stroke=0)

        # Colored left accent
        c.setFillColorRGB(*accent)
        c.rect(card_x, y, 4, 50, fill=1, stroke=0)

        c.setFillColorRGB(*TXT)
        c.setFont('Helvetica', 10.5)
        c.drawCentredString(card_x + card_w / 2, y + 18, desc)

    # Footer text
    c.setFillColorRGB(*TXT_LT)
    c.setFont('Helvetica', 9)
    c.drawCentredString(PW / 2, 35, 'European Commission  //  Your Europe Portal  //  Q1 2025')


# ================================================================
#  BUILD
# ================================================================
def build():
    c_pdf = canvas.Canvas(OUT, pagesize=(PW, PH))

    slides = [
        slide_title,
        slide_metrics,
        slide_rankings,
        slide_eif,
        slide_strategic,
        slide_findings,
        slide_framework,
        slide_actions,
    ]

    for i, slide_fn in enumerate(slides):
        if i > 0:
            c_pdf.showPage()
        # White background
        c_pdf.setFillColorRGB(*WHITE)
        c_pdf.rect(0, 0, PW, PH, fill=1, stroke=0)
        slide_fn(c_pdf)

    c_pdf.save()
    print(f'Saved: {OUT}')


if __name__ == '__main__':
    build()
