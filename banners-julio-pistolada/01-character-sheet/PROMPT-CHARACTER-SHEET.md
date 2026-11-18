# ETAPA 1 — Character sheet do JULIO PISTOLADA (versão corrigida)

**Correções do cliente aplicadas:**
1. **Mais magro que nas fotos:** o cliente pediu menos peso. A trava agora pede uns 10 a 15 kg a menos, sem deixar de ser ele.
2. **Só traje de GTA:** nada de camisa de time, colete, chinelo ou bandana, que deixavam “estilo favela”.
3. **Visual 3D de jogo:** não pode sair cartoon.

**A ficha é SÓ DA CABEÇA.** Ela trava o rosto. O corpo (peso) e a roupa vêm em cada prompt de cena, conforme a referência de traje de GTA. A trava de identidade continua com a linha de peso, para o corpo sair certo nas cenas.

Faça **na ordem**: 1A (rosto) → 1B (expressões). Só avance quando a 1A estiver aprovada.

---

## O que anexar (na 1A e na 1B)

| Arquivo (`referencias/`) | Por quê |
|---|---|
| `01-rosto-frente-oculos-vermelho.png` | Rosto oficial |
| `03-rosto-3-4.png` | Rosto em outro ângulo |
| `09-detalhe-barba.png` | Formato da barba |

**Não anexem** a ficha montada (`character-sheet-julio-pistolada.png`) no gerador. Ela tem muita camisa do Narizes e texto, e a IA copia. Ela serve para **vocês** conferirem o resultado.

---

## BLOCO 1 — TRAVA DE IDENTIDADE (cole sempre primeiro)

```
CHARACTER LOCK — JULIO PISTOLADA. The attached photos are the ONLY reference for this man's identity. Reproduce him exactly:
- Face: round full face, wide cheeks, warm light-brown/tan skin (#A17157 lit, #A97150 shadow), full lips. Same face shape as the photos.
- HAIR (important): very short, tight, coily/kinky black hair pressed close to the head on top, high skin fade on the sides. NOT wavy, NOT loose curls, NOT long.
- Beard: thick full black beard (#333130), fuller and slightly longer at the chin, sharp lined cheek edge, connected to the mustache.
- BODY WEIGHT LOCK: make him only slightly lighter than in the reference photos (about 5 kg), with head size correct for his body and the same build in face and body — a solid, broad-shouldered, sturdy build with only a slight belly, thick arms, defined jawline under the beard, no double chin, slimmer neck and slightly less full cheeks. He must still be clearly recognizable as the same man (same face shape, same beard, same skin). Do NOT make him fat or obese, do NOT exaggerate belly, cheeks or neck; also do NOT make him skinny or a bodybuilder. Realistic adult proportions, normal-sized head.
- [ÓCULOS] — always on his face. (Troque [ÓCULOS] pela linha escolhida em 02-cenas-gta/V2-CORRECOES-CLIENTE.md)
- Accessories: large black-and-silver chronograph watch on the left wrist, thin silver chain.
- Attitude: serious, confident, chin slightly up.
- CLOTHING LOCK: IGNORE the clothes in the reference photos completely (never the black jersey with a crest, never "NARIZES FC", never the red-and-blue sleeve band). He only wears GTA video game protagonist wardrobe as described in the prompt. Never: football jerseys, tactical vests, bandanas, balaclavas, slide sandals, flip-flops.
Do not change his ethnicity, age (mid-twenties), face shape, beard shape or weight. No tattoos, earrings or hats unless the prompt asks.
```

## BLOCO 2 — ESTILO 3D DE JOGO (cole logo depois)

