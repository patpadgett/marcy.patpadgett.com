#!/usr/bin/env python3
"""Write .impeccable/design.json — the extensions the frontmatter cannot hold."""
import colorsys
import datetime
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def ramp(hexv, steps=8):
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    out = []
    for i in range(steps):
        l = 0.15 + (0.95 - 0.15) * (i / (steps - 1))
        s = ss * (1 - abs(l - 0.55) * 0.9)
        rr, gg, bb = colorsys.hls_to_rgb(hh, l, max(0.02, min(1, s)))
        out.append("#%02x%02x%02x" % (round(rr * 255), round(gg * 255), round(bb * 255)))
    return out


COLORS = {
    "void": ("The Void", "neutral", "#170a2b", "The starfield behind the slab."),
    "paper": ("Lilac Paper", "neutral", "#fbf6ff", "Ground of the membrane."),
    "ink": ("Ink", "neutral", "#2a2036", "Body text on paper."),
    "link-blue": ("Chrome Blue", "secondary", "#1a00b8", "Links, WordArt dark stop."),
    "lilac": ("Lilac Edge", "secondary", "#c9a2f5", "Bevel highlight, dotted rules."),
    "violet": ("Violet Ink", "primary", "#6b3fa0", "Table border and structural rule."),
    "violet-deep": ("Deep Violet", "primary", "#3a0d5e", "Headings and small text."),
    "magenta": ("Hot Magenta", "tertiary", "#ff5fb2", "The one shout: active nav, NEW!, poll."),
    "ring-navy": ("Ring Navy", "neutral", "#0b0b46", "Webring box ground."),
    "ring-yellow": ("Webring Yellow", "tertiary", "#ffe94d", "The ring box, and only the ring box."),
    "substrate-black": ("Substrate Black", "neutral", "#050505", "Everything under the glass."),
    "bone": ("Bone", "neutral", "#b8b0a0", "The machine's type colour."),
    "wet-red": ("Wet Red", "primary", "#c9502f", "Warning ink in the substrate."),
    "ember": ("Ember", "tertiary", "#ff5a00", "Burn particles only."),
}

