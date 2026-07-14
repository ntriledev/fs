# FlirtSpot — BGC High Street 3D LED · Creative Brief & Spec

**Format:** Naked-eye 3D LED spectacular, Bonifacio Global City, Manila
**Booking:** Blindspot, per-play (~$0.46/play), 6–11 PM golden hours
**Deliverable:** 15.0-second seamless loop · 1920×1080 · H.264 · 30fps · MP4
**Prototype:** `ads/bgc-3d-led-creative.html` (open in browser — this IS the spot)

**Structure (locked):** LOGO open → radar + message **"Match the vibe here & now"** → spark + heart → CTA **"Get the app at flirt.spot"**.

---

## 1. The idea in one line

**The radar IS the ad.** FlirtSpot's product mechanic — a proximity radar finding
real people within 150m — rendered as a 3D LED spectacle that makes every person
walking BGC High Street feel like they're being *found*.

No models, no stock couples, no URL, no QR (premium 3D screens reject both as
pedestrian hazards). Just the brand's signature visual, made impossible to look
away from. It is the purest possible expression of what the app does.

---

## 2. Why it fits BGC at night

- **Audience match:** BGC High Street's evening crowd = young, affluent,
  phone-native, dating-age, walking slow. Exactly FlirtSpot's persona.
- **Format match:** 3D LED rewards a single hero object in depth. A radar dish
  receding into the screen with blips popping toward the viewer is *native* to
  the medium — not a 2D ad stretched onto a 3D screen.
- **Context match:** At 9 PM on High Street, the line "Someone within 150m is
  looking" lands as a dare, not a slogan. People are literally 150m from each
  other in a nightlife district.
