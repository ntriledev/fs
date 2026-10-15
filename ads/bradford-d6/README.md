# FlirtSpot × JCDecaux Bradford D6 "Broadway IFO 33" (MFRAME 931714-123)

**Deliverable:** `flirtspot-bradford-d6-12s-1080x1920.mp4`
**Screen:** Broadway IFO 33, Bradford city centre · via Blindspot ($0.08/play, 480+ plays/48h)
**File:** H.264 High · yuv420p · 25fps · exactly 12.000s · 1080×1920 portrait · loop point = black both ends

Google Play badge CTA (install intent, no scanning friction).

## 12-second flow: LOGO → RADAR + MESSAGE → SPARK/LOGO BLOOM → PLAY BADGE

| Time | Beat | On screen |
|---|---|---|
| 0.0–0.3s | From black | Global fade-in (seamless loop point) |
| 0.3–2.0s | **LOGO open** | flirt.spot wordmark gleams in centre (960px) with L→R light sweep |
| 1.8–7.8s | **RADAR** | Top-down radar disc, HUD `RADAR // FLIRTSPOT · 150M RADIUS · BRADFORD LIVE`, cyan sweep, YOU dot + pings, blips with distance labels (120M/63M/88M/42M) |
| 4.8–5.9s | **MESSAGE** | "MATCH THE VIBE" (Quicksand) · **HERE** (cyan→blue) **&** **NOW** (coral→gold) — Quicksand Bold 700, italic lean, per-word brand gradients |
| 6.0–6.3s | **LOCK** | Cyan reticle snaps onto the 88M blip |
| 6.3–7.1s | **SPARK** | White-hot filament travels YOU → target, arrival flash |
| 7.1–8.8s | **LOGO BLOOM** | flirt.spot wordmark blooms centre (scales in, glow pulse) |
| 8.6–12.0s | **CTA** | Mini logo top · app icon (intertwined hearts) · **Google Play badge** (GET IT ON / Google Play, 4-colour play mark, pings behind) · "GET THE APP AT FLIRT.SPOT" (coral→gold) · FREE · 18+ · fade to black |

## Build notes

- Google Play badge drawn in-code (4-colour play triangle ≈ official mark) — same approach as the JFC London spot, no trademark asset files.
- HERE/NOW + GET THE APP lines: **Quicksand** variable (wght 700, OFL) — sleek geometric face; "MATCH THE VIBE" at wght 600. Baloo 2 no longer used here.
- Palette = BGC v3 warm system (coral #FF512F / gold #F09819 / red-pink #FF2D55 / cyan #00C6FF / blue #0072FF on #0a0610) — consistent across all FlirtSpot DOOH.
- Fonts/assets reused from `../jfc-london/`: `logo_flirtspot_big.png`, `icon_flirtspot_hearts.png`, `fonts/Quicksand.ttf`.
- Attribution: installs land on the Play Store listing; tag the listing URL with `utm_source=dooh&utm_medium=bradford` in Play Console campaigns if supported, or restore the QR variant (git history) for direct landing attribution.

## Rebuild

```
cd ads/bradford-d6
python3 gen_12s.py            # ~2 min → build/frame_*.png + previews
../jfc-london/node_modules/ffmpeg-static/ffmpeg -y -framerate 25 -i build/frame_%03d.png \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high \
  -level 4.2 -movflags +faststart -r 25 flirtspot-bradford-d6-12s-1080x1920.mp4
```

## Upload to Blindspot

1. Book Broadway IFO 33, hours 6–9 PM (or 6–11 PM) Thu–Sat.
2. Upload MP4 → passes pre-check (12s, 1080×1920, H.264, no audio, dark bg, sans-serif, motion throughout).
3. Live in ~48h; read verified-play logs, tie to Play Console installs (Bradford-geo spike in the Thu–Sat 6–9 PM window).