components = [
    {
        "name": "Linkware Button",
        "kind": "button",
        "refersTo": "linkware-button",
        "description": "An 88x31 nav button from a 1999 linkware set; ten of them form the rail.",
        "html": "<button class=\"ds-lnk\">MY PIX</button>",
        "css": ".ds-lnk{width:88px;height:31px;cursor:pointer;font:bold 8.5px/1.15 Verdana,Geneva,sans-serif;letter-spacing:.02em;color:#241038;text-shadow:0 1px 0 rgba(255,255,255,.9);background:linear-gradient(180deg,#fff 0%,#ead9fb 44%,#d3b8f0 100%);border:1px solid #8f6cb8;border-top-color:#fff;border-left-color:#fff;box-shadow:inset 0 1px 0 #fff,inset 0 -1px 0 #a98bcb,0 1px 1px rgba(40,10,70,.25);border-radius:0}.ds-lnk:hover{filter:brightness(1.08) saturate(1.2)}.ds-lnk:focus-visible{outline:2px solid #ff3ab1;outline-offset:2px}.ds-lnk:active{box-shadow:inset 0 2px 3px rgba(60,20,100,.35)}",
    },
    {
        "name": "Webring Box",
        "kind": "custom",
        "refersTo": "ring-box",
        "description": "The 48-node ring the page belongs to. Yellow on navy; the densest widget on the page.",
        "html": "<div class=\"ds-ring\"><div class=\"ds-ring-h\">&#9733; THE SOFTEST HEARTS WEBRING &#9733;</div><div class=\"ds-ring-b\"><p>this site is<br><b>site 47</b><br>of 48</p><div class=\"ds-ring-l\"><button>&#9668; prev</button><button>random</button><button>next &#9658;</button></div></div></div>",
        "css": ".ds-ring{border:2px solid #ffe94d;background:#0b0b46;color:#ffe94d;text-align:center;box-shadow:0 0 0 1px #000,0 0 14px rgba(255,233,77,.18);border-radius:0}.ds-ring-h{font:bold 8px/1.25 Verdana,sans-serif;letter-spacing:.04em;background:#ffe94d;color:#0b0b46;padding:4px 3px}.ds-ring-b{padding:7px 6px 8px}.ds-ring-b p{margin:0 0 7px;font:8.5px/1.45 Verdana,sans-serif;color:#cfd0ff}.ds-ring-b b{color:#ffe94d;font-size:11px}.ds-ring-l{display:flex;gap:3px}.ds-ring-l button{flex:1;font:8px Verdana,sans-serif;padding:3px 1px;cursor:pointer;background:#241a5c;color:#ffe94d;border:1px solid #ffe94d;border-radius:0}.ds-ring-l button:hover{background:#ffe94d;color:#0b0b46}",
    },
    {
        "name": "Guestbook Entry",
        "kind": "card",
        "refersTo": "guestbook-entry",
        "description": "A signed entry; the left rule rotates colour every third entry. Burns to ash in place.",
        "html": "<div class=\"ds-ent\"><p class=\"ds-who\">jess :)</p><p class=\"ds-when\">march 14, 1999 &mdash; 4:52 pm</p><p class=\"ds-what\">MARCY YOUR PAGE IS SO COOL!!! teach me!!!</p></div>",
        "css": ".ds-ent{margin:0 0 10px;padding:9px 11px;background:#fff;border:1px solid #dcc6f2;border-left:4px solid #b98cf0;box-shadow:2px 2px 0 rgba(107,63,160,.12);border-radius:0}.ds-ent:nth-child(3n){border-left-color:#ff9ade}.ds-ent:nth-child(3n+2){border-left-color:#8fd0ff}.ds-who{font:bold 11px 'Comic Sans MS',cursive;color:#7a1e78;margin:0 0 2px}.ds-when{font:9px Verdana,sans-serif;color:#6b5078;margin:0 0 5px;letter-spacing:.03em}.ds-what{font:12.5px/1.5 'Times New Roman',serif;color:#3a2a48;margin:0}",
    },
    {
        "name": "Photo Print",
        "kind": "card",
        "description": "A scanned print on a white mat, caption in Comic Sans. Dissolves and re-develops into its truth line.",
        "html": "<figure class=\"ds-print\"><img src=\"assets/img/photo_team.jpg\" alt=\"\"><figcaption>me + the team!! i'm 4th from the left.</figcaption></figure>",
        "css": ".ds-print{margin:0;background:#fff;border:1px solid #8f6cb8;padding:4px 4px 0;box-shadow:2px 2px 0 rgba(107,63,160,.25);border-radius:0}.ds-print img{display:block;width:100%;height:auto}.ds-print figcaption{font:italic 10px/1.25 'Comic Sans MS',cursive;color:#5a3a78;padding:3px 2px 5px;text-align:center}",
    },
    {
        "name": "Odometer",
        "kind": "custom",
        "description": "Six 5x7 pixel digits on black; each dot is a 2px element. Counts down; flips to a date.",
        "html": "<div class=\"ds-odo\"><span class=\"ds-d\"></span><span class=\"ds-d\"></span><span class=\"ds-d\"></span></div>",
        "css": ".ds-odo{display:inline-flex;gap:2px;padding:4px 5px;background:#0a0a0a;border:2px inset #6a6a6a;box-shadow:0 0 10px rgba(80,255,140,.18);border-radius:0}.ds-d{position:relative;display:block;width:12px;height:16px}.ds-d::before{content:'';position:absolute;left:0;top:0;width:2px;height:2px;background:#7dff9a;box-shadow:2px 0 #7dff9a,4px 0 #7dff9a,6px 0 #7dff9a,8px 0 #7dff9a,0 2px #7dff9a,8px 2px #7dff9a,0 4px #7dff9a,8px 4px #7dff9a,0 6px #7dff9a,8px 6px #7dff9a,0 8px #7dff9a,8px 8px #7dff9a,0 10px #7dff9a,8px 10px #7dff9a,0 12px #7dff9a,2px 12px #7dff9a,4px 12px #7dff9a,6px 12px #7dff9a,8px 12px #7dff9a}",
    },
    {
        "name": "Fragment Card",
        "kind": "custom",
        "refersTo": "fragment-card",
        "description": "The machine's voice: a torn shard of black glass with bone serif type.",
        "html": "<div class=\"ds-frag-wrap\"><div class=\"ds-frag\"><div class=\"ds-frag-in\"><p class=\"ds-fk\">FRAGMENT 01 / 07 &nbsp; INTERCEPTED</p><p class=\"ds-ft\">i am writing this from a place where your name is a file.</p><p class=\"ds-fh\">GUESTBOOK / ENTRY 07 &nbsp; 1 OF 7 RECEIVED</p></div></div></div>",
        "css": ".ds-frag-wrap{filter:drop-shadow(0 32px 70px rgba(0,0,0,.85))}.ds-frag{width:min(560px,84vw);padding:2px;background:#c9c0ac;-webkit-mask-image:url(assets/img/torn.png);mask-image:url(assets/img/torn.png);-webkit-mask-size:100% 100%;mask-size:100% 100%;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}.ds-frag-in{background:#08070a;padding:24px 26px 20px;box-shadow:inset 0 0 60px rgba(120,100,70,.06)}.ds-fk{font:9px/1 'Courier New',monospace;letter-spacing:.28em;color:#8d8474;margin:0 0 14px}.ds-ft{font:15px/1.62 'Times New Roman',serif;color:#ddd6c6;margin:0}.ds-fh{margin:18px 0 0;font:8.5px/1 'Courier New',monospace;letter-spacing:.24em;color:#5f584b}",
    },
    {
        "name": "Badge (88x31)",
        "kind": "custom",
        "description": "A 'BEST VIEWED WITH' badge. 6.4px type, hard border, gradient fill. Clicking one destroys it.",
        "html": "<button class=\"ds-badge\">BEST VIEWED<br>IN NETSCAPE<br>NAVIGATOR 4.0</button>",
        "css": ".ds-badge{height:31px;width:88px;padding:2px 1px;cursor:pointer;text-align:center;font:bold 6.4px/1.25 Verdana,Geneva,sans-serif;letter-spacing:.02em;border:1px solid #000;color:#fff;text-shadow:1px 1px 0 #000;background:linear-gradient(#2b6fd6,#0a2a7a);border-radius:0}.ds-badge:hover{filter:brightness(1.25)}",
    },
]

