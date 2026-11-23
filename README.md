# Marcy's Little Corner of the Web

An interactive horror artifact: a 1999 Angelfire homepage that comes apart as you
learn who built it, plus a separate reconstruction by someone who does not believe it.

Static files, no build step. Open `index.html` or serve the folder:

```
python3 -m http.server 8814
```

- `index.html` — the homepage. A real-looking 1999 personal page: tiled background,
  centered table, WordArt, marquee, guestbook, hit counters, webring, badges, animated
  GIFs. Nothing on it breaks when you click. Instead, it changes as you find things.
- `reconstruction.html` — the archivist's reading: five exposures, full-bleed, in which
  the record does not agree with itself.

---

## 1. The homepage (`index.html`)

Marcy Vale, sixteen, Northvale. Volleyball, piano, friends, family, a dog, a webring
of forty-eight pages. Seven threads run through the page. Each one is an ordinary
1999 interaction; each one also gives up a fragment of the truth.

| Thread | What happens |
|---|---|
| Guestbook | you sign it; a 2027 entry appears underneath from someone who shouldn't be there |
| My Pix | six low-res scanned photos are printed in the page; a text link asks what happened to the fourth one |
| The Quiz | the answers are wrong no matter what you pick |
| Counter | 001999 → 020471 — it counts forward into a year that hasn't happened |
| Webring | node 47 → 48 → 49; node 49 is not a page |
| Badges | Netscape and Internet Explorer, both long dead |
| The page itself | the marquee keeps saying "I am not a robot" until it doesn't |

### The new mechanic: slow discovery, not destruction

There is no click-to-destroy. Clicking never damages the page. Learning does.

`js/decay.js` holds six stages. Every fragment collected moves the page one step
further through them:

| Stage | Class | What the visitor sees |
|---|---|---|
| 0 | `decay-0` | the intact 1999 page |
| 1 | `decay-1` | text rewrites in place, the title bar says *(edited)* |
| 2 | `decay-2` | star tile darkens to pastel marble, the two animated GIFs freeze, the ghost guestbook entry appears |
| 3 | `decay-3` | colour drains toward default blue-on-white, the restore link appears |
| 4 | `decay-4` | the stylesheet comes apart: tables unstyle, Times New Roman returns, marquee stops |
| 5 | `decay-5` | the confession holds for 25 seconds, then the Legion control panel takes over |

At stage four a password hint starts to spell itself out, one letter at a time; at
stage five the full word appears and the page can be restored to its first state.

The rewrites live in `js/texts.js`, keyed by element id and stage. `decay.textAt(key, level)`
clamps past the end of a key's list, so a short key simply holds its last value.

### The finale: LEGION (3 minutes 16 seconds)

Stage 5 opens on the white confession page and **holds for 25 seconds** so it can be read.
At 15 seconds a centred `T-minus` countdown appears over it. Whispering plays underneath;
at three seconds left the supplied `3secondstolive.mp3` plays, followed by `screamsofhorror.mp3`. Then the
screen cuts to the Legion control panel.

- **22 hard cuts, seven seconds apart** — long enough to read each feed. Four feeds rotate:
  `tty0 // ingress`, `oracle // financial suite`, `switch // cellular`, `satcom // media`.
- Every cut types new lines, fires a glitch bar, a camera punch and a short glitch sound.
  Scanlines, a refresh sweep, a slowly drifting node map and a 30-second ticker run underneath.
- Eight objectives check off through the run. A **spinning orthographic globe** turns from
  green to red as they complete: biggest population centres first, smallest last. At 100%
  the whole globe, grid included, is red.
- Clickable: feed tabs (jump to a feed), `[ auto: on/off ]`, `[ audio: on/off ]`, and each
  objective row (expands its detail line).
- A low distorted voice delivers four lines: "in 1999 we hijacked Marcy's homepage / we
  made the world believe that she exists / she does exist / she is us". Captions always show.
- White noise, a high beep, a low thump, then `reconstruction.html`.

All terminal content is invented set dressing — no real hosts, commands, account numbers or
working exploit details. A `[ skip transmission ]` link is always present, and
`prefers-reduced-motion` removes the flicker, drift and animated noise while keeping the
content, objectives and captions. `index.html?co=fast` compresses the whole film to about
two seconds for verification only.

### Files

```
index.html               the period homepage (inline attributes, centered tables)
css/membrane.css         base voice + the six decay stages + phone layout
css/collective.css       the Legion finale: scanlines, glitch cuts, camera, node map
js/texts.js              the stage-by-stage rewrite map (nine keys)
js/decay.js              M.decay: record(), render(), reset(), stage mutations
js/threads.js            M.threads: the seven interactions
js/app.js                restore wiring, counter init, first render
js/collective-data.js    invented terminal feeds, objectives, ticker and voice lines
js/collective.js         M.collective: the 3:16 film, countdown, audio, static, handoff
js/collective-globe.js   spinning orthographic globe, green to red by population
assets/audio/            3secondstolive.mp3 and screamsofhorror.mp3
assets/img/              GIFs, badges, WordArt banner, thumbnails, counter, tiled grounds
assets/vendor/           anime.js and motion.js (still shipped, no longer driving the page)
```

The old burn world — `js/burn.js`, `js/destroy.js`, `js/audio.js`, `js/data.js`,
`css/room.css` — has been removed from the shipping tree and is kept in
`.impeccable/backup/` for reference.

---

## 2. The reconstruction (`reconstruction.html`)

A different world for the same fiction. Five exposures, full-bleed, in which the record
fails to agree with itself: misregistration, halation, a halftone screen, a light leak,
and finally one physical object — the team photo she is not in.

```
reconstruction.html          five exposures and a coda
css/recon.css                black editorial world, Libre Caslon + Fragment Mono
js/recon.js                  the film gate: plate switching, scroll fade, timecode
tools/build_recon.py         every plate: grade, halation, misregister, halftone, dropout
assets/recon/                plate1–5, print
```

---

## Tools

```
tools/builder99.py         tiles, WordArt, 88x31 badges, animated GIFs, favicon
tools/make_photos.py       the six 320x240 scanned-looking album photos (from .impeccable/raw/)
tools/make_counter.py      the LED hit-counter GIF
tools/make_email.py        the @ envelope GIF
tools/make_divider.py      the diamond divider GIF
tools/build_recon.py       the reconstruction plates
tools/provenance*.py       asset provenance
tools/playthrough.js       legacy harness from the burn build
```

`.impeccable/backup/` holds earlier versions of every replaced file, including the
whole burn/glass world (`index.v1.html`, `glass.v1.js`, `membrane.v1.css`,
`substrate.css`, `aperture.js`, `DESIGN.v2.md`, `README.v2.md`).

## Verified

- 7 real interactions → stage 5, no console errors
- restore returns to stage 0 with the original tile and title
- no 404s on either page
- no horizontal overflow at 320 / 375 / 390 / 768 / landscape 844×390 / 1024 / 1280
- 44px touch targets on coarse pointers; real synthesized taps advance the story
- touch swipe scrolls the page without triggering a control
- stage 5 plain text stays within a phone viewport
- `file://` and localhost both work
