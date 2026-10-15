#!/usr/bin/env python3
"""
FlirtSpot — 12s DOOH spot · 1080x1920 portrait · 25fps · 300 frames
Screen: JCDecaux Bradford D6 "Broadway IFO 33" (MFRAME 931714-123), via Blindspot
Mall cut, Google Play badge CTA: radar hero -> lock/spark -> LOGO bloom -> Play badge
Flow: LOGO open -> RADAR + blips + MESSAGE -> spark/LOGO -> CTA (icon + Google Play)
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H, FPS, DUR = 1080, 1920, 25, 12.0
N = int(FPS * DUR)  # 300
_here = os.path.dirname(os.path.abspath(__file__))
JFC = os.path.join(os.path.dirname(_here), "jfc-london")
OUT = os.path.join(_here, "build")
os.makedirs(OUT, exist_ok=True)

# ---- palette (v3 warm, matches bgc-3d-led-creative.html) ----
BG      = (10, 6, 16)        # #0a0610
BG_DEEP = (7, 4, 10)
CORAL   = (255, 81, 47)      # --spark
GOLD    = (240, 152, 25)     # --pulse
REDPINK = (255, 45, 85)      # --glow
CYAN    = (0, 198, 255)      # --cyan
SKY     = (79, 172, 254)     # --sky
WHITE   = (255, 255, 255)
FG      = (255, 245, 234)    # --fg

F_LIB = "/usr/share/fonts/truetype/liberation/"
def font(size): return ImageFont.truetype(F_LIB + "LiberationSans-Bold.ttf", size)
def font_reg(size): return ImageFont.truetype(F_LIB + "LiberationSans-Regular.ttf", size)
F_BALOO = os.path.join(JFC, "fonts", "Baloo2.ttf")
F_QUICK = os.path.join(JFC, "fonts", "Quicksand.ttf")
def font_curvy(size, wght=800):
    f = ImageFont.truetype(F_BALOO, size)
    f.set_variation_by_axes([wght])
    return f
def font_quick(size, wght=700):
    f = ImageFont.truetype(F_QUICK, size)
    f.set_variation_by_axes([wght])
    return f

LOGO_SRC = Image.open(os.path.join(JFC, "logo_flirtspot_big.png")).convert("RGBA")
LOGO_SRC = LOGO_SRC.crop(LOGO_SRC.getbbox())
ICON_SRC = Image.open(os.path.join(JFC, "icon_flirtspot_hearts.png")).convert("RGBA")
ICON_SRC = ICON_SRC.crop(ICON_SRC.getbbox())

# ---- geometry ----
CX, CY, R = 540, 930, 430          # radar disc
M2PX = R / 150.0                   # 150m radius -> px
LOGO_CY_OPEN = 880                 # logo open, centred
LOGO_W_OPEN = 960
LOGO_W_CTA, LOGO_CY_CTA = 720, 330

def ease_out(t):  return 1 - (1 - t) ** 3
def ease_back(t): return 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2
def clamp01(t):   return max(0.0, min(1.0, t))
def seg(f, a, b): return clamp01((f - a) / (b - a)) if b > a else (1.0 if f >= b else 0.0)
def lerp(a, b, t): return a + (b - a) * t

def glow(layer, r, passes=1):
    g = layer
    for _ in range(passes): g = g.filter(ImageFilter.GaussianBlur(r))
    return g

def vgrad_full(c_top, c_bot):
    strip = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        strip.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(c_top, c_bot)))
    return strip.resize((W, H))

def vgrad_span(c_top, c_bot, y0, y1):
    """Full-frame W×H vertical gradient, clamped outside y0..y1 (so text gradient spans just its zone)."""
    strip = Image.new("RGB", (1, H))
    for y in range(H):
        t = clamp01((y - y0) / max(1, y1 - y0))
        strip.putpixel((0, y), tuple(int(a + (b - a) * t) for a, b in zip(c_top, c_bot)))
    return strip.resize((W, H))

def draw_tracked(d, x, y, text, fnt, fill, tr=0, mid=True):
    wtot = sum(d.textlength(c, font=fnt) for c in text) + tr * (len(text) - 1)
    if mid: x -= wtot / 2
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill, anchor="lm")
        x += d.textlength(c, font=fnt) + tr

def heart_poly(cx, cy, s, rot=0.0):
    pts = []
    for i in range(72):
        t = 2 * math.pi * i / 72
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        if rot:
            x, y = x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + x * s, cy + y * s))
    return pts

GP_BLUE, GP_YELLOW, GP_RED, GP_GREEN = (0, 201, 255), (255, 224, 0), (255, 58, 68), (0, 240, 118)
def play_icon(d, ix, iy, s, alpha=255):
    """Google Play triangle — top-left blue, bottom-left red, top-right yellow, bottom-right green."""
    P = lambda u, v: (ix + u * s, iy + v * s)
    L, Lm, Lb = (0.06, 0.02), (0.06, 0.50), (0.06, 0.98)
    Um, Dm, C, R = (0.50, 0.26), (0.50, 0.74), (0.36, 0.50), (0.96, 0.50)
    d.polygon([P(*L), P(*Um), P(*C), P(*Lm)], fill=GP_BLUE + (alpha,))
    d.polygon([P(*Lm), P(*C), P(*Dm), P(*Lb)], fill=GP_RED + (alpha,))
    d.polygon([P(*C), P(*Um), P(*R)], fill=GP_YELLOW + (alpha,))
    d.polygon([P(*C), P(*R), P(*Dm)], fill=GP_GREEN + (alpha,))

BADGE_W, BADGE_H = 740, 188
def badge_layer(alpha):
    lay = Image.new("RGBA", (BADGE_W + 40, BADGE_H + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = 20, 20, 20 + BADGE_W, 20 + BADGE_H
    d.rounded_rectangle([x0, y0, x1, y1], radius=34, fill=(13, 15, 20, int(242 * alpha / 255)),
                        outline=WHITE + (int(215 * alpha / 255),), width=4)
    play_icon(d, x0 + 50, y0 + BADGE_H / 2 - 60, 120, int(alpha))
    tx = x0 + 50 + 120 + 40
    d.text((tx, y0 + 54), "GET IT ON", font=font(36), fill=(198, 204, 214, alpha), anchor="lm")
    d.text((tx, y0 + 122), "Google Play", font=font(80), fill=WHITE + (alpha,), anchor="lm")
    return lay

def sweep_band_x(cx, sigma=90):
    band = Image.new("L", (W, H), 0)
    px = band.load()
    for x in range(W):
        a = int(255 * math.exp(-((x - cx) ** 2) / (2 * sigma ** 2)))
        if a:
            for y in range(0, H, 2):
                px[x, y] = a
                if y + 1 < H: px[x, y + 1] = a
    return band

def shear_mask_rows(m, k=-0.14, cy_ref=None):
    bb = m.getbbox()
    if not bb: return m
    y0, y1 = bb[1], bb[3]
    cy = cy_ref if cy_ref is not None else (y0 + y1) / 2
    out = Image.new("L", (W, H), 0)
    for y in range(y0, y1):
        out.paste(m.crop((0, y, W, y + 1)), (int(k * (y - cy)), y))
    return out

def radial_blob(color, alpha, size):
    lay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([size*0.05, size*0.05, size*0.95, size*0.95], fill=color + (alpha,))
    return glow(lay, size // 10)

# static ambients (pre-blurred once, cheap per-frame offset)
AMB_CORAL = radial_blob(CORAL, 88, 900)
AMB_CYAN  = radial_blob(CYAN,  72, 800)
VGRAD_HERE  = vgrad_span(CYAN, (0, 114, 255), 1400, 1660)     # HERE — flirt blue
VGRAD_NOW   = vgrad_span(CORAL, GOLD, 1400, 1660)             # NOW — spot coral/gold
VGRAD_APP   = vgrad_span(CORAL, GOLD, 1120, 1240)              # GET THE APP line

# blips: (metres, angle_deg, label, spawn_frame)
BLIPS = [
    (120, 150, "120M", 62),
    ( 63,  35,  "63M", 80),
    ( 88, -25,  "88M", 98),   # TARGET — locked
    ( 42, 115,  "42M", 116),
]
def blip_xy(m, adeg):
    r = m * M2PX; a = math.radians(adeg)
    return CX + r * math.cos(a), CY - r * math.sin(a)
TARGET = blip_xy(*BLIPS[2][:2])

def render_frame(f):
    img = Image.new("RGB", (W, H), BG).convert("RGBA")
    fx  = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # glow feed
    ov  = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # crisp layer
    d   = ImageDraw.Draw(ov)
    dfx = ImageDraw.Draw(fx)

    # ---- bg gradient + drifting ambients ----
    img.paste(vgrad_full(BG, BG_DEEP), (0, 0))
    wa = math.sin(f / N * 2 * math.pi)
    img.alpha_composite(AMB_CORAL, (int(-60 + 22 * wa), int(80 + 18 * wa)))
    img.alpha_composite(AMB_CYAN,  (int(360 - 22 * wa), int(1180 - 18 * wa)))

    # ================= 1) LOGO OPEN (f8–50) =================
    p_logo = seg(f, 8, 30)
    p_logo_out = seg(f, 42, 50)
    if p_logo > 0 and p_logo_out < 1:
        alpha = int(255 * p_logo * (1 - p_logo_out))
        k = 0.90 + 0.10 * ease_out(p_logo) + 0.012 * p_logo_out
        h = int(LOGO_W_OPEN / (LOGO_SRC.width / LOGO_SRC.height) * k)
        w = int(h * (LOGO_SRC.width / LOGO_SRC.height))
        lg = LOGO_SRC.resize((w, h), Image.LANCZOS)
        lg.putalpha(lg.getchannel("A").point(lambda v: v * alpha // 255))
        x0, y0 = CX - w // 2, LOGO_CY_OPEN - h // 2
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(lg, (x0, y0))
        if 14 <= f <= 42:  # light sweep
            band = sweep_band_x(160 + 900 * seg(f, 14, 38))
            mask = Image.new("L", (W, H), 0)
            mask.paste(lg.getchannel("A"), (x0, y0))
            lay.paste((225, 245, 255, alpha), (0, 0), ImageChops.multiply(band, mask))
        fx.alpha_composite(glow(lay, 12))
        ov.alpha_composite(lay)

    # ================= 2) RADAR SCENE (f44–194) =================
    r_life = seg(f, 44, 60) * (1 - seg(f, 182, 194))
    if r_life > 0:
        # HUD line
        p_hud = seg(f, 52, 64)
        if p_hud > 0:
            draw_tracked(d, CX, 452, "RADAR // FLIRTSPOT · 150M RADIUS · BRADFORD LIVE",
                         font_reg(26), CYAN + (int(200 * p_hud * r_life),), 6)
        # rings + cross
        for rr, lab, al in ((R, "150M", 44), (318, "100M", 34), (205, "50M", 30)):
            d.ellipse([CX-rr, CY-rr, CX+rr, CY+rr], outline=FG + (int(al * r_life),), width=3)
            lx, ly = CX + rr * 0.707, CY - rr * 0.707
            d.text((lx + 8, ly - 24), lab, font=font_reg(22), fill=FG + (int(110 * r_life),))
        d.line([CX, CY - R, CX, CY + R], fill=FG + (int(14 * r_life),), width=1)
        d.line([CX - R, CY, CX + R, CY], fill=FG + (int(14 * r_life),), width=1)
        # sweep beam (cropped square layer)
        if f >= 46:
            th = -70 + (f - 46) * 5.3
            S = 2 * R + 8
            sl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
            sd = ImageDraw.Draw(sl)
            sd.pieslice([6, 6, S-6, S-6], th - 14, th, fill=CYAN + (int(14 * r_life),))
            sd.pieslice([6, 6, S-6, S-6], th, th + 42, fill=CYAN + (int(30 * r_life),))
            sl = glow(sl, 6)
            ov.alpha_composite(sl, (CX - S // 2, CY - S // 2))
        # YOU dot + pings
        p_you = seg(f, 50, 58)
        if p_you > 0:
            ya = int(255 * p_you * r_life)
            d.ellipse([CX-11, CY-11, CX+11, CY+11], fill=FG + (ya,))
            dfx.ellipse([CX-16, CY-16, CX+16, CY+16], fill=FG + (int(120 * p_you),))
            for ph in (0.0, 0.5):
                pt = ((f - 56) / 30 + ph) % 1.0
                if 0 <= f - 56:
                    pr = pt * R
                    pa = int(90 * (1 - pt) * r_life)
                    if pa > 0:
                        d.ellipse([CX-pr, CY-pr, CX+pr, CY+pr], outline=REDPINK + (pa,), width=3)
        # blips + labels
        for m, a, lab, f0 in BLIPS:
            p_b = seg(f, f0, f0 + 5)
            if p_b > 0:
                bx, by = blip_xy(m, a)
                pulse = 0.85 + 0.15 * math.sin((f - f0) * 0.35)
                s = int(13 * p_b * pulse)
                al = int(255 * p_b * r_life)
                d.ellipse([bx-s, by-s, bx+s, by+s], fill=REDPINK + (al,))
                dfx.ellipse([bx-s*2, by-s*2, bx+s*2, by+s*2], fill=REDPINK + (int(110 * p_b),))
                p_l = seg(f, f0 + 3, f0 + 8)
                d.text((bx + 18, by - 26), lab, font=font_reg(24), fill=FG + (int(190 * p_l * r_life),))
        # reticle lock on TARGET
        p_ret = seg(f, 150, 158)
        if p_ret > 0:
            tx, ty = TARGET
            k = 1.6 - 0.6 * ease_back(p_ret)
            arm = int(46 * k); th_ = 5
            al = int(230 * p_ret * r_life)
            for sx in (-1, 1):
                for sy in (-1, 1):
                    cxp, cyp = tx + sx * arm, ty + sy * arm
                    d.line([cxp, cyp, cxp - sx * 22, cyp], fill=CYAN + (al,), width=th_)
                    d.line([cxp, cyp, cxp, cyp - sy * 22], fill=CYAN + (al,), width=th_)
            if f > 158:
                ra = int(70 + 50 * math.sin((f - 158) * 0.4))
                d.ellipse([tx-arm-8, ty-arm-8, tx+arm+8, ty+arm+8], outline=CYAN + (int(ra * r_life),), width=2)

    # ---- MESSAGE (f120–194) · Quicksand, per-word brand gradients ----
    p_m1 = seg(f, 120, 132)
    if p_m1 > 0:
        draw_tracked(d, CX, 1400 + 26 * (1 - ease_out(p_m1)), "MATCH THE VIBE",
                     font_quick(56, 600), FG + (int(235 * p_m1 * (1 - seg(f, 182, 194))),), 16)
    p_m2 = seg(f, 134, 146)
    if p_m2 > 0:
        dm = ImageDraw.Draw(Image.new("L", (1, 1)))
        size = int(138 * (0.82 + 0.18 * ease_back(p_m2)))
        tr = 16
        def wword(wd, sz): return sum(dm.textlength(c, font=font_quick(sz)) for c in wd) + tr * (len(wd) - 1)
        amp_sz = int(size * 0.62)
        total = wword("HERE", size) + 36 + wword("&", amp_sz) + 36 + wword("NOW", size)
        if total > 950:
            size = int(size * 950 / total); amp_sz = int(size * 0.62)
            total = wword("HERE", size) + 36 + wword("&", amp_sz) + 36 + wword("NOW", size)
        fade = int(p_m2 * (1 - seg(f, 182, 194)) * 255)
        x = CX - total / 2
        ybase = 1548 + 30 * (1 - ease_out(p_m2))
        for word, sz, grad in (("HERE", size, VGRAD_HERE), ("&", amp_sz, None), ("NOW", size, VGRAD_NOW)):
            m = Image.new("L", (W, H), 0)
            draw_tracked(ImageDraw.Draw(m), x, ybase, word, font_quick(sz), 255, tr, mid=False)
            m = shear_mask_rows(m, cy_ref=1548)
            m = m.point(lambda v: v * fade // 255)
            lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            if grad is None:
                lay2.paste(FG + (200,), (0, 0), m)
            else:
                lay2.paste(grad, (0, 0), m)
            fx.alpha_composite(glow(lay2, 10))
            ov.alpha_composite(lay2)
            x += wword(word, sz) + 36

    # ================= 3) SPARK -> LOGO BLOOM (f158–222) =================
    p_sp = seg(f, 158, 176)
    if p_sp > 0 and f <= 182:
        t = ease_out(p_sp)
        hx, hy = lerp(CX, TARGET[0], t), lerp(CY, TARGET[1], t)
        d.line([CX, CY, hx, hy], fill=FG + (235,), width=7)
        dfx.line([CX, CY, hx, hy], fill=WHITE + (150,), width=18)
        s = int(15 + 6 * math.sin(f * 0.9))
        d.ellipse([hx-s, hy-s, hx+s, hy+s], fill=WHITE + (255,))
        dfx.ellipse([hx-s*3, hy-s*3, hx+s*3, hy+s*3], fill=WHITE + (120,))
    if 174 <= f <= 182:  # arrival flash
        p_fl = seg(f, 174, 179)
        fr = int(30 + 380 * p_fl)
        d.ellipse([CX-fr, CY-fr, CX+fr, CY+fr], outline=WHITE + (int(200 * (1 - p_fl)),), width=6)
    p_h = seg(f, 178, 206)
    if p_h > 0:
        fade = 1 - seg(f, 208, 220)
        k = 0.15 + 0.85 * ease_back(p_h)
        k *= 1 + (0.02 * math.sin((f - 178) * 0.4) if p_h >= 1 else 0)
        lw = int(700 * k)
        lh = int(lw / (LOGO_SRC.width / LOGO_SRC.height))
        lg = LOGO_SRC.resize((lw, lh), Image.LANCZOS)
        lg.putalpha(lg.getchannel("A").point(lambda v: v * int(255 * fade) // 255))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(lg, (CX - lw // 2, int(CY - 10 - lh / 2)))
        fx.alpha_composite(glow(lay, 16))
        ov.alpha_composite(lay)

    # ================= 4) CTA / Google Play (f214–300) =================
    p_cta = seg(f, 214, 300)
    if p_cta > 0:
        out_f = seg(f, 290, 299)
        p_lg = seg(f, 216, 228)
        # mini logo
        if p_lg > 0:
            h = int(LOGO_W_CTA / (LOGO_SRC.width / LOGO_SRC.height) * (0.9 + 0.1 * ease_back(p_lg)))
            w = int(h * (LOGO_SRC.width / LOGO_SRC.height))
            lg = LOGO_SRC.resize((w, h), Image.LANCZOS)
            lg.putalpha(lg.getchannel("A").point(lambda v: v * int(p_lg * 255) // 255))
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.alpha_composite(lg, (CX - w // 2, LOGO_CY_CTA - h // 2))
            fx.alpha_composite(glow(lay, 9))
            ov.alpha_composite(lay)
        # app icon (intertwined hearts) above badge
        p_ic = seg(f, 220, 232)
        if p_ic > 0:
            s = int(200 * (0.7 + 0.3 * ease_back(p_ic))) * (1 + (0.02 * math.sin((f - 232) * 0.35) if f > 232 else 0))
            s = int(s)
            ic = ICON_SRC.resize((s, s), Image.LANCZOS)
            ic.putalpha(ic.getchannel("A").point(lambda v: v * int(p_ic * 255) // 255))
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.alpha_composite(ic, (CX - s // 2, int(690 - s / 2)))
            fx.alpha_composite(glow(lay, 9 + 2 * math.sin(f * 0.3)))
            ov.alpha_composite(lay)
        # ping rings behind badge
        pt = ((f - 222) / 37) % 1.0
        if f >= 222:
            pr = 260 + pt * 340
            pa = int(60 * (1 - pt))
            if pa > 0:
                d.ellipse([CX-pr, 960-pr, CX+pr, 960+pr], outline=REDPINK + (pa,), width=3)
        # Google Play badge
        p_q = seg(f, 224, 238)
        if p_q > 0:
            kq = 0.8 + 0.2 * ease_back(p_q)
            bl = badge_layer(255)
            bw, bh = int(bl.width * kq), int(bl.height * kq)
            bl = bl.resize((bw, bh), Image.LANCZOS)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.alpha_composite(bl, (CX - bw // 2, int(960 - bh / 2)))
            fx.alpha_composite(glow(lay, 8 + 2 * math.sin(f * 0.3)))
            ov.alpha_composite(lay)
        # GET THE APP AT FLIRT.SPOT
        p_s = seg(f, 238, 248)
        if p_s > 0:
            dm = ImageDraw.Draw(Image.new("L", (1, 1)))
            size = int(58 * (0.85 + 0.15 * ease_back(p_s)))
            txt = "GET THE APP AT FLIRT.SPOT"
            wtot = sum(dm.textlength(c, font=font_quick(size)) for c in txt) + 10 * (len(txt) - 1)
            if wtot > 960: size = int(size * 960 / wtot)
            m = Image.new("L", (W, H), 0)
            draw_tracked(ImageDraw.Draw(m), CX, 1190 + 20 * (1 - ease_out(p_s)), txt,
                         font_quick(size), 255, 10)
            m = shear_mask_rows(m, cy_ref=1190)
            lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay2.paste(VGRAD_APP, (0, 0), m)
            fx.alpha_composite(glow(lay2, 9))
            ov.alpha_composite(lay2)
        # FREE · 18+
        p_i = seg(f, 244, 254)
        if p_i > 0:
            draw_tracked(d, CX, 1350 + 10 * (1 - ease_out(p_i)), "FREE · 18+",
                         font(42), FG + (int(220 * p_i),), 10)
        # fade CTA out for seamless black loop point
        if out_f > 0:
            pass  # handled by global fade below

    # ---- composite + global fade in/out (loop point = black both ends) ----
    out = Image.alpha_composite(img, glow(fx, 2))
    out = Image.alpha_composite(out, ov)
    fade = max(1 - seg(f, 0, 6), seg(f, N - 7, N - 1))
    if fade > 0:
        out = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 255)), out,
                              Image.new("L", (W, H), int(255 * fade)))
    return out.convert("RGB")

if __name__ == "__main__":
    prevs = {28: "preview-1-logo.png", 130: "preview-2-radar-message.png",
             168: "preview-3-lock-spark.png", 200: "preview-4-logo-bloom.png", 252: "preview-5-cta-play.png"}
    for f in range(N):
        fr = render_frame(f)
        fr.save(f"{OUT}/frame_{f:03d}.png")
        if f in prevs: fr.save(os.path.join(_here, prevs[f]))
        if f % 25 == 0: print(f"frame {f}/{N}")
    print("done:", N, "frames")
