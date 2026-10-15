# FlirtSpot — Singapore Campaign Runbook

**Goal:** app installs from DOOH, bought programmatically via Blindspot (seeblindspot.com).
**Date:** Jul 2026 · Singapore page verified live: 213 screens, 5 formats, plays from ~$0.30, no minimums.
**Position:** Plan C pivot after Manila/Cebu showed no live inventory (Singapore was ranked 🥈 after HCMC in `manila-campaign-strategy.md` §6).

---

## TL;DR

Same idea, new island: **the radar only speaks at pedestrian speed.**

1. **Verify live inventory first** (the Manila lesson: SEO city pages ≠ live supply — Singapore shows 213 screens but *most are Changi airport screens at ~$4.60/play*, which we skip).
2. **Pilot ($1.5–3k, 2 weeks):** Bugis/Somerset youth corridor + Orchard Road evening belt, 6–11 PM only. Creative exists (`bgc-3d-led-creative.html` → re-render per screen spec).
3. **Decide:** scale to multi-zone ($8–25k workhorse tier per Blindspot) or kill.

English-native market → no translation, no Taglish-style variants needed. Vetting is
permissive but keep the creative clean (radar, no faces/couples) — it already is.

---

## 1. Why this shape (Manila logic, Singapore geometry)

- **Bugis/Somerset = BGC High Street.** Youth/mid-market retail corridor, high-energy
  footfall, younger audience (Blindspot scores: visibility 8, dwell 8, footfall 8). Evening
  shoppers walking slow with phones = the product demo.
- **Orchard Road = the flagship belt.** 2.5 km LED corridor, highest retail footfall in
  the city; shifts to social/tourism after dark — *different audience, same screens* →
  the 9 PM contextual swap ("The spark doesn't wait.") is native here.
- **Malls 12–8 PM** hold a long dwell window → the QR-enabled cut goes here (2 m
  viewing distance), same QR rule: 3D/premium = no QR; mall/street = QR.
- **Skip Changi** (most of SG supply, ~$4.60/play): airport audience is *leaving the
  island* — zero proximity value for a 150 m radar app.
- **Skip MRT for installs** (moving viewers, 6 dwell score); revisit only for a later
  brand-awareness phase. **CBD/Raffles Place** is B2B daytime — wrong persona for the pilot.
- Singapore doesn't have one rush hour — rotating audiences share the same streets
  (commuters 7:30–10 AM / 5–8 PM, shoppers 12–8 PM, nightlife 8 PM–1 AM). Hourly buying
  is the only model that matches; typically saves 30%+ vs a flat 4-week flight.

## 2. Zones & dayparts (pilot)

| Placement | Daypart | Why | Creative variant |
|---|---|---|---|
| **Bugis / Somerset** street & mall screens | 6–11 PM (retail + evening) | Youth corridor, FlirtSpot persona | radar loop, English (locked) |
| **Orchard Road** LED belt / mall screens | 6–11 PM, Fri/Sat to 1 AM if bookable | After-dark social/tourism shift | radar loop + 9 PM swap |
| Mall screens (Orchard, suburban) | 12–8 PM optional add-on | long dwell, 2 m distance | **QR cut** ("SCAN @ FLIRT.SPOT") |

**Pricing reality (Blindspot, June 2026):** urban/street panels from ~$0.30/play
(~$150 buys hourly slots) · mall & retail $0.40–4 · Orchard & Marina digital
$0.60–6 · MRT $0.30–3 · Changi $0.60–6 (skipped).

**Pilot math:** $1.5–3k on street/mall panels at $0.30–1.50/play ≈ **2,000–8,000
verified plays** over 2 weeks — same envelope as the BGC pilot.

## 3. Copy

English-native market — the locked lines carry over unchanged:

| Slot | Line |
|---|---|
| Message | **Match the vibe — here & now** |
| Late swap (9 PM+) | **The spark doesn't wait.** |
| CTA | **Get the app at flirt.spot** (+ `FREE · 18+` marking) |

Rules carried over: no faces/couples, dark/neon bg (#07060b + magenta/cyan), logo as
hero, `flirt.spot` as wordmark (not a raw URL) on premium screens, 18+ on all cuts.

Singapore ad standards (ASAS) are conservative on anything suggestive — this creative
has no people and no innuendo in the visuals, so it should clear vetting cleanly. The
18+ marking + "FREE" stays on every cut.

## 4. How to publish on seeblindspot.com — step by step

1. **Account:** <https://portal.seeblindspot.com/join> — free, no card, no sales call.
2. **Verify live inventory FIRST.** Open the map → search **Singapore** → check that
   Bugis/Somerset + Orchard screens show live availability and per-play prices. The
   city page is marketing; the portal is truth. If supply is thin, message support
   (or hello@seeblindspot.com) asking which SG zones are actually live *today*.
3. **Pick screens & hours.** Filter by zone (Orchard Road, Bugis/Somerset) and format
   (street-level & urban panels, mall & retail). Each card shows per-play price,
   plays/hour, and exact creative specs (resolution, orientation, file format).
4. **See the price before committing.** Build the plan screen-by-screen, hour-by-hour;
   running total is always visible. Set a campaign/daily budget cap.
   - *Alternative:* hand it to **Blinky** (their AI planner) with the brief:
     *"Launch FlirtSpot, a dating app, in Singapore. $2,500, two weeks, evening hours
     6–11 PM, pedestrian retail screens in Bugis/Somerset and Orchard Road. Skip
     airports and transit."* — it writes a screen-by-screen plan into your account;
     approve/edit before anything books.
5. **Upload creative.** Re-render `bgc-3d-led-creative.html` per each screen's spec
   (OBS screen-record, H.264 MP4, seamless 15 s loop, frame-450 = frame-1 black).
   You can run different creative per screen/city — QR cut only on mall screens.
6. **Approval.** AI pre-check → human sanity-check → screen-operator approval.
   Singapore content approval averages **~2 business days**; go-live can be same-day
   after that.
7. **Run & measure.** Pay only for verified plays; pause anytime. Track SG Play Store
   install spikes inside the 6–11 PM window vs the verified play logs (same
   measurement design as the BGC pilot).

**Gate:** only scale if install lift is measurable in the evening window.

## 5. Budget tiers (Blindspot SG benchmarks)

| Phase | Spend | Buys |
|---|---|---|
| Pilot (district test) | $800–2.5k | hourly burst on one/two zones, 1–2 weeks |
| Multi-zone push (if pilot wins) | $8–25k | Orchard + Marina + CBD peak windows, 4 weeks |
| Islandwide flagship | $40k+ | Orchard + Marina icons + MRT takeover |

No minimums, no contracts, no retainers, no platform fees.

## 6. Production checklist

- [ ] Verify live SG inventory in the portal (before any creative work)
- [ ] Confirm app is live on SG Play Store / App Store + flirt.spot resolves in SG
- [ ] Pull per-screen specs for chosen Bugis/Orchard screens from their cards
- [ ] Re-render radar loop at each spec (15 s seamless, H.264, 30 fps)
- [ ] Mall QR cut ("SCAN @ FLIRT.SPOT") for 12–8 PM add-on
- [ ] 9 PM contextual swap rule set in campaign settings
- [ ] Measurement: SG Play Store console, 6–11 PM window, control vs play logs
- [ ] Fallback if SG supply is thin: HCMC pilot (Nguyen Hue, $0.34–0.54/play) per §6 of the Manila doc
