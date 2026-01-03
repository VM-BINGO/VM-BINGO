from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import json

# ======================
# CONFIG
# ======================
INPUT_FILE = "vm_plader_200_15felter.json"

OUTPUT_A4 = "World_Cup_2026_Bingo_A4.pdf"
OUTPUT_LETTER = "World_Cup_2026_Bingo_LETTER.pdf"

TITLE_TEXT = "WORLD CUP 2026"
ROWS = 3
COLS = 5
CARDS_PER_PAGE = 3

# ======================
# COLOR THEME
# ======================
ACCENT_GREEN = colors.HexColor("#E6F2E6")        # lys grøn (print-venlig)
ACCENT_GREEN_DARK = colors.HexColor("#6FAE6F")

# ======================
# LOAD DATA
# ======================
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    cards = json.load(f)

card_numbers = sorted(cards.keys(), key=lambda x: int(x))
TOTAL_CARDS = len(card_numbers)

# ======================
# DRAW ONE BINGO CARD
# ======================
def draw_card(c, x, y, width, height, card_no, results):
    outer = 6 * mm
    padding = 8 * mm

    # --- Outer black border ---
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.2)
    c.rect(x + outer, y + outer, width - 2 * outer, height - 2 * outer)

    # --- Inner background ---
    c.setFillColor(colors.whitesmoke)
    c.rect(x + outer, y + outer, width - 2 * outer, height - 2 * outer, stroke=0, fill=1)

    # --- Header (green, NOT rounded) ---
    header_h = 16 * mm
    header_y = y + height - header_h - outer

    c.setFillColor(ACCENT_GREEN)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.rect(x + outer, header_y, width - 2 * outer, header_h, stroke=1, fill=1)

    # Header text
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(x + width / 2, header_y + header_h - 6 * mm, TITLE_TEXT)

    c.setFont("Helvetica", 9)
    c.drawCentredString(
        x + width / 2,
        header_y + 4,
        f"Card {int(card_no):03d}/{TOTAL_CARDS}",
    )

    # --- Grid ---
    grid_top = header_y - 6
    grid_bottom = y + outer + padding
    grid_height = grid_top - grid_bottom
    grid_width = width - 2 * outer - 2 * padding

    cell_w = grid_width / COLS
    cell_h = grid_height / ROWS

    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(0.6)

    idx = 0
    for r in range(ROWS):
        for col in range(COLS):
            cx = x + outer + padding + col * cell_w
            cy = grid_top - (r + 1) * cell_h

            c.roundRect(cx, cy, cell_w, cell_h, 4, stroke=1, fill=0)

            result = results[idx].replace("-", " – ")
            idx += 1

            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.black)
            c.drawCentredString(cx + cell_w / 2, cy + cell_h / 2 - 5, result)

# ======================
# CALLER CARD (SIDE 2)
# ======================
def draw_caller_card(c, page_w, page_h, results):
    margin = 20 * mm
    top_y = page_h - margin

    # Header
    header_h = 18 * mm
    c.setFillColor(ACCENT_GREEN)
    c.rect(margin, top_y - header_h + 4, page_w - 2 * margin, header_h, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.black)
    c.drawCentredString(page_w / 2, top_y, "CALLER CARD")

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.darkgrey)
    c.drawCentredString(
        page_w / 2,
        top_y - 18,
        "Mark each result as it occurs (up to three times)",
    )

    cols = 2
    col_gap = 14 * mm
    usable_w = page_w - 2 * margin - col_gap
    col_w = usable_w / cols

    start_y = top_y - 60
    line_h = 14 * mm
    group_gap = 6 * mm

    box_size = 5 * mm
    box_gap = 6
    box_radius = 2

    # Group results by home goals
    grouped = {}
    for r in results:
        home = int(r.split("-")[0])
        grouped.setdefault(home, []).append(r)

    col = 0
    y = start_y

    for home in sorted(grouped.keys()):
        for r in grouped[home]:
            if y < 30 * mm:
                col += 1
                y = start_y
                if col >= cols:
                    return

            x = margin + col * (col_w + col_gap)

            # Result label
            c.setFont("Helvetica", 11)
            label = r.replace("-", " – ")
            c.drawRightString(x + 24 * mm, y, label)

            box_start_x = x + 36 * mm

            # 1 2 3 labels
            c.setFont("Helvetica", 9)
            for j in range(3):
                c.drawCentredString(
                    box_start_x + j * (box_size + box_gap) + box_size / 2,
                    y + box_size + 2,
                    str(j + 1),
                )

            # Green check boxes
            c.setStrokeColor(ACCENT_GREEN_DARK)
            c.setLineWidth(1)
            for j in range(3):
                c.roundRect(
                    box_start_x + j * (box_size + box_gap),
                    y - 2,
                    box_size,
                    box_size,
                    box_radius,
                    stroke=1,
                    fill=0,
                )

            c.setStrokeColor(colors.black)
            c.setLineWidth(0.7)

            y -= line_h
        y -= group_gap

# ======================
# OWNERSHIP PAGE (SIDE 3)
# ======================
def draw_ownership_page(c, page_w, page_h):
    margin = 20 * mm
    top_y = page_h - margin

    header_h = 16 * mm
    c.setFillColor(ACCENT_GREEN)
    c.rect(margin, top_y - header_h + 4, page_w - 2 * margin, header_h, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.black)
    c.drawCentredString(page_w / 2, top_y, "CARD OWNERSHIP REGISTER")

    c.setFont("Helvetica", 11)
    c.setFillColor(colors.darkgrey)
    c.drawCentredString(
        page_w / 2,
        top_y - 18,
        "Use this page to record who each card has been sold to",
    )

    cols = 4
    col_gap = 8 * mm
    usable_w = page_w - 2 * margin - (cols - 1) * col_gap
    col_w = usable_w / cols

    start_y = top_y - 34
    line_h = 4.5 * mm

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)

    for i in range(TOTAL_CARDS):
        col = i // 50
        row = i % 50

        x = margin + col * (col_w + col_gap)
        y = start_y - row * line_h

        c.drawRightString(x + 8 * mm, y, f"{i + 1}:")
        c.setLineWidth(0.6)
        c.line(x + 10 * mm, y - 1, x + col_w, y - 1)

# ======================
# BUILD PDF
# ======================
def build_pdf(output_file, page_size):
    c = canvas.Canvas(output_file, pagesize=page_size)
    page_w, page_h = page_size

    # --- Caller Card ---
    sorted_results = sorted(set(sum(cards.values(), [])))
    draw_caller_card(c, page_w, page_h, sorted_results)
    c.showPage()

    # --- Ownership Page ---
    draw_ownership_page(c, page_w, page_h)
    c.showPage()

    # --- Bingo cards ---
    card_h = page_h / CARDS_PER_PAGE
    for i, card_no in enumerate(card_numbers):
        if i % CARDS_PER_PAGE == 0:
            c.showPage()
        y = page_h - ((i % CARDS_PER_PAGE) + 1) * card_h

        draw_card(
            c,
            x=0,
            y=y,
            width=page_w,
            height=card_h,
            card_no=card_no,
            results=cards[card_no],
        )

    c.save()

# ======================
# RUN
# ======================
build_pdf(OUTPUT_A4, A4)
build_pdf(OUTPUT_LETTER, LETTER)

print("PDF generated:")
print("-", OUTPUT_A4)
print("-", OUTPUT_LETTER)
