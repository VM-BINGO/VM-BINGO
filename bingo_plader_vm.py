import random
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

DATA = [
("1-0", 10.625), ("2-1", 10.625), ("0-1", 10.3125), ("0-0", 9.0625),
("1-1", 8.75), ("2-0", 7.8125), ("1-2", 7.5), ("0-2", 6.25),
("2-2", 3.75), ("3-1", 3.75), ("0-3", 3.4375), ("3-0", 3.125),
("2-3", 1.875), ("4-1", 1.5625), ("1-3", 1.5625), ("3-2", 1.25),
("3-3", 0.9375), ("0-4", 0.9375), ("1-4", 0.9375), ("4-0", 0.9375),
("4-2", 0.625), ("2-4", 0.625), ("6-1", 0.625), ("7-0", 0.625),
("5-0", 0.3125), ("5-2", 0.3125), ("6-0", 0.3125), ("6-2", 0.3125),
("1-5", 0.3125), ("1-7", 0.3125), ("2-5", 0.3125), ("4-3", 0.3125)
]

RESULTS = [r for r, _ in DATA]
WEIGHTS = [p for _, p in DATA]

TOTAL_PLATES = 100
OUTPUT_PDF = "vm_bingo_plader_6_pr_side_pæn.pdf"
OUTPUT_JSON = "vm_bingo_plader_100.json"

plates_data = {}   # 👈 her gemmer vi alle plader


def draw_plate(c, x, y, size, plate_no):
    cell = size / 3
    values = random.choices(RESULTS, weights=WEIGHTS, k=9)
    radius = 10

    # Gem pladens værdier
    plates_data[str(plate_no)] = values

    path = c.beginPath()
    path.roundRect(x, y, size, size, radius)
    c.saveState()
    c.clipPath(path, stroke=0, fill=0)

    c.setLineWidth(0.8)
    c.setFont("Helvetica-Bold", 22)

    i = 0
    for r in range(3):
        for col in range(3):
            cx = x + col * cell
            cy = y + (2 - r) * cell
            c.rect(cx, cy, cell, cell)
            c.drawCentredString(cx + cell / 2, cy + cell / 2 - 8, values[i])
            i += 1

    c.setFont("Helvetica", 9)
    c.drawString(x + 6, y + size - 14, "VM 2026")
    c.drawRightString(x + size - 6, y + size - 14, f"#{plate_no}")

    c.restoreState()

    c.setLineWidth(1.5)
    c.setStrokeColor(black)
    c.roundRect(x, y, size, size, radius, stroke=1, fill=0)


def main():
    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    width, height = A4

    margin = 25
    gap = 15
    cols, rows = 2, 3

    plate_size = min(
        (width - 2 * margin - (cols - 1) * gap) / cols,
        (height - 2 * margin - (rows - 1) * gap) / rows
    )

    plate_no = 1

    while plate_no <= TOTAL_PLATES:
        for r in range(rows):
            for col in range(cols):
                if plate_no > TOTAL_PLATES:
                    break

                x = margin + col * (plate_size + gap)
                y = height - margin - (r + 1) * plate_size - r * gap
                draw_plate(c, x, y, plate_size, plate_no)
                plate_no += 1

        c.showPage()

    c.save()

    # 💾 Gem JSON med plader
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(plates_data, f, ensure_ascii=False, indent=2)

    print("Gemt:", OUTPUT_PDF)
    print("Gemt:", OUTPUT_JSON)


if __name__ == "__main__":
    main()
