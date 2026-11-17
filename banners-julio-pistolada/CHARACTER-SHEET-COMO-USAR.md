# Character sheet — JULIO PISTOLADA

Arquivos nesta pasta:

| Arquivo | Para que serve |
|---|---|
| `character-sheet-julio-pistolada.png` | Ficha completa (fotos reais + paleta + traços). Anexe em **todo** pedido de imagem. |
| `referencias/01-rosto-frente.png` | Rosto de frente: a melhor referência de formato do rosto e da barba |
| `referencias/02-rosto-3-4-oculos-vermelho.png` | Rosto em 3/4 com o óculos assinatura |
| `referencias/03-corpo-inteiro.png` | Corpo e proporção (pra IA não emagrecer o Julio) |
| `referencias/04-detalhe-oculos.png` | Detalhe do óculos de lente vermelha |
| `referencias/05-detalhe-barba.png` | Detalhe do contorno da barba |
| `referencias/06-detalhe-relogio.png` | Detalhe do relógio |

## Como anexar

- **Gerador que aceita várias imagens** (ChatGPT, Gemini/Nano Banana, Midjourney com `--cref`/omni-reference etc.): anexe a ficha completa **e** as fotos `01`, `02` e `03`. Fotos separadas e sem texto costumam dar rosto mais fiel do que só a ficha.
- **Gerador que aceita uma imagem só:** use `01-rosto-frente.png`.
- Os nomes e recursos das ferramentas mudam rápido. Confira na sua ferramenta como ela chama a função de referência de personagem.

---

## Prompt A — “Trava de identidade” (cole antes de qualquer cena)

```
CHARACTER LOCK — JULIO PISTOLADA. The attached character sheet and photos are the ONLY reference for this person. Reproduce his face exactly: round full face with wide cheeks, warm light-brown/tan skin (#A17157 lit, #A97150 shadow), short black tightly-curled hair with a skin fade on the sides, thick full black beard with a sharp lined edge connected to the mustache, full lips. Heavyset, broad, stocky body — never slim him down, never make him muscular or lean. He always wears silver metal wraparound sport sunglasses with ruby-red mirrored lenses. Default outfit: oversized black t-shirt, thin silver chain, chunky black digital sports watch, olive-green cargo shorts. Expression: serious, confident, chin slightly up. Do not change his ethnicity, age, face shape, beard shape or body type. Do not add tattoos, earrings or hats unless asked.
```

Depois disso, cole a cena que quiser do arquivo `PROMPTS-GTA-JULIO-PISTOLADA.md`.

---

## Prompt B — Gerar a ficha ILUSTRADA no estilo GTA (faça uma vez e reaproveite)

Anexe a ficha + as fotos 01, 02 e 03 e peça:

```
Using the attached photos as strict reference, create a professional CHARACTER TURNAROUND SHEET of this man, JULIO PISTOLADA, drawn in the official Grand Theft Auto promotional art style (painted digital illustration, bold dark outlines, cinematic rim light, saturated Vice City sunset palette accents).

Layout on a clean light-gray background, horizontal 16:9:
- Top row: full-body turnaround — FRONT view, 3/4 view, SIDE profile, BACK view — same pose (standing, arms relaxed), same scale, aligned on a baseline.
- Bottom row: 4 head close-ups with different expressions — serious/neutral, confident smirk, shouting/hyped (streamer reaction), laughing.
- Small detail callouts: the silver wraparound sunglasses with ruby-red mirrored lenses (front and side), the beard line, the black digital watch.
- A small color palette strip: skin #A17157, hair/beard #333130, lens #73323A, frame #95908A, shirt #0E0E10, shorts olive green.

Keep his face, beard, skin tone and heavyset body IDENTICAL to the photos in every view. Same outfit in every view: oversized black t-shirt, thin silver chain, olive cargo shorts, black sneakers.
Only text allowed: "JULIO PISTOLADA" as the sheet title at the top-left. No other text, no watermarks.
```

Quando sair uma ficha ilustrada boa, **salve e use ela também como referência** dos próximos banners. É ela que mantém o Julio com a mesma “cara de GTA” em todas as artes.

## Prompt C — Variações de roupa (sem mudar o rosto)

```
Same character as the attached sheet, IDENTICAL face, beard, skin tone, body type and red-lens sunglasses. Only change the outfit to: [ex.: open floral Hawaiian shirt over black tee / black tactical vest / black hoodie / white tank top with gold chain]. Full body, front view, neutral light-gray background, GTA promotional art style.
```

---

## Dicas para o rosto não “fugir”

1. **O óculos ajuda:** como os olhos ficam escondidos, a IA erra menos o rosto. Mantenha o óculos em quase todas as artes.
2. **Se a IA emagrecer o Julio:** repita “heavyset, broad, stocky — do not slim him down” e anexe a `03-corpo-inteiro.png`.
3. **Se a barba mudar:** anexe a `05-detalhe-barba.png` e escreva “beard exactly like reference 05”.
4. **Se o tom de pele mudar:** os códigos de cor (#A17157 etc.) foram medidos nas fotos. Cite eles no prompt. A luz de cada foto muda o tom, então trate os códigos como aproximados.
5. **Gere várias e escolha:** nenhum gerador acerta o rosto 100% das vezes. Gere de 4 a 8 opções e fique com a mais parecida.
6. **Autorização:** o rosto é do Julio. Usem as fotos e as artes só com o ok dele.
