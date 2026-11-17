import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

IMG, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT + "/referencias", exist_ok=True)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font = lambda s, b=True: ImageFont.truetype(F if b else FR, s)

PINK, PURPLE, BG, PANEL, WHITE, GREEN = (255, 46, 160), (140, 70, 255), (18, 14, 28), (34, 26, 50), (245, 245, 250), (83, 252, 24)

body = Image.open(IMG + "/2.jpg").convert("RGB")
front_src = Image.open(IMG + "/3.webp").convert("RGB")
tq_src = Image.open(IMG + "/4.jpg").convert("RGB")

crops = {
    "01-rosto-frente": front_src.crop((420, 120, 1060, 900)),
    "02-rosto-3-4-oculos-vermelho": tq_src.crop((150, 250, 900, 1150)),
    "03-corpo-inteiro": body,
    "04-detalhe-oculos": tq_src.crop((170, 540, 800, 900)),
    "05-detalhe-barba": front_src.crop((500, 400, 880, 700)),
    "06-detalhe-relogio": body.crop((600, 1260, 860, 1460)),
}
for k, v in crops.items():
    v.save(f"{OUT}/referencias/{k}.png")

# colour swatches sampled from the photos
def avg(im, box, cond=lambda p: True):
    px = [p for p in im.crop(box).get_flattened_data() if cond(p)]
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3))

skin_l = avg(front_src, (590, 480, 640, 530))
skin_s = avg(front_src, (760, 480, 800, 530))
hair = avg(front_src, (600, 180, 760, 230), lambda p: sum(p) < 200)
lens = avg(tq_src, (420, 640, 640, 750), lambda p: p[0] > 90 and p[1] < 65 and p[2] > 40)
frame = avg(tq_src, (230, 560, 760, 820), lambda p: abs(p[0] - p[1]) < 12 and abs(p[1] - p[2]) < 12 and 120 < p[0] < 200)
swatches = [("PELE (LUZ)", skin_l), ("PELE (SOMBRA)", skin_s), ("CABELO/BARBA", hair),
            ("LENTE RUBI", lens), ("ARMAÇÃO PRATA", frame), ("CAMISA", (14, 14, 16))]

W, H = 2400, 1700
S = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(S)

# header
for x in range(W):
    t = x / W
    c = tuple(int(PINK[i] * (1 - t) + PURPLE[i] * t) for i in range(3))
    d.line([(x, 0), (x, 8)], fill=c)
d.text((30, 30), "JULIO PISTOLADA", font=font(78), fill=WHITE)
d.text((32, 118), "FICHA DE PERSONAGEM  •  REFERÊNCIA DE ROSTO PARA IA", font=font(28, False), fill=PINK)
d.text((W - 30, 52), "SEMPRE COM O ÓCULOS", font=font(30), fill=WHITE, anchor="ra")
d.text((W - 30, 92), "DE LENTE VERMELHA", font=font(30), fill=PINK, anchor="ra")

TOP = 175

def place(im, x, y, w=None, h=None, label=None):
    if w and h:
        im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    elif w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    else:
        im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    d.rectangle([x - 4, y - 4, x + im.width + 3, y + im.height + 3], fill=PINK)
    S.paste(im, (x, y))
    if label:
        f = font(24)
        tw = d.textlength(label, font=f)
        d.rectangle([x, y + im.height - 44, x + tw + 28, y + im.height], fill=(0, 0, 0))
        d.text((x + 14, y + im.height - 38), label, font=f, fill=WHITE)
    return im.size

# col 1: full body
place(crops["03-corpo-inteiro"], 34, TOP, w=670, h=H - TOP - 34, label="CORPO INTEIRO")
# col 2: faces
cx = 740
w2, h2 = place(crops["01-rosto-frente"], cx, TOP, w=580, h=700, label="FRENTE")
place(crops["02-rosto-3-4-oculos-vermelho"], cx, TOP + h2 + 20, w=580, h=H - TOP - h2 - 54, label="3/4  •  ÓCULOS ASSINATURA")

# col 3: details
dx = 1360
gw, gh = place(crops["04-detalhe-oculos"], dx, TOP, h=330, label="ÓCULOS")
place(crops["05-detalhe-barba"], dx + gw + 24, TOP, w=2366 - (dx + gw + 24), h=330, label="BARBA")
y2 = TOP + 330 + 24
ww, _ = place(crops["06-detalhe-relogio"], dx, y2, w=330, h=290, label="RELÓGIO")

# swatches
sx, sy = dx + ww + 30, y2
d.text((sx, sy), "PALETA (TIRADA DAS FOTOS)", font=font(24), fill=PINK)
for i, (name, col) in enumerate(swatches):
    cxx, cyy = sx + (i % 3) * 215, sy + 42 + (i // 3) * 125
    d.rounded_rectangle([cxx, cyy, cxx + 195, cyy + 72], 10, fill=col, outline=WHITE, width=2)
    d.text((cxx, cyy + 78), name, font=font(17), fill=WHITE)
    d.text((cxx, cyy + 100), "#%02X%02X%02X" % col, font=font(15, False), fill=(180, 180, 195))

# traits
ty = y2 + 290 + 34
d.rounded_rectangle([dx, ty, 2366, H - 34], 16, fill=PANEL)
d.text((dx + 28, ty + 22), "TRAÇOS QUE NÃO PODEM MUDAR", font=font(30), fill=PINK)
traits = [
    "Pele morena clara, tom quente",
    "Cabelo preto crespo/cacheado curto, degradê (fade) nas laterais",
    "Barba cheia preta, contorno marcado + bigode ligado",
    "Rosto redondo e cheio, bochechas largas",
    "Corpo robusto / plus size, ombros largos (NÃO emagrecer)",
    "Óculos esportivo prata com lente espelhada vermelha",
    "Camiseta preta oversized, corrente prata fina",
    "Relógio digital preto grande, bermuda cargo verde-oliva",
    "Expressão: séria, confiante, queixo levantado",
]
for i, t in enumerate(traits):
    yy = ty + 95 + i * 62
    d.ellipse([dx + 30, yy + 11, dx + 46, yy + 27], fill=GREEN)
    d.text((dx + 60, yy), t, font=font(27, False), fill=WHITE)

S.save(OUT + "/character-sheet-julio-pistolada.png", optimize=True)
print(swatches)
