# FlirtSpot × JFC Training College screen — London

**Deliverable:** `flirtspot-jfc-london-3s-1920x1080.mp4` (v4)
**Screen:** JFC Training College, London · spec MP4 1920×1080 · 3s spot
**File:** H.264 · yuv420p · high profile · 30fps · exactly 3.000s · ~439KB · seamless loop (opens/closes on black)

## 3-second flow: FULLSCREEN logo → HERE & NOW → Google Play badge

| Time | Beat | On screen |
|---|---|---|
| 0.0–0.5s | From black | Dim radar backdrop (rings + slow beam) fades in |
| 0.1–0.5s | **flirt.spot FULLSCREEN** | Official logo scales in edge-to-edge (x≈44–1874, ~96% width): blue "flirt" · heart-i · wifi icon · orange "spot" |
| 0.3–0.9s | **In motion** | Light sweep travels L→R across the logo |
| 0.9–1.5s | **HERE / NOW** | "HERE" slams in BIG filling the empty left, then "NOW" mirrors on the right — **Baloo 2 ExtraBold** (curvy rounded face, SIL OFL), italic lean, flirt-blue / spot-red gradients, no underlines |
| 1.3–1.7s | **Badge lockup** | Google Play badge + intertwined-hearts app icon bounce in centre-bottom, framed between HERE and NOW |
| 1.5s+ | Pulse | Badge glow pulses; **FREE · 18+** beneath |
| 2.8–3.0s | To black | Global fade → seamless loop point |

The logo never shrinks or leaves — full-screen the entire spot. Download prompt = the badge itself.

## Build notes

- Logo: `logo_flirtspot_big.png` (resvg raster of `../../images/logo_flirtspot.svg`, 2080×640, alpha-trimmed for full bleed)
- App icon: `icon_flirtspot_hearts.png` (resvg raster of `../../images/icon_flirtspot_picsart.svg` — skyblue circle, wifi arcs, intertwined heart outlines)
- Words HERE/NOW: Baloo 2 variable (wght 800) from Google Fonts (OFL) — `fonts/Baloo2.ttf`
- Play badge drawn in-code (4-colour triangle ≈ Google Play mark) — no trademark asset files needed
- Accent colors follow the logo redGrad (#FF512F)

## Rebuild

```
cd ads/jfc-london
python3 gen_3s.py
node_modules/ffmpeg-static/ffmpeg -y -framerate 30 -i build/frame_%03d.png \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -profile:v high \
  -level 4.2 -movflags +faststart -r 30 flirtspot-jfc-london-3s-1920x1080.mp4
```

Previews: `preview-1-fullscreen-logo.png` (0.4s) · `preview-2-here-blue.png` (1.3s) · `preview-3-triptych.png` (2.3s)
