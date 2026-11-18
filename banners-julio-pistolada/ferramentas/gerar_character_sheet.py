"""Gera a ficha de personagem do Julio Pistolada a partir das fotos originais.

Uso: python3 gerar_character_sheet.py <pasta_com_fotos> <pasta_saida>
Fotos esperadas (nomes do envio original): 2.jpg 3.webp 4.jpg 6.jpg 8.jpg 9.jpg
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

IMG, OUT = sys.argv[1], sys.argv[2]
REF = os.path.join(OUT, "referencias")
os.makedirs(REF, exist_ok=True)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font = lambda s, b=True: ImageFont.truetype(F if b else FR, s)
PINK, PURPLE, BG, PANEL, WHITE, GREEN = (255, 46, 160), (140, 70, 255), (18, 14, 28), (34, 26, 50), (245, 245, 250), (83, 252, 24)

op = lambda f: Image.open(os.path.join(IMG, f)).convert("RGB")
p2, p3, p4, p6, p8, p9 = op("2.jpg"), op("3.webp"), op("4.jpg"), op("6.jpg"), op("8.jpg"), op("9.jpg")

crops = {
    "01-rosto-frente-oculos-vermelho": p8.crop((180, 30, 540, 430)),
    "02-rosto-frente-sem-lente-vermelha": p3.crop((420, 120, 1060, 900)),
    "03-rosto-3-4": p4.crop((150, 250, 900, 1150)),
    "04-corpo-inteiro-em-pe": p6,
    "05-bracos-cruzados": p8,
    "06-pose-assinatura-pistolinha": p9,
    "07-corpo-sentado": p2,
    "08-detalhe-oculos": p9.crop((230, 90, 520, 330)),
    "09-detalhe-barba": p3.crop((500, 400, 880, 700)),
    "10-detalhe-relogio": p8.crop((250, 550, 370, 700)),
    "11-detalhe-oculos-lado": p4.crop((170, 540, 800, 900)),
    "12-detalhe-oculos-oficial": p3.crop((520, 300, 860, 460)),
    "13-detalhe-cabelo": p3.crop((520, 140, 860, 330)),
}
for k, v in crops.items():
    v.save(os.path.join(REF, k + ".png"))

def avg(im, box, cond=lambda p: True):
    px = [p for p in im.crop(box).get_flattened_data() if cond(p)]
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3))

swatches = [
    ("PELE (LUZ)", avg(p3, (590, 480, 640, 530))),
    ("PELE (SOMBRA)", avg(p3, (760, 480, 800, 530))),
    ("CABELO/BARBA", avg(p3, (600, 180, 760, 230), lambda p: sum(p) < 200)),
    ("LENTE RUBI", avg(p9, (230, 90, 520, 330), lambda p: p[0] > 170 and p[1] < 80 and p[2] < 120)),
    ("ARMAÇÃO PRATA", avg(p4, (230, 560, 760, 820), lambda p: abs(p[0] - p[1]) < 12 and abs(p[1] - p[2]) < 12 and 120 < p[0] < 200)),
    ("ROSA VICE", (255, 46, 160)),
    ("ROXO VICE", (110, 50, 200)),
]

W, H = 2400, 1700
S = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(S)
for x in range(W):
    t = x / W
    d.line([(x, 0), (x, 8)], fill=tuple(int(PINK[i] * (1 - t) + PURPLE[i] * t) for i in range(3)))
d.text((30, 30), "JULIO PISTOLADA", font=font(78), fill=WHITE)
d.text((32, 118), "FICHA DE PERSONAGEM  •  REFERÊNCIA DE ROSTO PARA IA", font=font(28, False), fill=PINK)
d.text((W - 30, 52), "ÓCULOS OFICIAL:", font=font(30), fill=WHITE, anchor="ra")
d.text((W - 30, 92), "RETANGULAR, LENTE FUMÊ", font=font(30), fill=PINK, anchor="ra")
TOP, BOT = 175, H - 34

def place(im, x, y, w, h, label=None, centering=(0.5, 0.5)):
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=centering)
    d.rectangle([x - 4, y - 4, x + w + 3, y + h + 3], fill=PINK)
    S.paste(im, (x, y))
    if label:
        f = font(22)
        tw = d.textlength(label, font=f)
        d.rectangle([x, y + h - 40, x + tw + 24, y + h], fill=(0, 0, 0))
        d.text((x + 12, y + h - 35), label, font=f, fill=WHITE)

# col 1 – corpo inteiro
place(crops["04-corpo-inteiro-em-pe"], 34, TOP, 590, BOT - TOP, "CORPO INTEIRO", (0.5, 0.3))
# col 2 – rosto frente + pose
c2 = 660
place(crops["02-rosto-frente-sem-lente-vermelha"], c2, TOP, 570, 640, "FRENTE  •  ÓCULOS OFICIAL")
place(crops["06-pose-assinatura-pistolinha"], c2, TOP + 664, 570, BOT - TOP - 664, "POSE ASSINATURA", (0.5, 0.25))
# col 3
c3, r = 1266, 2366
cw = (r - c3 - 40) // 3
place(crops["12-detalhe-oculos-oficial"], c3, TOP, cw, 360, "ÓCULOS OFICIAL")
place(crops["03-rosto-3-4"], c3 + cw + 20, TOP, cw, 360, "3/4")
place(crops["13-detalhe-cabelo"], c3 + 2 * (cw + 20), TOP, cw, 360, "CABELO")
y2 = TOP + 384
place(crops["09-detalhe-barba"], c3, y2, cw, 250, "BARBA")
place(crops["10-detalhe-relogio"], c3 + cw + 20, y2, cw, 250, "RELÓGIO", (0.5, 0.4))
place(crops["01-rosto-frente-oculos-vermelho"], c3 + 2 * (cw + 20), y2, cw, 250, "ÓCULOS ANTIGO: NÃO USAR")

y3 = y2 + 250 + 26
d.text((c3, y3), "PALETA (TIRADA DAS FOTOS, APROXIMADA)", font=font(22), fill=PINK)
sw = (r - c3 - 6 * 14) // 7
for i, (name, col) in enumerate(swatches):
    x = c3 + i * (sw + 14)
    d.rounded_rectangle([x, y3 + 36, x + sw, y3 + 96], 10, fill=col, outline=WHITE, width=2)
    d.text((x, y3 + 102), name, font=font(15), fill=WHITE)
    d.text((x, y3 + 122), "#%02X%02X%02X" % col, font=font(14, False), fill=(180, 180, 195))

ty = y3 + 160
d.rounded_rectangle([c3, ty, r, BOT], 16, fill=PANEL)
d.text((c3 + 26, ty + 20), "TRAÇOS QUE NÃO PODEM MUDAR", font=font(28), fill=PINK)
traits = [
    "Pele morena clara, tom quente",
    "Cabelo crespo BEM curto, colado, degradê alto (NÃO ondulado)",
    "Barba preta cheia e volumosa no queixo, ligada ao bigode",
    "Rosto redondo e cheio, bochechas largas",
    "Corpo ~5 kg mais leve, cabeça proporcional ao corpo",
    "Óculos NOVO: retangular fino, metal prata, lente escura fumê",
    "Relógio grande preto e prata + corrente prata",
    "ROUPA: só trajes de GTA (NÃO a camisa das fotos)",
    "Pose: braços cruzados ou “pistolinha” com a mão; queixo pra cima",
]
for i, t in enumerate(traits):
    yy = ty + 72 + i * 52
    d.ellipse([dx := c3 + 28, yy + 9, dx + 14, yy + 23], fill=GREEN)
    d.text((c3 + 54, yy), t, font=font(23, False), fill=WHITE)

S.save(os.path.join(OUT, "character-sheet-julio-pistolada.png"), optimize=True)
print(swatches)
