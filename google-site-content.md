# FlirtSpot Alpha — Google Sites content (ready to paste)

> Goal: a free Google Site (sites.google.com) that engages alpha testers
> and funnels them into the Google Group + Play alpha.

---

## ⚠️ About "embedding the group" (read first)

Google Groups sends `X-Frame-Options: SAMEORIGIN`, so the group page
CANNOT be shown in an iframe on a Google Site (it will appear blank).
This is a Google-side restriction, not something fixable in the embed code.

**Working approach:** use a big "Join the group" button that opens the
group in a new tab. This is what Google Sites itself recommends now.

Optional embed snippet (will link out, won't render inline — but keeps
the CTA framed on your page):

```html
<div style="text-align:center;padding:24px;border:1px solid #c850c0;border-radius:16px;background:#0f0d17;color:#fff;font-family:'DM Sans',sans-serif">
  <p style="font-size:20px;font-weight:700;margin:0 0 4px">💜 The Tester Lounge</p>
  <p style="opacity:.7;margin:0 0 16px">Where sparks get shipped. Join the group to talk to the team and other testers.</p>
  <a href="https://groups.google.com/g/flirt-spot" target="_blank" rel="noopener"
     style="display:inline-block;padding:12px 28px;border-radius:999px;background:#c850c0;color:#fff;text-decoration:none;font-weight:600">
     👉 Open the Google Group
  </a>
</div>
```

In Google Sites: **Insert → Embed code → paste**.

---

## PAGE SETUP

1. Go to **sites.google.com** → **Create new site** (blank).
2. Top-right pencil ✏️ to edit. Page name (top-left): **FlirtSpot Alpha**.
3. Site name / publish path: **flirtspot-alpha** → Publish.

Theme: right sidebar **Themes → "Ink"** (dark) for closest match to brand.

---

## SECTION 1 — HERO (Title + subtitle)

Add: **Insert → Text box** at top. Paste:

### Title (Heading 1)
**FlirtSpot Alpha — Tester Hub**

### Subtitle (normal text, smaller)
You're early. 👀 Help shape the world's first self-cleaning
proximity-match app — anonymous profiles, real sparks, data that
auto-wipes. Catch the vibe, break things, tell us everything.

---

## SECTION 2 — TWO BIG BUTTONS

**Insert → Button** (do this twice, side by side):

| Button text | Link |
|---|---|
| 🚀 **Get the Alpha (Play)** | `https://play.google.com/apps/testing/spot.flirt.app` |
| 💜 **Join the Tester Group** | `https://groups.google.com/g/flirt-spot` |

---

## SECTION 3 — "HOW TO GET ACCESS" (3 steps)

**Insert → Text box**, Heading 2:

### How to get access in 3 steps

Then a numbered list:

1. **Join the group** — tap *Join the Tester Group* above and click
   **Join group** (you need any Google account; it's instant).
2. **Open the alpha** — tap *Get the Alpha (Play)*, sign in with the
   same Google account, tap **Become a tester**.
3. **Download + open** — install from Play, run the radar, send a Flirt. ✨

> 💡 Must do step 1 first — the alpha only unlocks for group members.

---

## SECTION 4 — WHY TEST FLIRTSPOT

**Insert → Text box**, Heading 2 + bullets:

### Why this is worth your time

- 🔒 **Truly anonymous** — no name, no email, no phone number. Ever.
- 🧼 **Self-cleaning** — your profile + selfies auto-wipe 24h after your last activity.
- 📡 **Real proximity** — radar finds real people within 150m, not a swipe deck.
- ⏱ **60-second Flirts** — a quick authentic selfie with a live countdown.
- 👯 **Twins** — match, and a secure temporary chat opens until you vanish.

---

## SECTION 5 — WHAT TO TEST (checklist)

**Insert → Text box**, Heading 2 + checklist:

### Your mission, should you choose to accept it

- [ ] Choose a mode (Man or Woman) — note: this is permanent & private
- [ ] Run the radar in a real place (café, bar, event)
- [ ] Send at least one 60-second selfie Flirt
- [ ] Receive a Flirt and let the timer run out — does it really vanish?
- [ ] Twin up with someone and send a chat
- [ ] Hit **Delete Profile** — confirm it wipes everywhere
- [ ] Come back 24h later and confirm the trace is gone

---

## SECTION 6 — THE GROUP (embedded CTA, see snippet at top)

Use the **Embed code** snippet from the top of this file.
(Inline iframe of the group will be blank due to SAMEORIGIN — the
styled CTA box linking out is the reliable version.)

---

## SECTION 7 — GIVE FEEDBACK

**Insert → Text box**, Heading 2 + text:

### Tell us what's broken (and what's magic)

Three ways, ranked fastest → slowest:

1. **In the group** — post a thread, we read everything. 💜
2. **Email** — `flirt-spot@googlegroups.com`
3. **In-app** — shake your phone on any screen to capture a report.

**Golden rule:** tell us what *felt* off, not just what crashed. The
vibe is the product.

---

## SECTION 8 — FOOTER / RULES

**Insert → Text box**, small text:

🔞 FlirtSpot is 18+ only. Be kind, be real, be consensual.
Profiles are anonymous by design — please keep others' privacy too.
Don't share screenshots of real people.

*FlirtSpot is in alpha. Things will break. That's the point.* ✨

---

## PUBLISH

Top-right **Publish** → use suggested path or set custom:
`flirtspot-alpha` → URL becomes `sites.google.com/view/flirtspot-alpha`.

Done. Link it from your main site's footer or the tester group's
welcome message.

---

## OPTIONAL: want the same hub on your own domain?

`testers.html` in this repo is a ready, branded standalone version that
*can* be deployed to `flirt.spot/testers` via Cloudflare (and, unlike
Google Sites, can proxy/stream the group server-side for true embedding
later). Say the word and I'll deploy it.