- **Brand match:** Dark/neon palette (#07060b + magenta/cyan) is built for
  LED at night. High contrast = legible from across the street.

---

## 3. 15-second beat sheet (seamless loop)

All times are seconds within a 15.000s loop. Opens and closes on full black so
the loop is invisible to the eye. **Logo → message → CTA.**

| Time | % | Beat | What's on screen |
|---|---|---|---|
| **0.0–2.5** | 0–17% | **LOGO open** | From black, the **flirt.spot** wordmark gleams in dead-centre with a light sweep across it. Brand established before anything else moves. |
| **2.5–4.3** | 17–29% | **Radar ignites** | Wordmark fades. Radar plane tilts into 3D perspective. Range rings fade in (150/100/50/core). Cyan→magenta beam begins to rotate. HUD reads `RADAR // FLIRTSPOT · 150M RADIUS · BGC LIVE`. "YOU" dot ignites centre; ping-rings radiate. |
| **4.3–9.5** | 29–63% | **Blips + MESSAGE** | Blips spawn across the plane (42m / 88m / 120m / 63m). One locks (reticle snaps on). The hero message rises in the lower third, staggered: **"MATCH THE VIBE"** (white) then **"HERE & NOW"** (white→pink gradient). |
| **9.5–11.5** | 63–77% | **Lock · spark · heart** | Glowing filament sparks from YOU → the locked target, flashes white, ignites into the FlirtSpot **heart** bloom (pink→magenta). The payoff of "match the vibe here & now." |
| **11.5–15.0** | 77–100% | **CTA** | Heart clears. CTA lockup: mini flirt.spot logo + `GET THE APP / FREE · 18+`, then the domain **`flirt.spot`** big in white→pink gradient with a radar-ping motif behind it. Fades to black → seamless loop. |

**Copy (final):**
- Message: **Match the vibe — here & now**
- CTA: **Get the app at flirt.spot**

> The domain is written as `flirt.spot` (brand mark), not `https://www.flirt.spot`.
> It reads as a wordmark recall line, which passes premium-screen moderation far
> more cleanly than a raw URL — while still driving people to the domain.

---

## 4. Brand system (locked)

| Token | Value | Use |
|---|---|---|
| midnight | `#07060b` | background (always — white dies in LED glare) |
| spark | `#c850c0` | magenta primary |
| pulse | `#8B5CF6` | purple depth |
| glow | `#ff6b9d` | pink accent (blips, heart, tagline) |
| cyan | `#00C6FF` | sweep beam, HUD accent |
| blue | `#0072FF` | FLIRT wordmark gradient |
| fg | `#f3eef9` | "YOU" dot, headlines |

**Fonts:** Syne (display/headlines), DM Sans (body), JetBrains Mono (HUD
readouts — gives the techy/instrument feel that suits BGC's crowd).

**Wordmark:** `images/logo_flirtspot.svg` — blue FLIRT + cyan wifi + red SPOT,
with the red heart dotting the "i". Already embedded in the prototype.

---

## 5. The 3D / depth treatment

True naked-eye 3D on these spectaculars requires the **specific screen's
geometry map** (L-shaped corner fold, curved, etc.) to pre-distort content so it
reads correct from the prime viewing angle. The prototype simulates the 3D feel
for presentation; **final production needs the operator's geometry file**.

Depth techniques baked into the design (all carry to the 3D build):
- Radar plane tilted `rotateX(62°)` → reads as a horizontal dish receding into
  the screen.
- "YOU" dot and blips **counter-rotated** to face the camera, so they read as
  objects *floating above* the plane (the pop-out illusion).
- A lit **lower lip** along the bottom edge implies the corner-wrap panel —
  objects can be animated to rise *from* it in the final 3D build.
- Heavy bloom/volumetric glow on the sweep beam and heart.
- Vignette pushes focus to centre, tolerating the off-angle viewing typical of
  High Street pedestrian flow.

**Ask the operator / Blindspot for:** screen model, native resolution, viewing
angle, and the geometry/UV map before final render.

---

## 6. Technical delivery spec

| | |
|---|---|
| **Duration** | 15.000s exactly (frame-accurate for seamless loop) |
| **Resolution** | 1920×1080 (confirm native panel res with operator) |
| **Codec** | H.264, MP4 |
| **Frame rate** | 30 fps (450 frames total) |
| **Color** | Rec.709, full-range, high-bitrate (LED needs clean gradients — avoid banding, render at 10-bit if panel supports it) |
| **Safe area** | keep all type inside centre 80% |
| **Audio** | none (OOH) |
| **Loop seam** | frame 450 must equal frame 1 (full black) — no visible cut |

### Creative rules already satisfied (from premium-screen moderation)
- ✅ Motion throughout (required — no static logos)
- ✅ High contrast / dark bg (white backgrounds auto-reject in glare)
- ✅ Sans-serif only (Syne)
- ✅ No URL, no QR by default (toggle `QR: on` in the prototype adds a
  `SCAN @ FLIRT.SPOT` line — use **only** if the specific BGC screen allows QR;
  most 3D spectaculars don't)
- ✅ Logo is the hero, not a CTA

---

## 7. Production options

**A. Screen-record the prototype (fastest, free).** Open
`ads/bgc-3d-led-creative.html` in Chrome at fullscreen, screen-record exactly
one 15s loop with OBS at 1920×1080/30fps. Good enough for a Blindspot test buy.

**B. Rebuild in After Effects / Blender (recommended for the real buy).** Use
the prototype as the locked storyboard + timing. Rebuild the radar in true 3D
with the screen's geometry map for the genuine anamorphic pop-out. ~1–2 days of
motion-design work.

**C. Hand to Blindspot's creative team** — they sanity-check and approve before
go-live (~2 business days).

---

## 8. How to buy it once the MP4 is ready

1. Sign up at seeblindspot.com → free, no contract.
2. Map → Manila → filter **BGC / Bonifacio Global City** → **3D / iconic LED**.
3. Pick screens, set hours **6–11 PM**, see per-play price (~$0.46).
4. Upload the MP4, pass pre-check, go live in ~48h.
5. Run a **$1,500–3,000 test** (~3,000–6,000 verified plays over 1–2 weeks).
6. Read verified-play logs + tie to Play Store install spikes in those windows.

**Contextual swap idea (Blindspot-native, on-brand):** add a rule — *after
9 PM, swap tagline to "The spark doesn't wait."* The creative reacting to time
mirrors the app reacting to proximity. Signature move.

---

## 9. Notes & cautions

- ✅ **CTA uses `flirt.spot` as a brand-mark domain line**, not a raw URL
  (`https://…` / `www.`). Premium 3D screens reject raw URLs; the bare domain
  reads as part of the logo and passes moderation while still driving recall.
- ❌ No QR on the 3D spectacular — it gets rejected ("pedestrian hazard") and is
  pointless at plaza viewing distance anyway. Put QR on the *mall* and *transit
  shelter* screens, where viewers stand ~2m away.
- ❌ No human faces/couples — kills the mystery and raises ASC/APCON vetting
  risk. The radar implies a person *without showing one*.
- ❌ Don't run before 6 PM — BGC's crowd and the LED's contrast both peak after dark.
