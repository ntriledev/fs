#!/usr/bin/env python3
"""
FlirtSpot — 3s DOOH spot · 1920x1080 · 30fps · 90 frames  (v4)
Screen: JFC Training College, London (MP4 · 1920x1080 · 3s)
Flow: FULLSCREEN flirt.spot logo (light sweep) -> HERE (left, blue) / NOW (right, red) -> Google Play lockup
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H, FPS, DUR = 1920, 1080, 30, 3.0
N = int(FPS * DUR)  # 90
_here = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(_here, "build")
os.makedirs(OUT, exist_ok=True)

BG     = (7, 6, 11)
RED    = (255, 81, 47)     # logo redGrad (#FF512F)
CYAN   = (0, 198, 255)
WHITE  = (255, 255, 255)
OFFW   = (255, 245, 234)
GREYTX = (198, 204, 214)
BADGE_BG = (13, 15, 20)

# Google Play icon colors
GP_BLUE, GP_YELLOW, GP_RED, GP_GREEN = (0, 201, 255), (255, 224, 0), (255, 58, 68), (0, 240, 118)

F = "/usr/share/fonts/truetype/liberation/"
def font(size): return ImageFont.truetype(F + "LiberationSans-Bold.ttf", size)
F_BALOO = os.path.join(_here, "fonts", "Baloo2.ttf")          # curvy rounded display face
def font_curvy(size, wght=800):
    f = ImageFont.truetype(F_BALOO, size)
    f.set_variation_by_axes([wght])
    return f

LOGO_SRC = Image.open(os.path.join(_here, "logo_flirtspot_big.png")).convert("RGBA")
LOGO_SRC = LOGO_SRC.crop(LOGO_SRC.getbbox())        # trim transparent padding -> full bleed
ICON_SRC = Image.open(os.path.join(_here, "icon_flirtspot_hearts.png")).convert("RGBA")  # intertwined-hearts app icon
LOGO_W_FULL = 1860                                   # near edge-to-edge on 1920
LOGO_H   = int(LOGO_W_FULL / (LOGO_SRC.width / LOGO_SRC.height))
LOGO_CX, LOGO_CY = 960, 380

CX, CY, RX, RY = 960, 640, 520, 275                   # dim radar backdrop

def ease_out(t):  return 1 - (1 - t) ** 3
def ease_back(t): return 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2
def clamp01(t):   return max(0.0, min(1.0, t))
def seg(f, a, b): return clamp01((f - a) / (b - a)) if b > a else (1.0 if f >= b else 0.0)

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
BLUE_GRAD = vgrad((0, 198, 255), (0, 114, 255))       # logo blueGrad — HERE
RED_GRAD  = vgrad((255, 81, 47), (240, 152, 25))      # logo redGrad — NOW

def sweep_band(cx, sigma=110):
    band = Image.new("L", (W, H), 0)
    px = band.load()
    for x in range(W):
        a = int(255 * math.exp(-((x - cx) ** 2) / (2 * sigma ** 2)))
        if a:
            for y in range(0, H, 2):
                px[x, y] = a
                if y + 1 < H: px[x, y + 1] = a
    return band

def draw_tracked(d, x, y, text, fnt, fill, tr=0, mid=True):
    wtot = sum(d.textlength(c, font=fnt) for c in text) + tr * (len(text) - 1)
    if mid: x -= wtot / 2
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill, anchor="lm")
        x += d.textlength(c, font=fnt) + tr

def heart_poly(cx, cy, s, rot=0.0):
    pts = []
    for i in range(64):
        t = 2 * math.pi * i / 64
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        if rot:
            x, y = x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + x * s, cy + y * s))
    return pts

def shear_mask_rows(m, k=-0.16):
    """Italic lean: shear each row horizontally, proportional to distance from centre."""
    bb = m.getbbox()
    if not bb: return m
    y0, y1 = bb[1], bb[3]
    cy = (y0 + y1) / 2
    out = Image.new("L", (W, H), 0)
    for y in range(y0, y1):
        out.paste(m.crop((0, y, W, y + 1)), (int(k * (y - cy)), y))
    return out

def play_icon(d, ix, iy, s, alpha=255):
    """Google Play triangle (approx) — top-left blue, bottom-left red, top-right yellow, bottom-right green."""
    P = lambda u, v: (ix + u * s, iy + v * s)
    L, Lm, Lb = (0.06, 0.02), (0.06, 0.50), (0.06, 0.98)
    Um, Dm, C, R = (0.50, 0.26), (0.50, 0.74), (0.36, 0.50), (0.96, 0.50)
    d.polygon([P(*L), P(*Um), P(*C), P(*Lm)], fill=GP_BLUE + (alpha,))
    d.polygon([P(*Lm), P(*C), P(*Dm), P(*Lb)], fill=GP_RED + (alpha,))
    d.polygon([P(*C), P(*Um), P(*R)], fill=GP_YELLOW + (alpha,))
    d.polygon([P(*C), P(*R), P(*Dm)], fill=GP_GREEN + (alpha,))

BADGE_W, BADGE_H, BADGE_CY = 520, 132, 800
def badge_layer(alpha):
    lay = Image.new("RGBA", (BADGE_W + 40, BADGE_H + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = 20, 20, 20 + BADGE_W, 20 + BADGE_H
    d.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=BADGE_BG + (int(240 * alpha / 255),),
                        outline=WHITE + (int(210 * alpha / 255),), width=3)
    play_icon(d, x0 + 34, y0 + BADGE_H / 2 - 42, 84, int(alpha))
    tx = x0 + 34 + 84 + 28
    d.text((tx, y0 + 38), "GET IT ON", font=font(26), fill=GREYTX + (alpha,), anchor="lm")
    d.text((tx, y0 + 90), "Google Play", font=font(58), fill=WHITE + (alpha,), anchor="lm")
    return lay

def render_frame(f):
    img = Image.new("RGB", (W, H), BG).convert("RGBA")
    fx  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d   = ImageDraw.Draw(ov)

    # ---------- dim radar backdrop ----------
    amb = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(amb).ellipse([CX-640, CY-370, CX+640, CY+370], fill=(16, 32, 66, 20))
    img.alpha_composite(glow(amb, 90))
    r_in = seg(f, 2, 12)
    if r_in > 0:
        d.ellipse([CX-RX, CY-RY, CX+RX, CY+RY], outline=CYAN + (int(40 * r_in),), width=3)
        rx, ry = RX * 100 / 150, RY * 100 / 150
        d.ellipse([CX-rx, CY-ry, CX+rx, CY+ry], outline=CYAN + (int(30 * r_in),), width=2)
    if f >= 4:
        theta = -70 + (f - 4) * 6.0
        S = 2 * RX
        lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(lay).pieslice([8, 8, S-8, S-8], theta, theta + 46, fill=CYAN + (26,))
        lay = glow(lay, 7).resize((2 * RX, 2 * RY), Image.LANCZOS)
        ov.alpha_composite(lay, (CX - RX, CY - RY))

    # ---------- FULLSCREEN logo (entire spot) ----------
    p_in = seg(f, 4, 14)
    k = 0.92 + 0.08 * ease_out(p_in)
    alpha = int(255 * p_in)
    h = int(LOGO_H * k); w = int(h * (LOGO_SRC.width / LOGO_SRC.height))
    lg = LOGO_SRC.resize((w, h), Image.LANCZOS)
    x0, y0 = int(LOGO_CX - w / 2), int(LOGO_CY - h / 2)
    lg.putalpha(lg.getchannel("A").point(lambda v: v * alpha // 255))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay.alpha_composite(lg, (x0, y0))
    if 8 <= f <= 28:                                  # light sweep across logo
        band = sweep_band(380 + 1180 * seg(f, 8, 26))
        mask = Image.new("L", (W, H), 0)
        mask.paste(lg.getchannel("A"), (x0, y0))
        hi = ImageChops.multiply(band, mask)
        lay.paste((220, 245, 255, alpha), (0, 0), hi)
    fx.alpha_composite(glow(lay, 10 + 2 * math.sin(f * 0.3)))
    ov.alpha_composite(lay)

    # ---------- HERE big LEFT / NOW big RIGHT · curvy Baloo, brand gradients, italic lean ----------
    for word, cxw, f0, grad, max_w in (
            ("HERE",  380, 28, BLUE_GRAD, 470),
            ("NOW", 1540, 34, RED_GRAD,  430)):
        p_w = seg(f, f0, f0 + 10)
        if p_w > 0:
            size = int(150 * (0.80 + 0.20 * ease_back(p_w)))
            dm = ImageDraw.Draw(Image.new("L", (1, 1)))
            wpx = sum(dm.textlength(c, font=font_curvy(size)) for c in word) + 12 * (len(word) - 1)
            if wpx > max_w:                                    # fit the empty side zone
                size = int(size * max_w / wpx)
            m = Image.new("L", (W, H), 0)
            draw_tracked(ImageDraw.Draw(m), cxw, 800 + 30 * (1 - ease_out(p_w)),
                         word, font_curvy(size), 255, 12)
            m = shear_mask_rows(m)
            m = m.point(lambda v: int(v * p_w))
            lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay2.paste(grad, (0, 0), m)
            fx.alpha_composite(glow(lay2, 10))
            ov.alpha_composite(lay2)

    # ---------- app icon (intertwined hearts) + Google Play badge ----------
    p_i = seg(f, 43, 55)                               # icon bounces in just after badge
    if p_i > 0:
        if f <= 55: k_i = 0.55 + 0.45 * ease_back(p_i)
        else:       k_i = 1 + 0.015 * math.sin((f - 55) * 0.35)
        s = int(148 * k_i)
        ic = ICON_SRC.resize((s, s), Image.LANCZOS)
        ic.putalpha(ic.getchannel("A").point(lambda v: v * int(p_i * 255) // 255))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(ic, (int(694 - s / 2), int(BADGE_CY - s / 2)))
        fx.alpha_composite(glow(lay, 7 + 2 * math.sin(f * 0.3)))
        ov.alpha_composite(lay)
    p_b = seg(f, 40, 52)
    if p_b > 0:
        if f <= 52:
            k = 0.55 + 0.45 * ease_back(p_b)
        else:
            k = 1 + 0.015 * math.sin((f - 52) * 0.35)
        bl = badge_layer(int(255 * p_b))
        bw, bh = int(bl.width * k), int(bl.height * k)
        bl = bl.resize((bw, bh), Image.LANCZOS)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(bl, (int(788 - 20 + (520 - bw + 40) / 2), int(BADGE_CY - bh / 2)))
        fx.alpha_composite(glow(lay, 8 + 2 * math.sin(f * 0.3)))
        ov.alpha_composite(lay)

    # ---------- FREE · 18+ ----------
    p_f = seg(f, 46, 54)
    if p_f > 0:
        draw_tracked(d, W / 2, 964 + 14 * (1 - ease_out(p_f)), "FREE · 18+",
                     font(30), OFFW + (int(210 * p_f),), 6)

    # ---------- composite + fade ----------
    out = Image.alpha_composite(img, glow(fx, 1))
    out = Image.alpha_composite(out, ov)
    fade = seg(f, N - 6, N - 1)
    if fade > 0:
        out = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), out,
                              Image.new("L", (W, H), int(255 * fade)))
    return out.convert("RGB")

for f in range(N):
    render_frame(f).save(f"{OUT}/frame_{f:03d}.png")
    if f % 30 == 0: print(f"frame {f}/{N}")
print("done:", N, "frames")