data = {
    "schemaVersion": 2,
    "generatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
    "title": "Design System: Marcy's Little Corner of the Web",
    "extensions": {
        "colorMeta": {
            k: {"role": role, "displayName": name, "canonical": hexv,
                "tonalRamp": ramp(hexv), "purpose": purpose}
            for k, (name, role, hexv, purpose) in COLORS.items()
        },
        "typographyMeta": {
            "display": {"displayName": "WordArt Chrome", "purpose": "Banner only, two stacked lines."},
            "heading": {"displayName": "Comic Sans Heading", "purpose": "Section titles."},
            "body": {"displayName": "Times Body", "purpose": "All reading copy."},
            "ui": {"displayName": "Verdana UI", "purpose": "Controls, names, poll questions."},
            "label": {"displayName": "Verdana Micro", "purpose": "Badges, captions, rail lists."},
            "machine": {"displayName": "Courier Machine", "purpose": "HUD, log, fragment kickers, substrate voice."},
        },
        "shadows": [
            {"name": "bevel", "value": "inset 0 1px 0 #fff, inset 0 -1px 0 #a98bcb, 0 1px 1px rgba(40,10,70,.25)", "purpose": "Every control on the membrane, at rest."},
            {"name": "hard-offset", "value": "2px 2px 0 rgba(107,63,160,.25)", "purpose": "Prints, guestbook entries, award cards."},
            {"name": "slab-float", "value": "0 18px 60px rgba(0,0,0,.75), 0 0 90px rgba(120,60,190,.18)", "purpose": "The page slab, nothing else."},
            {"name": "panel-bevel", "value": "inset 1px 1px 0 #fff, inset -1px -1px 0 rgba(150,118,186,.55), 2px 2px 0 rgba(107,63,160,.20)", "purpose": "Every content panel; without it a panel is a modern box in period clothes."},
            {"name": "glass-glow", "value": "0 0 6px rgba(255,255,255,.9)", "purpose": "Fracture sparks and shard edges."},
        ],
        "motion": [
            {"name": "crack-draw", "value": "110-300ms ease-out, stroke-dashoffset to 0", "purpose": "Fracture lines drawing from the impact point."},
            {"name": "shard-fall", "value": "700-1500ms cubic-bezier(.55,0,.9,.6)", "purpose": "Glass shards leaving the page, with gravity."},
            {"name": "frag-in", "value": "460ms outExpo", "purpose": "Fragment card arriving."},
            {"name": "peel", "value": "300ms out + 340ms in, jagged clip", "purpose": "Webring node change."},
            {"name": "melt", "value": "1100ms inQuad, 26ms per-letter stagger", "purpose": "Text dissolving into drips."},
            {"name": "burn", "value": "900-1100ms radial mask expansion", "purpose": "An entry burning away to ash."},
        ],
        "breakpoints": [
            {"name": "rail-collapse", "value": "820px"},
            {"name": "side-stack", "value": "560px"},
            {"name": "banner-shrink", "value": "420px"},
        ],
    },
    "components": components,
    "narrative": {
        "northStar": "A Lit Page in a Dark Room",
        "overview": "The system is two substances wearing one material. The surface is a 780px slab of lilac paper floating in a purple-black starfield, with every period artifact a 1999 teenager could type. Underneath it is a black lacquer of ribbed bone and brushed steel with one warm light in it. The only material the two worlds share is glass.",
        "keyCharacteristics": [
            "Two grounds, one seam: paper #fbf6ff in #170a2b, and #050505 bone under both.",
            "Bevel logic from the Windows 95 widget set; never a modern shadow on the membrane.",
            "Microtype proportional to 1999: 8.5-10px Verdana for UI, 13px Times for body.",
            "Zero border radius anywhere.",
            "Every motion is violent, brief, and caused by the visitor.",
        ],
        "rules": [
            {"name": "The Two Grounds Rule", "body": "A surface is either paper or substrate. Nothing is half-toned between them; the glass is the only place they meet.", "section": "colors"},
            {"name": "The One Shout Rule", "body": "Magenta appears once per screenful. If a second magenta element is needed, the first one was wrong.", "section": "colors"},
            {"name": "The Four Faces Rule", "body": "Times, Comic Sans, Verdana, Courier. No fifth face, no hosted font, no variable axis.", "section": "typography"},
            {"name": "The 8px Floor Rule", "body": "Machine voice never sets above 9px and never below 7px.", "section": "typography"},
            {"name": "The Bevel-Or-Nothing Rule", "body": "On the membrane, a shadow is either a 1px bevel or a 2px hard offset. Blurred shadows belong to the slab and the substrate.", "section": "elevation"},
        ],
        "dos": [
            "Do keep reading copy at 13px Times or larger; microtype is for labels and badges only.",
            "Do let the substrate be genuinely dark, with one warm light source and no neon.",
            "Do make every destructive effect a consequence of a click, and let something remain.",
            "Do give every control a 2px magenta focus ring at 2px offset.",
            "Do hold flash rates under 3 Hz and honour prefers-reduced-motion.",
        ],
        "donts": [
            "Don't round a corner on the membrane.",
            "Don't use a blurred shadow on a control.",
            "Don't add a fifth typeface or a hosted font.",
            "Don't let magenta appear twice in one screenful.",
            "Don't decorate with the substrate; it appears only through damage, the finale, and the fragment cards.",
        ],
    },
}

with open(os.path.join(ROOT, ".impeccable", "design.json"), "w") as f:
    json.dump(data, f, indent=2)
print("wrote .impeccable/design.json", len(json.dumps(data)) // 1024, "KB")
