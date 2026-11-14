"""Generates the retro green-phosphor SVG panels for the GitHub profile README."""
import os, textwrap, pyfiglet
from xml.sax.saxutils import escape as esc

OUT = "profile/assets"
os.makedirs(OUT, exist_ok=True)

W = 900            # viewBox width
PAD = 34           # left padding
FS = 14.5          # font size
CW = FS * 0.6      # monospace char width
LH = 23            # line height
BAR = 38           # title bar height
WRAP = int((W - 2 * PAD) / CW) - 2

BG, PANEL = "#030703", "#061006"
BRIGHT, MAIN, DIM, DEEP = "#39ff14", "#1fe03a", "#14873a", "#0b3d1a"
FONT = "'Courier New','DejaVu Sans Mono','Liberation Mono',Consolas,monospace"


def defs(extra_css=""):
    return f"""<defs>
  <filter id="glow" x="-5%" y="-5%" width="110%" height="110%">
    <feGaussianBlur stdDeviation="1.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1.6" fill="#000" opacity=".35"/>
  </pattern>
  <radialGradient id="vig" cx="50%" cy="50%" r="75%">
    <stop offset="60%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity=".7"/>
  </radialGradient>
  <radialGradient id="tint" cx="50%" cy="40%" r="70%">
    <stop offset="0%" stop-color="{BRIGHT}" stop-opacity=".07"/>
    <stop offset="100%" stop-color="{BRIGHT}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{BRIGHT}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{BRIGHT}" stop-opacity=".09"/>
    <stop offset="100%" stop-color="{BRIGHT}" stop-opacity="0"/>
  </linearGradient>
</defs>
<style>
  text{{font-family:{FONT};font-size:{FS}px;white-space:pre}}
  .b{{fill:{BRIGHT};font-weight:bold}} .m{{fill:{MAIN}}} .d{{fill:{DIM}}}
  .p{{fill:{BRIGHT}}} .t{{fill:{DIM};font-size:13px}}
  .crt{{animation:flick 6s infinite}}
  @keyframes flick{{0%,100%{{opacity:1}}47%{{opacity:1}}48%{{opacity:.93}}49%{{opacity:1}}82%{{opacity:.97}}}}
  .cur{{animation:blink 1.06s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  .beam{{animation:roll 7s linear infinite}}
  @keyframes roll{{from{{transform:translateY(-120px)}}to{{transform:translateY(var(--h))}}}}
  {extra_css}
</style>"""


