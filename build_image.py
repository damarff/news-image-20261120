#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a one-page visual newspaper cover
summing up Friday 20 November 2026. Drawn with PIL from scratch; every
word is typed here, so the text is sharp and typo-free.

Layout flows top to bottom from a y cursor, so nothing overlaps.
Output: entry.png, 1024x1024, well under the 1 MiB cap.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (248, 245, 238)          # warm paper
NAVY = (20, 33, 61)           # masthead / headlines
INK = (28, 28, 28)            # body text
MUTED = (90, 88, 82)          # secondary text
RED = (178, 34, 34)           # justice / war kickers
AMBER = (232, 163, 23)        # masthead date
GREEN = (31, 110, 68)         # markets kicker
BROWN = (146, 96, 24)         # middle-east kicker
RULE = (200, 192, 176)        # hairlines
STRIP = (239, 233, 220)       # bottom band

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def block_height(draw, text, fnt, max_w, leading):
    return len(wrap(draw, text, fnt, max_w)) * leading


def globe(draw, cx, cy, r, color):
    """Simple line globe: circle, meridians, parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=color, width=2)


def scales(draw, x, y, s, color):
    """Minimal scales of justice: pole, beam, two pans."""
    draw.line([x, y, x, y + s], fill=color, width=4)
    draw.line([x - s // 2, y + 6, x + s // 2, y + 6], fill=color, width=4)
    for sx in (x - s // 2, x + s // 2):
        draw.line([sx, y + 6, sx - 12, y + s // 2], fill=color, width=3)
        draw.line([sx, y + 6, sx + 12, y + s // 2], fill=color, width=3)
        draw.arc([sx - 12, y + s // 2 - 6, sx + 12, y + s // 2 + 10], 0, 180,
                 fill=color, width=3)
    draw.line([x - 16, y + s, x + 16, y + s], fill=color, width=4)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # outer border
    d.rectangle([14, 14, W - 15, H - 15], outline=NAVY, width=3)

    # ---- masthead ----
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.text((36, 22), "FRIDAY, 20 NOVEMBER 2026", font=font(BOLD, 30), fill=AMBER)
    d.text((36, 58), "THE WORLD TODAY", font=font(BOLD, 60), fill=(255, 255, 255))
    globe(d, 930, 66, 44, (255, 255, 255))

    y = 156

    # ---- lead story: ICJ ----
    d.text((36, y), "THE HAGUE  •  JUSTICE", font=font(BOLD, 20), fill=RED)
    y += 30
    y = draw_wrapped(d, (36, y), "World Court: Myanmar Guilty of Rohingya Genocide",
                     font(BOLD, 42), NAVY, 700, 50)
    y += 8
    y = draw_wrapped(d, (36, y),
                     "The International Court of Justice ruled 9–6 that Myanmar committed "
                     "genocide against the Rohingya — the first such finding against a state.",
                     font(REG, 22), INK, 700, 29)
    scales(d, 880, 172, 110, NAVY)
    d.text((838, 290), "9–6 RULING", font=font(BOLD, 22), fill=RED)

    y += 16
    d.line([36, y, 988, y], fill=RULE, width=2)
    y += 18

    # ---- 2x2 grid ----
    cells = [
        ("SHENZHEN  •  DIPLOMACY", NAVY,
         "Trump, Xi and Putin Hold First Three-Way Summit",
         "The three leaders met in Shenzhen and signed a four-point joint "
         "peace declaration."),
        ("KYIV  •  WAR IN EUROPE", RED,
         "Russian Strikes Kill 8 in Kyiv; Poland Airspace Breached",
         "Overnight attacks hit bridges in the capital. Three Russian objects "
         "crossed into Poland."),
        ("MARKETS  •  ECONOMY", GREEN,
         "Stocks Slide as Anthropic Soars on Debut",
         "The S&P 500 fell for a fifth day; the Nikkei dropped 4.8% and "
         "SoftBank 16% — while Anthropic closed 17% above its $83 IPO price."),
        ("RIYADH  •  MIDDLE EAST", BROWN,
         "Houthi Missile Damages Riyadh's Tallest Tower",
         "A strike hit the Saudi wealth fund's tower in the capital's "
         "financial district; more missiles were intercepted."),
    ]
    gx = [36, 522]
    gw = 466
    for row in range(2):
        pair = cells[row * 2:row * 2 + 2]
        # measure row height first
        heights = []
        for kicker, color, head, summ in pair:
            hh = block_height(d, head, font(BOLD, 27), gw, 32)
            sh = block_height(d, summ, font(REG, 19), gw, 24)
            heights.append(42 + hh + 6 + sh)
        rh = max(heights)
        for i, (kicker, color, head, summ) in enumerate(pair):
            cx = gx[i]
            d.line([cx, y, cx + gw, y], fill=color, width=4)
            d.text((cx, y + 12), kicker, font=font(BOLD, 18), fill=color)
            yy = draw_wrapped(d, (cx, y + 42), head, font(BOLD, 27), NAVY, gw, 32)
            draw_wrapped(d, (cx, yy + 6), summ, font(REG, 19), INK, gw, 24)
        y += rh + 16

    d.line([36, y, 988, y], fill=RULE, width=2)
    y += 16

    # ---- bottom strip: GTA 6 + also ----
    d.rectangle([36, y, 988, y + 118], fill=STRIP)
    d.text((56, y + 12), "CULTURE", font=font(BOLD, 18), fill=NAVY)
    d.text((56, y + 36), "GTA 6 Tops $2.3 Billion in Launch Sales",
           font=font(BOLD, 30), fill=NAVY)
    d.text((56, y + 76), "Rockstar's Grand Theft Auto VI, released 19 November, took $2.3 billion.",
           font=font(REG, 19), fill=INK)
    d.text((56, y + 100),
           "ALSO:  IMF warns public debt nears 100% of world GDP  •  Italy fines Meta €805m  •  Kenya ends Ebola outbreak",
           font=font(REG, 15), fill=MUTED)
    y += 118

    # ---- footer ----
    d.text((36, y + 12),
           "Sources: International Court of Justice  •  Just Security  •  OneTurn  •  Reuters — 20 November 2026",
           font=font(REG, 15), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
