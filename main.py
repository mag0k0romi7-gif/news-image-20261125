#!/usr/bin/env python3
"""news-image-20261125: draw one 1024x1024 PNG summing up the world news of
Wednesday, 25 November 2026. Deterministic: no network, no timestamps, no
randomness. Run: python3 main.py  (writes entry.png next to this file, or to
$MAKEFUN_OUTPUT_DIR when set)."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (90, 86, 78)
RULE = (180, 172, 156)
RED = (139, 26, 26)
DARK = (24, 32, 48)
WHITE = (255, 255, 255)

FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

DATE_LINE = "Wednesday, 25 November 2026"
MASTHEAD = "THE WORLD IN ONE PAGE"
SUBHEAD = "46 STORIES  \u2022  9 REGIONS  \u2022  ONE DAY"

TOP = (
    "Houthis strike Saudi oil refinery and Riyadh tower",
    "Second attack on the capital's financial district in a week wounds 11; "
    "the Saudi-led coalition hits Hodeidah port in reply.",
)

# (region title, accent colour, [(headline, one-line summary), ...])
REGIONS = [
    ("NORTH AMERICA", (31, 68, 120), [
        ("Trump awards Giuliani the Medal of Freedom",
         "Ex-New York mayor honoured with the top US civilian award."),
        ("Huawei guilty of stealing US trade secrets",
         "NY jury convicts after eight years; racketeering dropped."),
        ("US soldier admits selling secrets to China",
         "Sergeant photographed restricted files, offered hard drives."),
        ("Abrego Garcia leaves US for Spain a free man",
         "Deportation symbol exits voluntarily after a negotiated deal."),
        ("Democrats win biggest House majority since 1990",
         "At least 259 seats: power to block Trump and probe."),
    ]),
    ("LATIN AMERICA", (122, 62, 24), [
        ("All hostages freed in Cartagena supermarket siege",
         "Forces storm store after failed raid; one gunman killed."),
        ("Car bomb wounds 20+ in Colombian city",
         "Blast tears through Villavicencio; governor's office also hit."),
        ("Argentina slides into technical recession",
         "Activity fell 1.2% in Q3, first contraction run since 2024."),
        ("Panama may reopen Cobre Panama copper mine",
         "Mine shut by court in 2023 could restart temporarily."),
        ("WHO chief visits Cuba amid health crisis",
         "Tedros pledges $2m for vaccines amid fuel blockade."),
    ]),
    ("EUROPE", (43, 92, 66), [
        ("Spain's election race turns on housing",
         "Sanchez and Feijoo clash in debate before Sunday vote."),
        ("Arrests after break-in at Prince William's home",
         "Two men held over burglary at the Norfolk estate."),
        ("Met Police still institutionally racist, report finds",
         "London's force faulted again in a fresh review."),
        ("Russian strikes kill 15 in Kyiv region",
         "Overnight attacks hit homes as winter closes in."),
        ("Hungary's PM visits Kyiv, opens 'new chapter'",
         "Peter Magyar meets Zelensky after years of tension."),
    ]),
    ("MIDDLE EAST", (139, 26, 26), [
        ("Tankers hit by blasts near Strait of Hormuz",
         "Tehran reports explosions as Red Sea tensions spread."),
        ("Coalition strikes Hodeidah port in Yemen",
         "Saudi-led forces hit Houthi sites; Jeddah threatened in return."),
        ("Israeli strike kills Hamas security chief in Gaza",
         "Wife and teenage daughters also killed, reports say."),
        ("Jordan hands death sentence over officer killing",
         "State Security Court convicts man of terrorist acts."),
        ("Netanyahu presses Trump for new Iran strikes",
         "Israeli PM urges action; US president reported hesitant."),
    ]),
    ("AFRICA", (146, 104, 12), [
        ("Senegal regains CAN-2025 title from Morocco",
         "CAS returns the crown ten months after a chaotic final."),
        ("Ramaphosa wins Farmgate court case",
         "Court sets aside panel report that found possible violations."),
        ("Ebola fuels abuse of women and girls in Congo",
         "Outbreak has killed 5,800 since May, UNICEF says."),
        ("Landmine toll hits five-year high of 7,000",
         "Myanmar and Syria top the casualty list."),
        ("Sahel rebels take war to the skies with drones",
         "Cheap FPV drones erode armies' air edge in Mali and beyond."),
    ]),
    ("SOUTH ASIA", (96, 48, 120), [
        ("Pakistan's first astronaut heads to Chinese station",
         "Zeeshan Ali is the first foreigner aboard Tiangong."),
        ("Bangladesh raises garment wage 36% after protests",
         "Workers yet to accept the offer; new protests flare."),
        ("India food inflation squeezes household budgets",
         "Rising prices weigh on families, BBC reports."),
        ("India-Nepal joint military drill begins",
         "Exercise runs in Rupandehi until 8 December."),
        ("Afghan landmine blasts kill 257 this year",
         "Unexploded ordnance toll keeps rising."),
    ]),
    ("EAST ASIA", (16, 110, 110), [
        ("China probes Shanghai party chief Chen Jining",
         "Fourth Politburo member investigated in graft crackdown."),
        ("China Southern orders 50 Boeing 737 MAX jets",
         "Biggest Chinese Boeing deal in nearly a decade, $7.4bn."),
        ("Japan child suicides rise at record pace",
         "NHK reports the fastest increase on record."),
        ("Seoul protests Russian jets near its airspace",
         "South Korea summons Moscow envoy over incursion."),
        ("China cobalt firms race DR Congo export ban",
         "Battery-metal traders rush to beat Kinshasa's freeze."),
    ]),
    ("SOUTHEAST ASIA", (178, 84, 20), [
        ("Dozens of miners trapped in Indonesia mine",
         "Rescuers race rains flooding a 100-metre-deep pit."),
        ("Indonesia factory fire: 3 dead, 34 missing",
         "Blaze engulfs plant; search continues."),
        ("Hanoi gas blast kills six, injures 10",
         "Suspected explosion rips through building."),
        ("Malaysia Airlines orders 10 Boeing 787s",
         "Deliveries planned for 2032-2035."),
        ("Thailand asks China to curb Myanmar mine pollution",
         "Toxic runoff fouls rivers across the border."),
    ]),
    ("OCEANIA", (24, 90, 140), [
        ("Australia-Solomons sign landmark security treaty",
         "Canberra becomes first security partner; no foreign bases."),
        ("Solomons scraps China security pact",
         "Archipelago pivots to Australia four years after Beijing deal."),
        ("US faults Australia's social-media law",
         "Washington says the ban harms free speech."),
        ("Fiji drought emergency may stretch into 2027",
         "Water shortages persist as El Nino builds."),
        ("Pacific fisheries weigh bigeye tuna limits",
         "WCPFC talks open in Vanuatu over catch controls."),
    ]),
]

MARKETS = ("MARKETS  \u2014  Nikkei \u22122.78%  \u00b7  Kospi \u22126%  \u00b7  "
           "Nasdaq \u22121.48%  \u00b7  Brent $87.41 \u22124.37%  \u00b7  "
           "Gold $3,516  \u00b7  Bitcoin $58,999  \u00b7  VIX 26.36")
SOURCES = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 SCMP \u00b7 NHK \u00b7 "
           "Japan Times \u00b7 Al Jazeera \u00b7 Le Monde \u2014 all stories dated 25 November 2026")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    """Greedy word wrap; returns list of lines (at most max_lines)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # ellipsize the last line until it fits
        while lines and draw.textlength(lines[-1] + "\u2026", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = lines[-1] + "\u2026"
    return lines


def draw_story(draw, x, y, w, headline, summary, f_title, f_sum):
    lines = wrap(draw, headline, f_title, w, max_lines=2)
    for ln in lines:
        draw.text((x, y), ln, font=f_title, fill=INK)
        y += 14
    slines = wrap(draw, summary, f_sum, w, max_lines=1)
    for ln in slines:
        draw.text((x, y), ln, font=f_sum, fill=MUTED)
        y += 12
    return y + 5  # gap to next story


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = font(FONT_SERIF_B, 44)
    f_date = font(FONT_SANS_B, 16)
    f_sub = font(FONT_SANS, 13)
    f_top_label = font(FONT_SANS_B, 12)
    f_top_title = font(FONT_SANS_B, 21)
    f_top_sum = font(FONT_SANS, 13)
    f_reg = font(FONT_SANS_B, 14)
    f_title = font(FONT_SANS_B, 12)
    f_sum = font(FONT_SANS, 10)
    f_foot = font(FONT_SANS_B, 11)
    f_src = font(FONT_SANS, 10)

    # ---- header ----
    d.text((12, 8), MASTHEAD, font=f_mast, fill=INK)
    d.text((12, 56), DATE_LINE, font=f_date, fill=RED)
    sw = d.textlength(SUBHEAD, font=f_sub)
    d.text((W - 12 - sw, 58), SUBHEAD, font=f_sub, fill=MUTED)
    d.line([(12, 82), (W - 12, 82)], fill=RULE, width=2)

    # ---- top story banner ----
    bx, by, bw, bh = 12, 90, W - 24, 64
    d.rectangle([bx, by, bx + bw, by + bh], fill=RED)
    d.text((bx + 12, by + 7), "TOP STORY", font=f_top_label, fill=(255, 214, 180))
    title_lines = wrap(d, TOP[0], f_top_title, bw - 24, max_lines=1)
    d.text((bx + 12, by + 24), title_lines[0], font=f_top_title, fill=WHITE)
    d.text((bx + 12, by + 47), TOP[1], font=f_top_sum, fill=(240, 225, 215))

    # ---- region grid: 3 x 3 ----
    gx, gy = 12, 164
    gap = 10
    pw = (W - 2 * gx - 2 * gap) // 3
    ph = 262
    for i, (name, accent, stories) in enumerate(REGIONS):
        col, row = i % 3, i // 3
        x = gx + col * (pw + gap)
        y = gy + row * (ph + gap)
        d.rectangle([x, y, x + pw, y + ph], outline=RULE, width=1)
        d.rectangle([x, y, x + pw, y + 26], fill=accent)
        d.text((x + 8, y + 5), name, font=f_reg, fill=WHITE)
        d.text((x + pw - 30, y + 5), str(len(stories)), font=f_reg,
               fill=(255, 255, 255))
        sy = y + 34
        for headline, summary in stories:
            sy = draw_story(d, x + 8, sy, pw - 16, headline, summary,
                            f_title, f_sum)
        assert sy <= y + ph - 2, "overflow in %s: %d > %d" % (name, sy, y + ph)

    # ---- footer ----
    fy = gy + 3 * ph + 2 * gap + 6
    d.line([(12, fy), (W - 12, fy)], fill=RULE, width=2)
    d.text((12, fy + 8), MARKETS, font=f_foot, fill=DARK)
    d.text((12, fy + 26), SOURCES, font=f_src, fill=MUTED)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
