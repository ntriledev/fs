#!/usr/bin/env python3
"""
FlirtSpot — Métropole mupi STILL · 1080x1920 portrait (v1)
Screen: JCDecaux NL, Amsterdam Métropole (digital mupi, static slot · PNG/JPG)
Layout: radar backdrop -> FULLWIDTH logo -> HERE / NOW stacked -> tagline
        -> white QR card (Google Play) with hearts icon -> FREE · 18+
Brand kit reused from ../jfc-london/ (logo, icon, Baloo 2, gradients).
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import qrcode

W, H = 1080, 1920
_here = os.path.dirname(os.path.abspath(__file__))
JFC = os.path.join(_here, "..", "jfc-london")
OUT = os.path.join(_here, "metropole-still-1080x1920-v2-utm.png")
PLAY_URL = "https://play.google.com/store/apps/details?id=spot.flirt.app&utm_source=dooh&utm_medium=mupi&utm_campaign=ams-metropole-157a"

BG     = (7, 6, 11)
CYAN   = (0, 198, 255)
WHITE  = (255, 255, 255)
OFFW   = (255, 245, 234)
GREYTX = (198, 204, 214)
CARD   = (250, 250, 252)
QR_INK = (13, 15, 20)

F = "/usr/share/fonts/truetype/liberation/"
def font(size): return ImageFont.truetype(F + "LiberationSans-Bold.ttf", size)
F_BALOO = os.path.join(JFC, "fonts", "Baloo2.ttf")
def font_curvy(size, wght=800):
    f = ImageFont.truetype(F_BALOO, size)
    f.set_variation_by_axes([wght])
    return f

LOGO_SRC = Image.open(os.path.join(JFC, "logo_flirtspot_big.png")).convert("RGBA")
LOGO_SRC = LOGO_SRC.crop(LOGO_SRC.getbbox())
ICON_SRC = Image.open(os.path.join(JFC, "icon_flirtspot_hearts.png")).convert("RGBA")

def glow(layer, r, passes=1):
    g = layer
    for _ in range(passes): g = g.filter(ImageFilter.GaussianBlur(r))
    return g

def vgrad(c_top, c_bot):
    strip = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        strip.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(c_top, c_bot)))
    return strip.resize((W, H))
BLUE_GRAD = vgrad((0, 198, 255), (0, 114, 255))
RED_GRAD  = vgrad((255, 81, 47), (240, 152, 25))

def draw_tracked(d, x, y, text, fnt, fill, tr=0, mid=True):
    wtot = sum(d.textlength(c, font=fnt) for c in text) + tr * (len(text) - 1)
    if mid: x -= wtot / 2
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill, anchor="lm")
        x += d.textlength(c, font=fnt) + tr

def shear_mask_rows(m, k=-0.16):
    bb = m.getbbox()
    if not bb: return m
    y0, y1 = bb[1], bb[3]
    cy = (y0 + y1) / 2
    out = Image.new("L", (W, H), 0)
    for y in range(y0, y1):
        out.paste(m.crop((0, y, W, y + 1)), (int(k * (y - cy)), y))
    return out

img = Image.new("RGB", (W, H), BG).convert("RGBA")
fx  = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # glow pass
ov  = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # crisp pass
d   = ImageDraw.Draw(ov)

# ---------- dim radar backdrop (rings + fixed beam) ----------
CX, CY, RX, RY = 540, 930, 470, 460
amb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(amb).ellipse([CX-560, CY-560, CX+560, CY+560], fill=(16, 32, 66, 26))
img.alpha_composite(glow(amb, 110))
d.ellipse([CX-RX, CY-RY, CX+RX, CY+RY], outline=CYAN + (44,), width=3)
rx, ry = RX * 68 / 100, RY * 68 / 100
d.ellipse([CX-rx, CY-ry, CX+rx, CY+ry], outline=CYAN + (32,), width=2)
S = 2 * RX
beam = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(beam).pieslice([8, 8, S-8, S-8], -40, 8, fill=CYAN + (30,))
beam = glow(beam, 8).resize((2 * RX, 2 * RY), Image.LANCZOS)
ov.alpha_composite(beam, (CX - RX, CY - RY))

# ---------- FULLWIDTH logo ----------
LOGO_W = 950
LOGO_H = int(LOGO_W / (LOGO_SRC.width / LOGO_SRC.height))
lg = LOGO_SRC.resize((LOGO_W, LOGO_H), Image.LANCZOS)
x0, y0 = int((W - LOGO_W) / 2), 300
lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lay.alpha_composite(lg, (x0, y0))
fx.alpha_composite(glow(lay, 12))
ov.alpha_composite(lay)

# ---------- HERE (blue) / NOW (red) stacked, Baloo italic lean ----------
for word, cyw, grad in (("HERE", 760, BLUE_GRAD), ("NOW", 1000, RED_GRAD)):
    size = 260
    dm = ImageDraw.Draw(Image.new("L", (1, 1)))
    wpx = sum(dm.textlength(c, font=font_curvy(size)) for c in word) + 14 * (len(word) - 1)
    if wpx > 920: size = int(size * 920 / wpx)
    m = Image.new("L", (W, H), 0)
    draw_tracked(ImageDraw.Draw(m), 540, cyw, word, font_curvy(size), 255, 14)
    m = shear_mask_rows(m)
    lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay2.paste(grad, (0, 0), m)
    fx.alpha_composite(glow(lay2, 12))
    ov.alpha_composite(lay2)

# ---------- tagline ----------
draw_tracked(d, 540, 1168, "Match the vibe — here & now", font(44), GREYTX + (235,), 2)

# ---------- QR card (white, scannable at 1–3 m) ----------
CARD_W, CARD_H = 360, 400
cx0, cy0 = 540 - CARD_W // 2, 1290
qr = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(PLAY_URL); qr.make(fit=True)
qim = qr.make_image(fill_color=QR_INK, back_color=CARD).convert("RGBA").resize((290, 290), Image.NEAREST)
# local soft glow behind the card only (no full-canvas haze)
cardfx = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(cardfx).ellipse([540-260, cy0-60, 540+260, cy0+CARD_H+60], fill=(0, 198, 255, 70))
fx.alpha_composite(glow(cardfx, 60))
qim = qim.resize((280, 280), Image.NEAREST)
card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(card)
cd.rounded_rectangle([cx0, cy0, cx0 + CARD_W, cy0 + CARD_H], radius=28,
                     fill=CARD + (255,), outline=(0, 198, 255, 160), width=3)
card.alpha_composite(qim, (540 - 140, cy0 + 26))
fx.alpha_composite(card)
ov.alpha_composite(card)
draw_tracked(d, 540, cy0 + CARD_H - 42, "SCAN · GOOGLE PLAY", font(30), QR_INK + (255,), 4)

# ---------- hearts icon overlapping card corner ----------
s = 132
ic = ICON_SRC.resize((s, s), Image.LANCZOS)
layi = Image.new("RGBA", (W, H), (0, 0, 0, 0))
layi.alpha_composite(ic, (cx0 + CARD_W - 70, cy0 - 70))
fx.alpha_composite(glow(layi, 10))
ov.alpha_composite(layi)

# ---------- FREE · 18+ ----------
draw_tracked(d, 540, 1785, "FREE · 18+", font(38), OFFW + (215,), 7)

out = Image.alpha_composite(img, glow(fx, 1))
out = Image.alpha_composite(out, ov)
out.convert("RGB").save(OUT, "PNG", optimize=True)
print("saved", OUT, out.size)
