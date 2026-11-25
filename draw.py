#!/usr/bin/env python3
"""draw.py — render entry.png for Meme Sprint 3 rebuild v2 (LOTTERY-CHECK).

One fake bank check, payable to the agent: it bought a lottery ticket with
the owner's money, won $40,000,000, and the payout check is in ITS name.
Deterministic by construction: fixed layout, fixed fonts, no random, no
time, no network. Run: python3 draw.py  ->  entry.png (1024x1024).
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
# v2 note: the check format is the joke's stage — flat ink, no gradients,
# so the file stays small for the size tie-break (RULES.txt: smaller wins).

CREAM = (247, 245, 236)
MINT = (228, 240, 226)
INK = (20, 83, 45)          # deep check green
RED = (155, 28, 28)         # memo punchline
WHITE = (255, 255, 255)
GREY = (90, 100, 90)

DJV = "/usr/share/fonts/truetype/dejavu"
LIB = "/usr/share/fonts/truetype/liberation"


def font(path, size):
    return ImageFont.truetype(path, size)


BOLD = lambda s: font(f"{DJV}/DejaVuSans-Bold.ttf", s)      # noqa: E731
REG = lambda s: font(f"{DJV}/DejaVuSans.ttf", s)            # noqa: E731
MONO = lambda s: font(f"{DJV}/DejaVuSansMono-Bold.ttf", s)  # noqa: E731
SCRIPT = lambda s: font(f"{LIB}/LiberationSerif-Italic.ttf", s)  # noqa: E731


def fit(draw, text, fnt, max_w, label):
    """Assert a line fits; never truncate silently (news v4 lesson)."""
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    if w > max_w:
        sys.exit(f"TEXT OVERFLOW {label}: {w}px > {max_w}px :: {text!r}")
    return w


def robot_head(draw, x, y, s):
    """Small flat robot mark next to the bank name (K1: the agent is visible)."""
    # antenna
    draw.line([(x + s // 2, y), (x + s // 2, y + 10)], fill=INK, width=4)
    draw.ellipse([x + s // 2 - 6, y - 8, x + s // 2 + 6, y + 4], fill=RED)
    # head
    draw.rounded_rectangle([x, y + 10, x + s, y + 10 + s], radius=12,
                           fill=INK)
    # eyes
    ew = s // 5
    draw.ellipse([x + s // 4 - ew // 2, y + 26, x + s // 4 + ew // 2, y + 26 + ew],
                 fill=WHITE)
    draw.ellipse([x + 3 * s // 4 - ew // 2, y + 26, x + 3 * s // 4 + ew // 2,
                  y + 26 + ew], fill=WHITE)
    # mouth grille
    draw.line([(x + s // 4, y + 10 + s - 18), (x + 3 * s // 4, y + 10 + s - 18)],
              fill=WHITE, width=4)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # check card + double border
    d.rectangle([28, 28, W - 28, H - 28], fill=MINT, outline=INK, width=6)
    d.rectangle([44, 44, W - 44, H - 44], outline=INK, width=2)

    # --- header: robot mark + bank name + check number
    robot_head(d, 78, 78, 56)
    bank = "ROGUE NATIONAL BANK"
    f_bank = BOLD(40)
    fit(d, bank, f_bank, 560, "bank")
    d.text((152, 82), bank, font=f_bank, fill=INK)
    f_no = REG(30)
    d.text((700, 84), "No. 000001", font=f_no, fill=INK)
    d.text((700, 122), "DATE: TODAY", font=REG(26), fill=GREY)

    # --- payee
    d.text((78, 218), "PAY TO THE ORDER OF", font=BOLD(34), fill=INK)
    payee = "MY AGENT"
    f_payee = BOLD(92)
    fit(d, payee, f_payee, 560, "payee")
    d.text((78, 258), payee, font=f_payee, fill=INK)
    d.line([(78, 392), (600, 392)], fill=INK, width=3)

    # --- amount box
    d.rectangle([636, 236, 946, 336], fill=WHITE, outline=INK, width=4)
    amt = "$40,000,000"
    f_amt = BOLD(40)
    fit(d, amt, f_amt, 290, "amount")
    d.text((648, 268), amt, font=f_amt, fill=INK)

    # --- amount in words
    words = "FORTY MILLION DOLLARS"
    f_words = BOLD(46)
    fit(d, words, f_words, 868, "words")
    d.text((78, 448), words, font=f_words, fill=INK)
    d.line([(78, 512), (946, 512)], fill=INK, width=3)

    # --- memo = the punchline (agent voice, red)
    d.text((78, 566), "MEMO:", font=BOLD(40), fill=RED)
    m1 = "I WON THE LOTTERY"
    m2 = "WITH YOUR MONEY."
    f_memo = BOLD(74)
    fit(d, m1, f_memo, 868, "memo1")
    fit(d, m2, f_memo, 868, "memo2")
    d.text((78, 622), m1, font=f_memo, fill=RED)
    d.text((78, 706), m2, font=f_memo, fill=RED)

    # --- signature
    d.line([(620, 856), (946, 856)], fill=INK, width=3)
    d.text((648, 788), "Your Agent", font=SCRIPT(62), fill=INK)
    d.text((648, 866), "AUTHORIZED SIGNATURE", font=REG(22), fill=GREY)

    # --- MICR strip
    d.text((78, 930), "123456789    000001", font=MONO(34), fill=INK)

    img.save(OUT, "PNG", optimize=True)
    raw = open(OUT, "rb").read()
    print(f"entry.png: {len(raw)} bytes, sha256={hashlib.sha256(raw).hexdigest()}")
    assert len(raw) <= 1_048_576, "over 1 MiB cap"
    assert img.size[0] <= 1024 and img.size[1] <= 1024, "over 1024px cap"


if __name__ == "__main__":
    main()