```
STYLE — 3D VIDEO GAME CHARACTER: render him as a real-time 3D character model from a modern open-world crime video game, like Grand Theft Auto V on PC at max settings / Grand Theft Auto VI (Rockstar RAGE engine look). Realistic human proportions but a clearly VIDEO-GAME look: smooth, slightly simplified game-model skin (no real-life pores), stylized game-model features, game-quality curly hair and beard, clean game textures, game-engine lighting. It must look like a 3D character model viewer inside the game, NOT a real photo, NOT hyperrealistic, NOT a drawing.
NEGATIVE: no real photo, no hyperrealism, no film look, no cartoon, no comic, no illustration, no painting, no cel shading, no black outlines, no anime, no caricature, no big head, no exaggerated body, no vector art.
```

---

## 1A — FICHA DA CABEÇA (gere primeiro e aprove o rosto)

```
[BLOCO 1]
[BLOCO 2]

3D HEAD TURNAROUND SHEET of JULIO PISTOLADA, horizontal 16:9, neutral mid-gray 3D studio backdrop, soft three-point lighting, same lighting in every view.
HEAD ONLY — no body, no outfit: each view is cropped at the base of the neck (only a hint of a plain dark neutral collar, no logos, no clothing details).
TOP ROW — 5 head renders at the same scale: FRONT, 3/4 LEFT, LEFT PROFILE, 3/4 RIGHT, BACK OF THE HEAD.
BOTTOM ROW — 2 bigger close-ups: FRONT close-up and 3/4 close-up, showing the game-model beard texture, hair fade and the reflection on the red lenses; plus a small render of the sunglasses alone (front and side).
He wears the sunglasses described in the lock in every head view.
Match the reference photos exactly: face shape, beard line and length, hair fade, skin tone — but with the slimmer neck, no double chin and slightly less full cheeks from the weight lock. Neutral serious expression.
Only text: "JULIO PISTOLADA" small in the top-left corner.
```

**Aprova se:** o rosto é dele, a barba tem o mesmo formato, a pele tem o mesmo tom, o óculos está certo, e o rosto está **um pouco mais magro que nas fotos** (pescoço mais fino, sem papada), mas ainda é claramente o Julio. Mostrem pro Julio e salvem a aprovada como `APROVADO-1A-cabeca.png`.

---

## 1B — EXPRESSÕES (só cabeça)

Anexe a `APROVADO-1A-cabeca.png` + `01-rosto-frente-oculos-vermelho.png`.

```
[BLOCO 1]
[BLOCO 2]

3D EXPRESSION SHEET of JULIO PISTOLADA — HEAD ONLY: 3x3 grid of in-engine head renders cropped at the neck (no outfit details), same lighting, neutral gray studio backdrop, sunglasses ON in all:
1 serious/neutral, 2 confident smirk, 3 hyped shouting (streamer reaction), 4 laughing, 5 shocked, 6 angry frown, 7 eyebrow raised (one brow above the glasses), 8 chin up looking down at the camera, 9 tired-but-smiling (marathon mode).
Same face, beard and weight in all 9 — slimmer neck and jawline, no double chin. Only text: "JULIO PISTOLADA" small at the top.
```

---

## Se der errado

| Problema | Correção (mande como edição na imagem que saiu) |
|---|---|
| Saiu mais gordo | `Make him slightly slimmer to match the full-body reference photo exactly: smaller belly, less double chin, thinner neck. Keep face and beard identical.` |
| Saiu magro demais / rosto mudou | `Keep him recognizable: face only slightly slimmer than the reference photos, same cheeks shape and beard.` Ou troque “10-15 kg” por “5-10 kg” na trava. |
| Saiu cartoon | Comece com `3D game screenshot, Rockstar RAGE engine render, realistic` e peça `not fan art, not illustration`. |
| Apareceu roupa/camisa | Reforce `HEAD ONLY — no clothing details` e anexe só os recortes de rosto. |
| Rosto diferente | Gere 4 a 8 opções e escolha. Se a ferramenta deixar, use a função de referência de personagem/rosto. |

Daqui pra frente, **todo prompt de cena** leva: a `APROVADO-1A-cabeca.png` anexada + a TRAVA DE IDENTIDADE + o traje de GTA da cena. Assim o rosto vem da ficha e a roupa vem do prompt.
