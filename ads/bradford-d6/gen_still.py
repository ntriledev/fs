#!/usr/bin/env python3
"""
FlirtSpot — static DOOH poster · 1080x1920 PNG
Screen: JCDecaux Bradford D6 "Broadway IFO 33" (MFRAME 931714-123), via Blindspot
One-frame composition of the 12s spot: logo hero · radar with locked target ·
HERE / NOW (Quicksand brand gradients) · Google Play badge · FREE · 18+
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from gen_12s import (W, H, BG, BG_DEEP, CORAL, GOLD, REDPINK, CYAN, FG, WHITE,
                     glow, vgrad_span, draw_tracked, shear_mask_rows, badge_layer,
                     font, font_reg, font_quick, LOGO_SRC, ICON_SRC,
                     radial_blob, sweep_band_x, ease_out)

OUT_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "flirtspot-bradford-d6-static-1080x1920.png")

CX, CY, R = 540, 880, 270
M2PX = R / 150.0
VGRAD_HERE = vgrad_span(CYAN, (0, 114, 255), 1340, 1480)
VGRAD_NOW  = vgrad_span(CORAL, GOLD, 1340, 1480)
VGRAD_WEB  = vgrad_span(WHITE, (255, 150, 190), 1800, 1875)   # flirt.spot domain line
AMB_CORAL = radial_blob(CORAL, 88, 900)
AMB_CYAN  = radial_blob(CYAN, 72, 800)

BLIPS = [  # (metres, angle_deg, label)
    (120, 150, "120M"),
    ( 63,  35,  "63M"),
    ( 88, -25,  "88M"),   # locked target
    ( 42, 115,  "42M"),
]
def blip_xy(m, adeg):
    r = m * M2PX; a = math.radians(adeg)
    return CX + r * math.cos(a), CY - r * math.sin(a)

img = Image.new("RGB", (W, H), BG).convert("RGBA")
img.paste(vgrad_span(BG, BG_DEEP, 0, H), (0, 0))
img.alpha_composite(AMB_CORAL, (-60, 60))
img.alpha_composite(AMB_CYAN, (360, 1180))

fx = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d  = ImageDraw.Draw(ov)
dfx = ImageDraw.Draw(fx)

# ---- HUD ----
draw_tracked(d, CX, 190, "RADAR // FLIRTSPOT · 150M RADIUS · BRADFORD LIVE",
             font_reg(30), CYAN + (200,), 6)

# ---- logo hero ----
LOGO_W = 920
h = int(LOGO_W / (LOGO_SRC.width / LOGO_SRC.height))
lg = LOGO_SRC.resize((LOGO_W, h), Image.LANCZOS)
x0, y0 = CX - LOGO_W // 2, 350 - h // 2
lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lay.alpha_composite(lg, (x0, y0))
band = sweep_band_x(760, sigma=110)          # light sweep frozen mid-logo
mask = Image.new("L", (W, H), 0)
mask.paste(lg.getchannel("A"), (x0, y0))
lay.paste((225, 245, 255, 255), (0, 0), ImageChops.multiply(band, mask))
fx.alpha_composite(glow(lay, 12))
ov.alpha_composite(lay)

# ---- radar disc ----
for rr, lab, al in ((R, "150M", 44), (int(R*0.74), "100M", 34), (int(R*0.48), "50M", 30)):
    d.ellipse([CX-rr, CY-rr, CX+rr, CY+rr], outline=FG + (al,), width=3)
    lx, ly = CX + rr * 0.707, CY - rr * 0.707
    d.text((lx + 8, ly - 24), lab, font=font_reg(22), fill=FG + (110,))
d.line([CX, CY - R, CX, CY + R], fill=FG + (14,), width=1)
d.line([CX - R, CY, CX + R, CY], fill=FG + (14,), width=1)

S = 2 * R + 8
sl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
sd = ImageDraw.Draw(sl)
sd.pieslice([6, 6, S-6, S-6], -74, -60, fill=CYAN + (14,))
sd.pieslice([6, 6, S-6, S-6], -60, -18, fill=CYAN + (30,))
sl = glow(sl, 6)
ov.alpha_composite(sl, (CX - S // 2, CY - S // 2))

# YOU dot + pings
d.ellipse([CX-11, CY-11, CX+11, CY+11], fill=FG + (255,))
dfx.ellipse([CX-16, CY-16, CX+16, CY+16], fill=FG + (120,))
for pr, pa in ((90, 70), (185, 36)):
    d.ellipse([CX-pr, CY-pr, CX+pr, CY+pr], outline=REDPINK + (pa,), width=3)

# blips + labels + spark to locked target
tx, ty = blip_xy(*BLIPS[2][:2])
for m, a, lab in BLIPS:
    bx, by = blip_xy(m, a)
    s = 11
    d.ellipse([bx-s, by-s, bx+s, by+s], fill=REDPINK + (255,))
    dfx.ellipse([bx-s*2, by-s*2, bx+s*2, by+s*2], fill=REDPINK + (110,))
    d.text((bx + 16, by - 24), lab, font=font_reg(22), fill=FG + (190,))
# spark YOU -> target
d.line([CX, CY, tx, ty], fill=FG + (235,), width=6)
dfx.line([CX, CY, tx, ty], fill=WHITE + (150,), width=15)
d.ellipse([tx-12, ty-12, tx+12, ty+12], fill=WHITE + (255,))
# reticle lock
arm = 36
for sx in (-1, 1):
    for sy in (-1, 1):
        cxp, cyp = tx + sx * arm, ty + sy * arm
        d.line([cxp, cyp, cxp - sx * 17, cyp], fill=CYAN + (230,), width=4)
        d.line([cxp, cyp, cxp, cyp - sy * 17], fill=CYAN + (230,), width=4)
d.ellipse([tx-arm-8, ty-arm-8, tx+arm+8, ty+arm+8], outline=CYAN + (110,), width=2)

# ---- message: MATCH THE VIBE + HERE & NOW ----
draw_tracked(d, CX, 1250, "MATCH THE VIBE", font_quick(58, 600), FG + (235,), 14)

dm = ImageDraw.Draw(Image.new("L", (1, 1)))
size, tr = 150, 16
def wword(wd, sz): return sum(dm.textlength(c, font=font_quick(sz)) for c in wd) + tr * (len(wd) - 1)
amp_sz = int(size * 0.62)
total = wword("HERE", size) + 36 + wword("&", amp_sz) + 36 + wword("NOW", size)
if total > 950:
    size = int(size * 950 / total); amp_sz = int(size * 0.62)
    total = wword("HERE", size) + 36 + wword("&", amp_sz) + 36 + wword("NOW", size)
x = CX - total / 2
for word, sz, grad in (("HERE", size, VGRAD_HERE), ("&", amp_sz, None), ("NOW", size, VGRAD_NOW)):
    m = Image.new("L", (W, H), 0)
    draw_tracked(ImageDraw.Draw(m), x, 1410, word, font_quick(sz), 255, tr, mid=False)
    m = shear_mask_rows(m, cy_ref=1410)
    lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if grad is None:
        lay2.paste(FG + (200,), (0, 0), m)
    else:
        lay2.paste(grad, (0, 0), m)
    fx.alpha_composite(glow(lay2, 10))
    ov.alpha_composite(lay2)
    x += wword(word, sz) + 36

# ---- CTA: Google Play badge + FREE · 18+ ----
pr = 340
d.ellipse([CX-pr, 1620-pr, CX+pr, 1620+pr], outline=REDPINK + (45,), width=3)

bl = badge_layer(255)
bw = 660
bh = int(bl.height * bw / bl.width)
bl = bl.resize((bw, bh), Image.LANCZOS)
lay4 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lay4.alpha_composite(bl, (CX - bw // 2, int(1620 - bh / 2)))
fx.alpha_composite(glow(lay4, 8))
ov.alpha_composite(lay4)

draw_tracked(d, CX, 1755, "FREE · 18+", font(40), FG + (220,), 10)

# ---- web: flirt.spot ----
md = Image.new("L", (W, H), 0)
draw_tracked(ImageDraw.Draw(md), CX, 1840, "flirt.spot", font_quick(58), 255, 12)
md = shear_mask_rows(md, cy_ref=1840)
layw = Image.new("RGBA", (W, H), (0, 0, 0, 0))
layw.paste(VGRAD_WEB, (0, 0), md)
fx.alpha_composite(glow(layw, 9))
ov.alpha_composite(layw)

# ---- composite ----
out = Image.alpha_composite(img, glow(fx, 2))
out = Image.alpha_composite(out, ov)
out.convert("RGB").save(OUT_PNG)
print("saved:", OUT_PNG)