def frame(h, title, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img">
{defs()}
<rect width="{W}" height="{h}" rx="14" fill="{BG}"/>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="13" fill="{PANEL}" stroke="{BRIGHT}" stroke-opacity=".35"/>
<rect x="1" y="1" width="{W-2}" height="{BAR}" rx="13" fill="#0a1a0a"/>
<rect x="1" y="{BAR-12}" width="{W-2}" height="12" fill="#0a1a0a"/>
<line x1="1" y1="{BAR}" x2="{W-1}" y2="{BAR}" stroke="{BRIGHT}" stroke-opacity=".25"/>
<circle cx="24" cy="{BAR/2}" r="5.5" fill="{BRIGHT}"/><circle cx="44" cy="{BAR/2}" r="5.5" fill="{MAIN}" opacity=".6"/><circle cx="64" cy="{BAR/2}" r="5.5" fill="{DIM}" opacity=".6"/>
<text x="{W/2}" y="{BAR/2+4.5}" text-anchor="middle" class="t">{esc(title)}</text>
<g class="crt" filter="url(#glow)">
{body}
</g>
<rect y="{BAR}" width="{W}" height="{h-BAR}" fill="url(#tint)"/>
<rect class="beam" style="--h:{h}px" width="{W}" height="120" fill="url(#beam)"/>
<rect width="{W}" height="{h}" rx="14" fill="url(#scan)"/>
<rect width="{W}" height="{h}" rx="14" fill="url(#vig)"/>
</svg>"""


def wrap(text, indent=0):
    return textwrap.wrap(text, WRAP - indent) or [""]


def render(lines, y0):
    """lines: list of (cls, text, indent_chars). Returns svg body and next y."""
    out, y = [], y0
    for cls, txt, ind in lines:
        if cls == "cells":
            for cx, ccls, ctxt in txt:
                out.append(f'<text x="{PAD + cx:.1f}" y="{y}" class="{ccls}">{esc(ctxt)}</text>')
        elif cls == "grid":
            out.append(txt(y))
        elif cls != "gap":
            out.append(f'<text x="{PAD + ind*CW:.1f}" y="{y}" class="{cls}">{esc(txt)}</text>')
        y += 0 if cls == "grid" else (LH if cls != "gap" else LH // 2)
    return "\n".join(out), y


def card(name, title, cmd, lines, alt):
    y = BAR + 34
    head = [("p", f"bassam@uqu:~$ {cmd}", 0), ("gap", "", 0)]
    body, y = render(head + lines, y)
    y += 4
    body += f'\n<text x="{PAD}" y="{y}" class="p">bassam@uqu:~$</text>'
    body += f'\n<rect class="cur" x="{PAD + 14*CW:.1f}" y="{y-13}" width="{CW:.1f}" height="16" fill="{BRIGHT}"/>'
    h = y + 26
    svg = frame(h, title, body).replace('role="img">', f'role="img"><title>{esc(alt)}</title>', 1)
    open(f"{OUT}/{name}.svg", "w").write(svg)


def item(tag, head, desc):
    L = [("b", f"{tag} {head}", 0)]
    L += [("m", s, 4) for s in wrap(desc, 4)]
    L.append(("gap", "", 0))
    return L



# ================================================================ HERO (typed)
def hero():
    art = pyfiglet.figlet_format("MR-MAXVX", font="ansi_shadow", width=200).rstrip("\n").split("\n")
    art = [a for a in art if a.strip()]
    afs, alh = 15, 15.5
    ax = (W - max(map(len, art)) * afs * 0.6) / 2
    y = BAR + 42
    parts = [f'<text x="{ax:.1f}" y="{y + i*alh:.1f}" class="b art">{esc(r)}</text>' for i, r in enumerate(art)]
    y += len(art) * alh + 36
    # academic / research-paper name format (IEEE style: initials + family name)
    parts.append(f'<text x="{W/2}" y="{y:.1f}" text-anchor="middle" class="b" style="font-size:28px;letter-spacing:6px">B. M. AL-DOSSARY</text>')
    y += 28
    parts.append(f'<text x="{W/2}" y="{y:.1f}" text-anchor="middle" class="m" style="font-size:15px;letter-spacing:4px">a.k.a. MAX</text>')
    y += 26
    for row in ["Systems Builder  •  Programming Language Enthusiast  •  Cybersecurity Obsessor",
                "Network Nerd  •  Cryptography Enjoyer"]:
        parts.append(f'<text x="{W/2}" y="{y:.1f}" text-anchor="middle" class="d" style="font-size:14px;fill:{MAIN};opacity:.85">{esc(row)}</text>')
        y += 21
    y += 26

    typed = [
        ("p", "bassam@uqu:~$ whoami"),
        ("m", "> Computer Science @ Umm Al-Qura University"),
        ("m", "> Expected graduation: 17 May 2028"),
        ("p", "bassam@uqu:~$ echo $MISSION"),
        ("b", '> "Bridging academia and engineering: where theory meets practice."'),
        ("p", "bassam@uqu:~$ uptime --status"),
        ("d", "> [ONLINE]  currently mastering: C++ / Rust"),
    ]
    t, clips = 0.9, []
    for i, (cls, txt) in enumerate(typed):
        n = len(txt)
        dur = max(n * (0.05 if cls == "p" else 0.028), 0.3)
        vals = ";".join(f"{k*CW:.1f}" for k in range(n + 1))
        clips.append(f'<clipPath id="c{i}"><rect x="{PAD-2}" y="{y-16}" height="{LH}" width="0">'
                     f'<animate attributeName="width" values="{vals}" calcMode="discrete" dur="{dur:.2f}s" begin="{t:.2f}s" fill="freeze"/></rect></clipPath>')
        parts.append(f'<text x="{PAD}" y="{y}" class="{cls}" clip-path="url(#c{i})">{esc(txt)}</text>')
        t += dur + (0.45 if cls == "p" else 0.15)
        y += LH + (8 if i in (2, 4) else 0)
    y += 6
    parts.append(f'<text x="{PAD}" y="{y}" class="p" opacity="0">bassam@uqu:~$<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>')
    parts.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                 f'<rect class="cur" x="{PAD + 14*CW:.1f}" y="{y-13}" width="{CW:.1f}" height="16" fill="{BRIGHT}"/></g>')
    h = int(y + 30)
    body = "<defs>" + "".join(clips) + "</defs>\n" + "\n".join(parts)
    svg = frame(h, "Mr-MaxVX@github: ~ — tty1 — 80x24", body)
    svg = svg.replace("</style>", f".art{{font-size:{afs}px}}</style>")
    svg = svg.replace('role="img">', 'role="img"><title>Mr-MaxVX: B. M. Al-Dossary (Bassam Mohammed Al-Dossary), a.k.a. MAX. '
                      'Systems builder, programming language enthusiast, cybersecurity obsessor, network nerd, cryptography enjoyer. '
                      'Computer Science at Umm Al-Qura University, expected graduation 17 May 2028.</title>', 1)
    open(f"{OUT}/hero.svg", "w").write(svg)


hero()

T = lambda s, ind=0, c="m": (c, s, ind)

# ================================================================ LANGUAGES / STACK
card("stack", "~/stack — tree", "tree ~/languages ~/tools", [
    T("~/languages", 0, "b"),
    T("├── fluent_in/"),
    T("│   ├── Java (JavaFX)     ├── Python        ├── C"),
    T("│   ├── MIPS Assembly     ├── SQL (MySQL)   ├── JavaScript"),
    T("│   └── HTML / CSS"),
    T("├── currently_mastering/"),
    T("│   ├── C++               [■■■■■■□□□□]  compiling..."),
    T("│   └── Rust              [■■■■□□□□□□]  fighting the borrow checker"),
    T("└── human_languages/"),
    T("    └── Arabic (native)  ·  English (fluent)  ·  Russian (learning)"),
    ("gap", "", 0),
    T("~/tools", 0, "b"),
    T("├── security_and_networking/  Wireshark · Nmap · Cisco Packet Tracer"),
    T("└── environments/             Linux · MySQL · Git & GitHub"),
], "Languages: Java (JavaFX), Python, C, MIPS Assembly, SQL (MySQL), JavaScript, HTML/CSS; currently mastering C++ and Rust. "
   "Spoken: Arabic (native), English (fluent), Russian (learning). Tools: Wireshark, Nmap, Cisco Packet Tracer, Linux, MySQL, Git and GitHub.")

# ================================================================ WHY (what I love)
card("why", "~/why — less", "cat why_i_love_this.md",
     item("[01]", "WHY CRYPTOGRAPHY?",
          "I'm genuinely passionate about encryption because I love solving puzzles. Every time I crack one, "
          "I feel my brain getting faster at recognizing patterns, and cryptography is the ultimate puzzle.")
     + item("[02]", "WHY BLOCKCHAIN?",
            "Because it's a hard problem that really matters to people. Its decentralization gives it a strange, "
            "almost paradoxical kind of trust: no central authority, yet records you can rely on as immutable truth.")
     + item("[03]", "WHY SECURITY?",
            "Security is where everything meets. It fuses decentralization, cryptography, and networks, and almost "
            "every technology depends on it. To me, security is the hybrid of all technologies working together.")
     + item("[04]", "WHY NETWORKS?",
            "Networks are the foundation of everything, the backbone of the internet itself. If you understand "
            "how packets move, you understand how the modern world talks.")
     + item("[05]", "WHY BUILD & LEAD?",
            "I've loved being the project manager and team lead since my early university days. I enjoy running teams "
            "in a coordinated, organized way, and I've led 90% of my university projects to full marks. "
            "Leadership isn't a role I take, it's who I am.")[:-1],
     "Why I love this: cryptography because I love solving puzzles and recognizing patterns; blockchain because it's a hard, "
     "important problem and decentralization creates trust; security because it fuses decentralization, cryptography and networks; "
     "networks because they're the foundation of the internet; build and lead because I'm a natural team leader (90% of university projects led to full marks).")

# ================================================================ BUILDS
BUILDS = [
    ("GHOST ASCENT", "C++ / OpenGL", "Custom 2D/3D graphics pipeline & game build."),
    ("ALBIONSELLER", "Hybrid", "Market tracking & trading utility tool."),
    ("JAVAJAM COFFEE", "Java / Native", "Full-featured desktop application build."),
]
bl = []
for i, (n, st, d) in enumerate(BUILDS, 1):
    bl.append(("cells", [(0, "b", f"[0{i}] {n}"), (CW*28, "d", f"<{st}>")], 0))
    bl += [("m", l, 5) for l in wrap(d, 5)]
    bl.append(("gap", "", 0))
card("builds", "~/builds — ls -l", "ls -l ~/builds",
     bl + [T("3 builds shipped · more in the repos below", 0, "d")],
     "Featured builds: Ghost Ascent (C++ / OpenGL), a custom 2D/3D graphics pipeline and game build; AlbionSeller (hybrid), "
     "a market tracking and trading utility tool; JavaJam Coffee (Java / native), a full-featured desktop application build.")

# ================================================================ GUARDIAN: pixel-art skeleton knight
KNIGHT = """\
....W...........................
...SBS..........................
...SBS.........DDDDDDD..........
...SBS.......DDMMMMMMMDD........
...SBS......DMMMMMMMMMMMD.......
...SBS......DMBBBBBBBBBMD.......
...SBS......DBBBBBBBBBBBD.......
...SBS......DBEEEBBBEEEBD.......
...SBS......DBEEEBBBEEEBD.......
...SBS......DBBBBB.BBBBBD.......
...SBS.......DBBB...BBBD........
...SBS.......DBBBBBBBBBD........
...SBS........DB.B.B.BD.........
...SBS.........DBBBBBD..........
...SBS...........BBB............
..HHHHH..DDDDMMMMMMMDDDD........
...HMH..DMMMDDBBBBBDDMMMD.......
..BBBBBDMMMD..B...B..DMMMD......
..BBBBDMMMD.BBBBBBBBB.DMMMD.....
...BBDDDD....B..B..B...DDDBB....
.............BBBBBBBBB.....BB...
.............B..B..B.......BBB..
..............BBBBBBB.......BB..
............DDDDDDDDDDD.........
............DMMEMMMEMMD.........
............DDDDDDDDDDD.........
..............BB...BB...........
..............BB...BB...........
.............DBBD.DBBD..........
..............BB...BB...........
..............BB...BB...........
............DDDDD.DDDDD.........""".split("\n")


def guardian():
    px, ox = 8, PAD + 10
    oy = BAR + 32
    col = {"B": BRIGHT, "M": MAIN, "D": DIM, "S": "#8dff7a", "H": MAIN, "W": "#d9ffd0", "E": "#000"}
    rects, eyes = [], []
    for r, row in enumerate(KNIGHT):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            x, y = ox + c * px, oy + r * px
            rects.append(f'<rect x="{x}" y="{y}" width="{px}" height="{px}" fill="{col[ch]}"/>')
            if ch == "E":
                eyes.append(f'<rect class="eye" x="{x+2}" y="{y+2}" width="{px-4}" height="{px-4}" fill="#eaffea"/>')
    blade_x = ox + 4 * px
    shine = (f'<rect class="shine" x="{blade_x+1}" y="{oy}" width="{px-2}" height="{px*3}" fill="#ffffff" opacity=".0"/>')
    art_h = len(KNIGHT) * px
    tx = ox + 34 * px + 10
    info = [
        ("p", "bassam@uqu:~$ ./summon_guardian.sh"),
        ("d", "> summoning... done."),
        ("gap", ""),
        ("b", "THE GUARDIAN OF Mr-MaxVX"),
        ("m", "class ..... Skeleton Knight"),
        ("m", "weapon .... Blade of Pattern Recognition"),
        ("m", "armor ..... Cipher-forged plate (AES-256)"),
        ("m", "guards .... every repo on this profile"),
        ("m", "alignment . Lawful Green"),
        ("gap", ""),
        ("m", "HP  [■■■■■■■■■■] 100%"),
        ("m", "XP  [■■■■■■■□□□]  lvl 2028"),
        ("gap", ""),
        ("d", "> status: on watch 24/7. no intruders shall pass."),
    ]
    out, y = [], oy + 18
    for cls, s in info:
        if cls != "gap":
            out.append(f'<text x="{tx}" y="{y}" class="{cls}">{esc(s)}</text>')
        y += LH if cls != "gap" else LH // 2
    out.append(f'<rect class="cur" x="{tx + 31*CW:.1f}" y="{oy + 18 + 0 - 13}" width="0" height="0"/>')
    h = max(oy + art_h, y) + 30
    ground = f'<line x1="{ox-6}" x2="{ox + 30*px}" y1="{oy+art_h+4}" y2="{oy+art_h+4}" stroke="{DIM}" stroke-width="2" stroke-dasharray="4 4"/>'
    body = (f'<g class="bob">{"".join(rects)}{"".join(eyes)}{shine}</g>{ground}' + "\n".join(out))
    css = (".bob{animation:bob 1.6s steps(2) infinite}@keyframes bob{50%{transform:translateY(2px)}}"
           ".eye{animation:glow 2.4s ease-in-out infinite}@keyframes glow{0%,100%{opacity:.25}50%{opacity:1}}"
           f".shine{{animation:sh 3s linear infinite}}@keyframes sh{{0%{{opacity:0;transform:translateY({px*14}px)}}"
           f"10%{{opacity:.8}}40%{{opacity:.8;transform:translateY(0)}}45%,100%{{opacity:0;transform:translateY(0)}}}}")
    svg = frame(h, "~/guardian — ./summon_guardian.sh", body).replace("</style>", css + "</style>")
    svg = svg.replace('role="img">', '<title>Pixel-art green skeleton knight with a sword, the guardian of Mr-MaxVX profile.</title>'.join(['role="img">', '']), 1)
    open(f"{OUT}/guardian.svg", "w").write(svg)


guardian()

card("activity", "~/activity — htop", "git log --author=Mr-MaxVX --stats", [
    T("> streaming live commit telemetry from github.com/Mr-MaxVX ...", 0, "d"),
], "GitHub activity")

# ================================================================ divider + footer
div = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 24" width="{W}" height="24">
<style>.s{{animation:mv 4s linear infinite}}@keyframes mv{{from{{transform:translateX(-200px)}}to{{transform:translateX({W}px)}}}}</style>
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{BRIGHT}" stop-opacity="0"/><stop offset=".5" stop-color="{BRIGHT}"/><stop offset="1" stop-color="{BRIGHT}" stop-opacity="0"/></linearGradient></defs>
<line x1="0" y1="12" x2="{W}" y2="12" stroke="{DEEP}" stroke-width="2" stroke-dasharray="6 6"/>
<rect class="s" y="11" width="200" height="2" fill="url(#g)"/>
</svg>"""
open(f"{OUT}/divider.svg", "w").write(div)

foot_body = (f'<text x="{W/2}" y="{BAR+38}" text-anchor="middle" class="b">&gt; Always building • Open to collaborating on systems, security &amp; decentralized tools.</text>'
             f'<text x="{W/2}" y="{BAR+64}" text-anchor="middle" class="d">[ thanks for stopping by • connection kept alive ]</text>')
open(f"{OUT}/footer.svg", "w").write(frame(BAR + 88, "EOF", foot_body))
print("ok")
