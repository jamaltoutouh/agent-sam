# -*- coding: utf-8 -*-
"""Ilustraciones planas (SVG, sin degradados) para la web de AGENT-SAM."""

# Paleta
SKY = "#E3EFF3"
SKY_WARM = "#FBEBD9"
SKY_GREY = "#E4E7EA"
B1, B2, B3 = "#C7D7DD", "#B2C6CE", "#D6E2E6"
WIN = "#EEF5F7"
GREEN, GREEN_D = "#86BE9F", "#4E8E70"
TRUNK = "#7A6250"
WALK = "#ECE6DA"
ROAD = "#5D6971"
BIKE = "#8CC6A7"
TEAL = "#0B6E69"
TEAL_L = "#CFE8E3"
ORANGE = "#E07A3C"
SUN = "#F2B84B"
RED = "#C8462E"
INK = "#24323A"
WATER = "#7DB8D2"
WATER_D = "#5B9CBA"
SKIN = ["#E8BC96", "#C68E62", "#8D5A3B", "#F1CDB0"]
HAIR = ["#3B2A20", "#1F1A17", "#7A4A2A", "#B8B2A8"]


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
            f'<title>{title}</title>{body}</svg>')


def rect(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" {extra}/>'


def circle(x, y, r, fill, extra=""):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" {extra}/>'


def line(x1, y1, x2, y2, stroke, w, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def path(d, fill="none", stroke=None, w=0, extra=""):
    s = f' stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{s} {extra}/>'


def cloud(x, y, s=1, fill="#FFFFFF"):
    return (circle(x, y, 18 * s, fill) + circle(x + 20 * s, y - 8 * s, 22 * s, fill) + circle(x + 42 * s, y, 17 * s, fill)
            + rect(x, y - 2 * s, 42 * s, 19 * s, fill))


def sun(x, y, r, rays=True, color=SUN):
    out = circle(x, y, r, color)
    if rays:
        import math
        for i in range(8):
            a = i * math.pi / 4
            out += line(x + math.cos(a) * (r + 7), y + math.sin(a) * (r + 7), x + math.cos(a) * (r + 17), y + math.sin(a) * (r + 17), color, 4)
    return out


def tree(x, base, s=1, c=GREEN, dark=GREEN_D):
    return (rect(x - 4 * s, base - 40 * s, 8 * s, 40 * s, TRUNK, 2)
            + circle(x, base - 58 * s, 26 * s, c) + circle(x - 16 * s, base - 46 * s, 16 * s, dark) + circle(x + 15 * s, base - 44 * s, 15 * s, c))


def building(x, base, w, h, fill, cols=3, rows=None, win=WIN):
    out = rect(x, base - h, w, h, fill)
    rows = rows or max(1, int(h // 34))
    gw = w / cols
    for r in range(rows):
        for c in range(cols):
            out += rect(x + c * gw + gw * 0.25, base - h + 12 + r * 32, gw * 0.5, 16, win, 2)
    return out


def person(x, y, h, shirt, pants, skin=SKIN[0], hair=HAIR[0], stride=1.0, backpack=None, arm_up=False):
    hr = h * 0.105
    sw = h * 0.25
    top, hip = y - h * 0.80, y - h * 0.40
    out = ""
    # piernas
    out += line(x - sw * 0.2, hip, x - stride * h * 0.13, y - 2, pants, h * 0.1)
    out += line(x + sw * 0.2, hip, x + stride * h * 0.11, y - 2, pants, h * 0.1)
    # mochila
    if backpack:
        out += rect(x - sw * 0.5 - h * 0.12, top + h * 0.04, h * 0.16, h * 0.28, backpack, 3)
    # torso
    out += rect(x - sw / 2, top, sw, hip - top + 2, shirt, h * 0.06)
    # brazos
    out += line(x - sw / 2 + 2, top + 4, x - sw / 2 - stride * h * 0.08, top + h * 0.3, skin, h * 0.07)
    if arm_up:
        out += line(x + sw / 2 - 2, top + 4, x + sw / 2 + h * 0.16, top + h * 0.2, skin, h * 0.07)
    else:
        out += line(x + sw / 2 - 2, top + 4, x + sw / 2 + stride * h * 0.08, top + h * 0.3, skin, h * 0.07)
    # cabeza
    hy = top - hr - 1
    out += circle(x, hy, hr, skin)
    out += path(f"M{x - hr:.1f},{hy:.1f} a{hr:.1f},{hr:.1f} 0 0 1 {2 * hr:.1f},0 q{-hr * 0.4:.1f},{-hr * 0.35:.1f} {-hr:.1f},{-hr * 0.3:.1f} z", hair)
    return out


def bus(x, y, s=1, color="#2F7E8C"):
    w, h = 170 * s, 66 * s
    out = rect(x, y - h, w, h - 8 * s, color, 10 * s)
    for i in range(5):
        out += rect(x + 12 * s + i * 30 * s, y - h + 10 * s, 22 * s, 20 * s, "#DCEFF4", 3)
    out += rect(x + w - 26 * s, y - h + 10 * s, 16 * s, 38 * s, "#DCEFF4", 3)
    out += rect(x, y - 20 * s, w, 6 * s, "#25636E")
    for cx in (x + 34 * s, x + w - 40 * s):
        out += circle(cx, y - 8 * s, 12 * s, "#2B2F33") + circle(cx, y - 8 * s, 5 * s, "#C9CED2")
    return out


def car(x, y, s=1, color="#D9734A"):
    out = path(f"M{x},{y - 12 * s} q0,-12 {12 * s},-14 l{14 * s},-14 h{34 * s} l{16 * s},14 q{12 * s},2 {12 * s},14 v{8 * s} h{-88 * s} z", color)
    out += path(f"M{x + 28 * s},{y - 27 * s} l{10 * s},-10 h{12 * s} v10 z", "#DCEFF4") + path(f"M{x + 54 * s},{y - 27 * s} v-10 h{8 * s} l{10 * s},10 z", "#DCEFF4")
    for cx in (x + 20 * s, x + 66 * s):
        out += circle(cx, y - 4 * s, 9 * s, "#2B2F33") + circle(cx, y - 4 * s, 4 * s, "#C9CED2")
    return out


def bicycle(x, y, s=1, rider=True):
    out = ""
    r = 15 * s
    out += circle(x, y - r, r, "none", f'stroke="{INK}" stroke-width="{3 * s}"') + circle(x + 46 * s, y - r, r, "none", f'stroke="{INK}" stroke-width="{3 * s}"')
    out += path(f"M{x},{y - r} L{x + 18 * s},{y - r - 22 * s} L{x + 40 * s},{y - r - 22 * s} L{x + 46 * s},{y - r} M{x + 18 * s},{y - r - 22 * s} L{x + 22 * s},{y - r} L{x},{y - r}", stroke=TEAL, w=3.5 * s)
    if rider:
        out += line(x + 20 * s, y - r - 26 * s, x + 30 * s, y - r - 54 * s, "#F2A541", 13 * s)  # torso
        out += line(x + 30 * s, y - r - 50 * s, x + 42 * s, y - r - 26 * s, SKIN[1], 4.5 * s)  # brazo
        out += line(x + 20 * s, y - r - 26 * s, x + 26 * s, y - r - 4 * s, "#34495E", 5.5 * s)  # pierna
        out += circle(x + 32 * s, y - r - 66 * s, 9 * s, SKIN[1]) + path(f"M{x + 22 * s},{y - r - 68 * s} a10,9 0 0 1 20,0 z", RED)
    return out


def traffic_light(x, base, s=1):
    return (rect(x - 2.5 * s, base - 110 * s, 5 * s, 110 * s, "#56616A") + rect(x - 11 * s, base - 150 * s, 22 * s, 52 * s, "#2E363C", 5)
            + circle(x, base - 140 * s, 6 * s, "#5B2A24") + circle(x, base - 124 * s, 6 * s, "#5D5326") + circle(x, base - 108 * s, 6 * s, "#4CC38A"))


def school(x, base, w=150, h=110):
    out = rect(x, base - h, w, h, "#F2E4C9") + rect(x - 6, base - h - 10, w + 12, 12, "#C9603A", 2)
    out += rect(x + w / 2 - 16, base - 44, 32, 44, "#8A5A3C", 3)
    for i, cx in enumerate((x + 14, x + w - 44)):
        out += rect(cx, base - h + 22, 30, 24, "#BFE0EA", 2) + rect(cx, base - 58, 30, 24, "#BFE0EA", 2)
    out += circle(x + w / 2, base - h + 30, 13, "#FFFFFF") + line(x + w / 2, base - h + 30, x + w / 2, base - h + 22, INK, 2) + line(x + w / 2, base - h + 30, x + w / 2 + 6, base - h + 30, INK, 2)
    out += line(x + w - 10, base - h - 10, x + w - 10, base - h - 48, "#56616A", 2.5) + path(f"M{x + w - 10},{base - h - 48} h22 l-6,7 l6,7 h-22 z", ORANGE)
    return out


def zebra(x, y, w, h, n=6):
    gap = w / (2 * n - 1)
    return "".join(rect(x + i * 2 * gap, y, gap, h, "#F4F4F0") for i in range(n))


# ----------------------------------------------------------------- hero
def hero():
    W, H = 720, 480
    b = rect(0, 0, W, H, SKY)
    b += sun(612, 82, 30) + cloud(90, 86, 1.1) + cloud(330, 60, 0.8)
    b += building(10, 330, 90, 170, B2) + building(110, 330, 70, 120, B3, cols=2) + building(480, 330, 80, 190, B1) + building(570, 330, 120, 140, B2, cols=4)
    b += building(690, 330, 40, 210, B3, cols=1)
    b += school(250, 330, 190, 130)
    b += tree(200, 332, 1.05) + tree(468, 332, 0.95)
    b += rect(0, 330, W, 30, WALK)
    b += rect(0, 360, W, 20, BIKE) + "".join(rect(20 + i * 70, 369, 34, 3, "#FFFFFF", 1) for i in range(11))
    b += rect(0, 380, W, 70, ROAD) + "".join(rect(20 + i * 80, 413, 44, 4, "#F4F4F0", 2) for i in range(10) if not 4 <= i <= 6)
    b += zebra(330, 380, 140, 70, 7)
    b += rect(0, 450, W, 30, WALK)
    b += bus(30, 444, 0.95) + bicycle(560, 378, 0.9)
    b += traffic_light(486, 352, 0.9)
    # alerta de calor en un poste
    b += rect(116, 250, 5, 82, "#56616A") + rect(96, 214, 46, 46, "#FFFFFF", 8, f'stroke="{ORANGE}" stroke-width="3"')
    b += rect(115, 222, 8, 26, "#F6D7C3", 4) + circle(119, 249, 7, RED) + rect(117, 232, 4, 16, RED, 2)
    # peatones cruzando
    b += person(372, 446, 74, TEAL, "#2F3E46", SKIN[1], HAIR[1], 1.0, arm_up=True)
    b += person(402, 446, 48, ORANGE, "#3C4F76", SKIN[1], HAIR[0], 0.9, backpack="#4D8DC9")
    b += person(436, 446, 50, "#F2C14E", "#2F3E46", SKIN[0], HAIR[2], 1.1, backpack="#C8462E")
    b += person(290, 476, 70, "#7E6BB0", "#3A3A3A", SKIN[3], HAIR[3], 0.7)
    b += person(630, 476, 64, "#4E8E70", "#2F3E46", SKIN[2], HAIR[1], 0.9)
    return svg(W, H, b, "Calle escolar segura: niños cruzando, bicicleta, autobús y alerta de calor")


# ----------------------------------------------------------------- riesgos
def hazard_heat():
    W, H = 400, 260
    b = rect(0, 0, W, H, SKY_WARM) + sun(320, 66, 34, color="#F0A23A")
    for i in range(3):
        y = 60 + i * 26
        b += path(f"M40,{y} q15,-10 30,0 t30,0 t30,0 t30,0", stroke="#F0A23A", w=3)
    b += building(20, 200, 70, 120, "#E8CDB0") + building(250, 200, 90, 90, "#EAD6BF", cols=3)
    b += rect(0, 200, W, 60, "#E9DCC6") + tree(170, 202, 1.1)
    b += path("M120,206 h100 l-10,8 h-80 z", "#00000014")
    b += person(160, 236, 64, "#7E6BB0", "#3A3A3A", SKIN[3], HAIR[3], 0.4)
    b += person(298, 236, 54, ORANGE, "#2F3E46", SKIN[1], HAIR[0], 0.9, backpack="#4D8DC9")
    b += rect(352, 120, 30, 82, "#FFFFFF", 15, f'stroke="{RED}" stroke-width="3"') + rect(362, 132, 10, 52, "#F6D7C3", 5) + rect(362, 150, 10, 34, RED, 5) + circle(367, 190, 10, RED)
    return svg(W, H, b, "Ola de calor en el camino al colegio")


def hazard_flood():
    W, H = 400, 260
    b = rect(0, 0, W, H, SKY_GREY) + cloud(70, 60, 1.4, "#B9C3CB") + cloud(240, 48, 1.6, "#A9B5BE")
    for i in range(16):
        x = 30 + i * 23
        b += line(x, 96 + (i % 3) * 8, x - 8, 118 + (i % 3) * 8, WATER_D, 2.5)
    b += building(0, 190, 80, 80, B1, cols=2) + building(320, 190, 80, 100, B2, cols=2)
    # paso subterráneo
    b += rect(90, 140, 220, 50, "#A7B0B6") + path("M120,190 v-20 a80,40 0 0 1 160,0 v20 z", "#4B555C")
    b += rect(0, 190, W, 70, WALK)
    b += car(150, 214, 0.9, "#D9734A")
    b += rect(0, 196, W, 64, WATER, 0, 'opacity="0.9"')
    for i in range(9):
        b += path(f"M{i * 46},{204} q11,-7 23,0 t23,0", stroke="#FFFFFF", w=2.5)
    b += rect(328, 150, 4, 50, "#56616A") + path("M310,118 l20,-34 l20,34 z", "#F2C14E", stroke=INK, w=2) + line(330, 94, 330, 108, INK, 3) + circle(330, 113, 2, INK)
    return svg(W, H, b, "Paso subterráneo inundado por lluvias intensas")


def hazard_air():
    W, H = 400, 260
    b = rect(0, 0, W, H, "#ECEAE4")
    for (x, y, r) in [(60, 60, 30), (110, 46, 24), (300, 70, 34), (350, 52, 22), (200, 40, 20)]:
        b += circle(x, y, r, "#D3CFC6")
    b += school(240, 190, 130, 90)
    b += building(10, 190, 80, 110, B1, cols=2)
    b += rect(0, 190, W, 70, ROAD) + rect(0, 186, W, 8, WALK)
    for i, (x, c) in enumerate([(14, "#D9734A"), (110, "#4D8DC9"), (206, "#8A8F94"), (302, "#C8462E")]):
        b += car(x, 240, 0.95, c)
        b += circle(x - 6, 226, 8, "#A9A39A") + circle(x - 16, 218, 6, "#BDB7AE") + circle(x - 24, 208, 5, "#CEC9C0")
    b += rect(108, 112, 54, 54, "#FFFFFF", 10, 'stroke="#8A6E3A" stroke-width="3"')
    b += circle(122, 140, 6, "#8A8F94") + circle(136, 132, 7, "#8A8F94") + circle(148, 144, 5, "#8A8F94")
    return svg(W, H, b, "Coches y contaminación a la puerta del colegio")


# ----------------------------------------------------------------- tareas
def _frame(bg):
    return rect(0, 0, 400, 260, bg)


def icon_school(x, y, s=1):
    return (path(f"M{x - 16 * s},{y} v{-16 * s} l{16 * s},{-12 * s} l{16 * s},{12 * s} v{16 * s} z", "#FFFFFF", stroke=ORANGE, w=2.5)
            + rect(x - 4 * s, y - 10 * s, 8 * s, 10 * s, ORANGE))


def icon_health(x, y, s=1):
    return circle(x, y, 15 * s, "#FFFFFF", f'stroke="{RED}" stroke-width="2.5"') + rect(x - 3 * s, y - 9 * s, 6 * s, 18 * s, RED) + rect(x - 9 * s, y - 3 * s, 18 * s, 6 * s, RED)


def icon_bus(x, y, s=1):
    return (rect(x - 13 * s, y - 13 * s, 26 * s, 24 * s, "#2F7E8C", 5) + rect(x - 9 * s, y - 9 * s, 18 * s, 8 * s, "#DCEFF4", 2)
            + circle(x - 7 * s, y + 6 * s, 2.5 * s, "#DCEFF4") + circle(x + 7 * s, y + 6 * s, 2.5 * s, "#DCEFF4"))


def t11():
    b = _frame("#EEF5F3")
    for i in range(7):
        b += line(20 + i * 60, 10, 0 + i * 60, 250, "#FFFFFF", 12)
    for j in range(4):
        b += line(0, 40 + j * 62, 400, 26 + j * 62, "#FFFFFF", 12)
    b += circle(110, 120, 52, ORANGE, 'opacity="0.18"') + circle(300, 180, 40, WATER, 'opacity="0.35"')
    nodes = [(60, 50), (140, 96), (210, 70), (280, 120), (340, 64), (110, 190), (220, 176), (320, 214)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (1, 5), (5, 6), (6, 3), (6, 7), (3, 7), (2, 4)]
    for a, c in edges:
        b += line(*nodes[a], *nodes[c], TEAL, 3.5)
    for (x, y) in nodes:
        b += circle(x, y, 8, "#FFFFFF", f'stroke="{TEAL}" stroke-width="3"')
    b += icon_school(140, 86) + icon_health(280, 112) + icon_bus(220, 176)
    return svg(400, 260, b, "Grafo multimodal del corredor con colegio, centro de salud y parada")


def t12():
    b = _frame("#F3F6F8") + line(40, 220, 370, 220, INK, 2) + line(40, 220, 40, 30, INK, 2)
    obs = [(50, 170), (80, 150), (110, 160), (140, 120), (170, 135), (200, 110)]
    b += path("M200,110 L240,92 L280,104 L320,80 L360,90 L360,150 L320,150 L280,160 L240,140 L200,110 z", TEAL_L)
    b += path("M" + " L".join(f"{x},{y}" for x, y in obs), stroke=INK, w=3)
    b += path("M200,110 L240,116 L280,130 L320,114 L360,120", stroke=TEAL, w=3.5, extra='stroke-dasharray="8 6"')
    for x, y in obs:
        b += circle(x, y, 4, INK)
    b += line(200, 40, 200, 220, "#9AA6AD", 1.5, 'stroke-dasharray="4 5"')
    b += sun(300, 48, 13, color="#F0A23A") + cloud(90, 52, 0.6, "#C6D0D6")
    return svg(400, 260, b, "Predicción generativa con banda de incertidumbre")


def t13():
    b = _frame("#EEF3F5")
    tiles = [("#FFFFFF", "sun"), ("#FDE7D4", "hot"), ("#DCEBF3", "rain"), ("#ECEAE4", "smog")]
    for i, (bg, kind) in enumerate(tiles):
        x, y = 34 + (i % 2) * 174, 24 + (i // 2) * 116
        b += rect(x + 6, y + 6, 160, 100, "#D3DDE1", 12) + rect(x, y, 160, 100, bg, 12, 'stroke="#C9D6DB" stroke-width="1.5"')
        cx, cy = x + 46, y + 48
        if kind == "sun":
            b += sun(cx, cy, 15)
        elif kind == "hot":
            b += sun(cx, cy, 17, color="#E07A3C") + rect(cx + 34, cy - 22, 10, 38, "#FFFFFF", 5, f'stroke="{RED}" stroke-width="2"') + circle(cx + 39, cy + 18, 7, RED)
        elif kind == "rain":
            b += cloud(cx - 22, cy - 6, 0.7, "#9FB2BE") + "".join(line(cx - 14 + k * 12, cy + 14, cx - 18 + k * 12, cy + 26, WATER_D, 2.5) for k in range(4))
        else:
            b += circle(cx - 8, cy, 14, "#BDB7AE") + circle(cx + 10, cy - 6, 12, "#A9A39A") + circle(cx + 4, cy + 10, 10, "#CEC9C0")
        for k in range(3):
            b += rect(x + 86, y + 30 + k * 16, 54 - k * 12, 7, "#C2CDD2", 3)
    return svg(400, 260, b, "Biblioteca de escenarios: día normal, calor, lluvia y contaminación")


def t21():
    b = _frame("#F1F6F4") + rect(0, 112, 400, 36, ROAD) + zebra(180, 112, 40, 36, 3)
    pos = [(70, 60), (330, 60), (70, 200), (330, 200)]
    for (x, y) in pos:
        b += line(x, y, 200, 130, "#9FB7B2", 2.5, 'stroke-dasharray="5 5"')
    for (x, y) in pos:
        b += circle(x, y, 38, "#FFFFFF", f'stroke="{TEAL}" stroke-width="3"')
    x, y = pos[0]
    b += circle(x, y, 22, "#FFFFFF", f'stroke="{RED}" stroke-width="6"') + f'<text x="{x}" y="{y + 7}" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="20" fill="{INK}">30</text>'
    x, y = pos[1]
    b += person(x - 8, y + 20, 34, ORANGE, "#3C4F76", SKIN[1], HAIR[0], 0.9, backpack="#4D8DC9") + person(x + 10, y + 22, 26, "#F2C14E", "#2F3E46", SKIN[0], HAIR[2], 1.0)
    x, y = pos[2]
    b += rect(x - 9, y - 26, 18, 46, "#2E363C", 5) + circle(x, y - 15, 5, "#5B2A24") + circle(x, y - 2, 5, "#5D5326") + circle(x, y + 11, 5, "#4CC38A")
    x, y = pos[3]
    b += icon_bus(x, y, 1.3)
    return svg(400, 260, b, "Cuatro poblaciones de agentes: velocidad, calle escolar, semáforos y autobús")


def t22():
    import random
    rnd = random.Random(7)
    b = _frame("#F3F6F8") + line(48, 222, 372, 222, INK, 2) + line(48, 222, 48, 28, INK, 2)
    for _ in range(46):
        x, y = rnd.uniform(90, 360), rnd.uniform(70, 210)
        if (x - 48) * (y - 28) > 9000:
            b += circle(x, y, 4.5, "#B9C4CA")
    front = [(70, 200), (96, 150), (126, 116), (166, 92), (214, 74), (270, 62), (340, 54)]
    b += path("M" + " L".join(f"{x},{y}" for x, y in front), stroke=TEAL, w=3)
    for x, y in front:
        b += circle(x, y, 7, TEAL)
    b += circle(166, 92, 13, "none", f'stroke="{ORANGE}" stroke-width="3"')
    b += path("M20,60 l10,-6 l10,6 v10 q0,10 -10,14 q-10,-4 -10,-14 z", "#FFFFFF", stroke=TEAL, w=2.5)
    b += path("M332,244 q14,-22 34,-16 q-4,22 -30,22 z", GREEN, stroke=GREEN_D, w=2)
    return svg(400, 260, b, "Frente de Pareto entre seguridad y emisiones")


def t23():
    b = _frame("#EEF5F3")
    b += rect(40, 70, 110, 110, "#FFFFFF", 22, f'stroke="{TEAL}" stroke-width="3"')
    b += rect(66, 100, 58, 40, TEAL, 10) + circle(84, 120, 6, "#FFFFFF") + circle(106, 120, 6, "#FFFFFF") + line(95, 70, 95, 54, TEAL, 3) + circle(95, 50, 6, ORANGE)
    b += rect(250, 70, 120, 110, "#FFFFFF", 22, f'stroke="{TEAL}" stroke-width="3"')
    b += rect(250, 150, 120, 30, ROAD, 0) + zebra(290, 150, 40, 30, 3) + traffic_light(270, 150, 0.6)
    b += person(334, 148, 40, ORANGE, "#3C4F76", SKIN[1], HAIR[0], 0.9, backpack="#4D8DC9")
    b += path("M160,96 C200,70 220,70 244,92", stroke=INK, w=3) + path("M236,84 l10,8 l-12,4", stroke=INK, w=3)
    b += path("M244,160 C210,190 190,190 158,164", stroke=ORANGE, w=3) + path("M168,160 l-12,4 l6,10", stroke=ORANGE, w=3)
    b += path("M190,214 l6,-12 l6,12 l13,1 l-10,8 l3,13 l-12,-7 l-12,7 l3,-13 l-10,-8 z", SUN)
    return svg(400, 260, b, "Aprendizaje por refuerzo: el agente actúa sobre el cruce y recibe recompensa")


def mini_city(x, base, s=1, c1=B1, c2=B2):
    return (building(x, base, 30 * s, 60 * s, c1, cols=2, rows=1) + building(x + 32 * s, base, 26 * s, 84 * s, c2, cols=2, rows=2)
            + building(x + 60 * s, base, 30 * s, 48 * s, c1, cols=2, rows=1))


def t31():
    b = _frame("#F1F5F7")
    b += rect(24, 150, 120, 80, "#FFFFFF", 16) + mini_city(40, 214, 0.95)
    b += rect(256, 150, 120, 80, "#FFFFFF", 16) + mini_city(272, 214, 0.95, "#D4C7B8", "#C2B5A5")
    b += circle(200, 70, 40, "#FFFFFF", f'stroke="{TEAL}" stroke-width="3"')
    for k in range(3):
        b += rect(182, 52 + k * 13, 36, 9, TEAL if k != 1 else ORANGE, 3)
    b += path("M100,146 C110,100 140,80 158,76", stroke=TEAL, w=3) + path("M148,70 l12,6 l-10,8", stroke=TEAL, w=3)
    b += path("M300,146 C290,100 260,80 242,76", stroke=TEAL, w=3) + path("M252,70 l-12,6 l10,8", stroke=TEAL, w=3)
    b += rect(116, 104, 20, 14, ORANGE, 3) + rect(264, 104, 20, 14, ORANGE, 3)
    return svg(400, 260, b, "Aprendizaje federado: dos ciudades comparten modelos, no datos")


def t32():
    import random
    rnd = random.Random(3)
    b = _frame("#EEF3F5")
    for _ in range(70):
        x, y = rnd.uniform(20, 380), rnd.uniform(20, 240)
        if (x - 200) ** 2 + (y - 130) ** 2 > 92 ** 2:
            b += circle(x, y, rnd.uniform(2.5, 5), rnd.choice(["#B9C4CA", "#9FB7B2", TEAL_L]))
    b += path("M200,40 L268,66 V126 C268,172 238,204 200,220 C162,204 132,172 132,126 V66 Z", "#FFFFFF", stroke=TEAL, w=4)
    b += rect(176, 120, 48, 40, TEAL, 7) + path("M184,120 v-12 a16,16 0 0 1 32,0 v12", stroke=TEAL, w=6) + circle(200, 138, 5, "#FFFFFF") + rect(198, 140, 4, 10, "#FFFFFF", 2)
    return svg(400, 260, b, "Privacidad diferencial y agregación segura")


def t33():
    b = _frame("#F3F6F8") + line(48, 222, 372, 222, INK, 2) + line(48, 222, 48, 28, INK, 2)
    b += path("M60,50 C150,56 230,80 270,130 C300,168 330,196 362,206", stroke=TEAL, w=4)
    for (x, y) in [(60, 50), (150, 62), (230, 92), (300, 168), (362, 206)]:
        b += circle(x, y, 6, TEAL)
    b += circle(230, 92, 13, "none", f'stroke="{ORANGE}" stroke-width="3"') + line(230, 105, 230, 222, ORANGE, 2, 'stroke-dasharray="5 5"')
    b += rect(340, 232, 22, 18, TEAL, 4) + path("M345,232 v-6 a6,6 0 0 1 12,0 v6", stroke=TEAL, w=3)
    b += circle(24, 44, 12, "none", f'stroke="{INK}" stroke-width="2.5"') + circle(24, 44, 5, ORANGE)
    return svg(400, 260, b, "Curva de compromiso entre privacidad y utilidad")


# ----------------------------------------------------------------- ciudades
def malaga():
    W, H = 400, 220
    b = rect(0, 0, W, H, SKY) + sun(330, 52, 22) + cloud(60, 50, 0.8)
    b += path("M0,150 C60,90 120,80 170,120 L170,150 Z", "#A9C9A0") + rect(100, 84, 40, 22, "#C9B48F") + "".join(rect(100 + i * 10, 78, 6, 7, "#C9B48F") for i in range(4))
    b += building(170, 150, 60, 70, "#E9D9BD", cols=3, rows=2) + rect(236, 54, 34, 96, "#D8C3A0") + path("M236,54 l17,-24 l17,24 z", "#C9603A")
    b += rect(246, 70, 14, 22, "#B79C74", 7) + building(276, 150, 50, 60, "#EFE3CF", cols=2, rows=2) + building(330, 150, 70, 80, B3, cols=3, rows=2)
    b += rect(0, 150, W, 20, "#EADBB8") + rect(0, 170, W, 50, WATER)
    for i in range(8):
        b += path(f"M{i * 52 + 10},190 q13,-7 26,0", stroke="#FFFFFF", w=2.5)
    b += rect(48, 106, 6, 48, TRUNK) + path("M51,108 q-30,-6 -40,10 M51,108 q-20,-20 -38,-14 M51,108 q24,-18 40,-8 M51,108 q30,0 36,16", stroke=GREEN_D, w=6)
    return svg(W, H, b, "Málaga: costa, catedral y castillo de Gibralfaro")


def melilla():
    W, H = 400, 220
    b = rect(0, 0, W, H, SKY) + sun(70, 50, 20) + cloud(250, 46, 0.9)
    b += path("M150,150 V92 H360 V150 Z", "#D2B48C") + "".join(rect(150 + i * 22, 82, 12, 12, "#D2B48C") for i in range(10))
    b += rect(170, 62, 34, 88, "#C9A77D") + "".join(rect(170 + i * 12, 54, 8, 9, "#C9A77D") for i in range(3))
    b += rect(320, 36, 22, 60, "#FFFFFF") + rect(316, 30, 30, 10, RED) + rect(324, 46, 14, 10, "#F2C14E")
    b += building(20, 150, 70, 70, "#F3E6D2", cols=3, rows=2) + path("M20,80 q35,-26 70,0 z", "#B9D3C9") + building(92, 150, 54, 56, "#E7D2E0", cols=2, rows=2)
    b += rect(0, 150, W, 16, "#BFA27C") + rect(0, 166, W, 54, WATER)
    for i in range(8):
        b += path(f"M{i * 52 + 20},190 q13,-7 26,0", stroke="#FFFFFF", w=2.5)
    return svg(W, H, b, "Melilla: fortaleza de Melilla la Vieja, faro y edificios modernistas")


# ----------------------------------------------------------------- logo
def logo_mark(size=40):
    b = (rect(0, 0, 40, 40, TEAL, 10) + path("M8,30 C14,30 14,20 20,20 C26,20 26,11 32,11", stroke="#FFFFFF", w=3.6)
         + circle(8, 30, 3.6, "#FFFFFF") + circle(32, 11, 4.5, ORANGE))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="{size}" height="{size}">{b}</svg>'


ALL = {
    "hero": hero, "riesgo-calor": hazard_heat, "riesgo-inundacion": hazard_flood, "riesgo-contaminacion": hazard_air,
    "t1-1": t11, "t1-2": t12, "t1-3": t13, "t2-1": t21, "t2-2": t22, "t2-3": t23, "t3-1": t31, "t3-2": t32, "t3-3": t33,
    "malaga": malaga, "melilla": melilla,
}
