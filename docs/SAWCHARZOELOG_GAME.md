# SAWCHARZOELOG _ GAME — Visão e plano inicial

> Status: **ideia salva, nada instalado ainda.** Tudo abaixo depende de aprovação.

## A ideia
- Site que é um **acervo de arcade** + um **hub 3D** onde os players andam e interagem.
- Clima de "sala de jogos" estilo fliperama dos anos 90/2000 (referência de espírito: Pizza Planet do Toy Story), começando simples, mas caprichado.
- Dentro do hub: uma **sala de arcade** com máquinas; chegar perto de uma máquina abre um jogo do acervo. Depois, conectamos os jogos do amigo.
- Login com **Google ou e-mail**.
- Ao entrar, o player escolhe um **nome único** (nunca pode repetir).
- **Criador de personagem** simples: altura/tamanho, cor e tamanho dos olhos, cabelo (estilo + cor), cor da pele, roupa. Botão "aleatório" para gerar automaticamente.
- **Monetização futura**: painéis de LED dentro do mundo 3D e objetos 3D patrocinados; anúncio no site só em **momentos pontuais** (ex.: entre partidas), nunca no meio do jogo.

## Divisão do time
- Eu (Lucas): estrutura do hub 3D, ambiente, criador/gerador de personagem.
- Amigo: jogos do acervo (integração depois).

## Stack proposta (custo zero no início — verificar limites atuais antes de usar)
| Parte | Opção gratuita | Observação |
|---|---|---|
| 3D no navegador | Three.js (+ React Three Fiber, opcional) | Open source (MIT) |
| Login Google/e-mail | Supabase Auth (plano free) | Limites do plano free mudam; conferir em supabase.com/pricing |
| Banco + nome único | Supabase Postgres com `UNIQUE` (case-insensitive) no nome | O banco garante que não repete |
| Players online juntos | Supabase Realtime (presença/posições) no começo | Se crescer: Colyseus (open source, servidor próprio) |
| Hospedagem | Cloudflare Pages / Vercel / GitHub Pages (free) | Conferir termos de uso comercial do plano free |
| Assets 3D/áudio | Kenney.nl, Quaternius, Poly Pizza (muitos CC0) | Sempre conferir a licença de cada asset e manter `CREDITS.md` |
| Personagem | Gerado por código (formas low-poly + parâmetros) | Sem custo, leve, e fácil de randomizar |

## Primeiro marco (MVP)
1. Página com login (Google/e-mail).
2. Tela de criação de personagem + escolha de nome único.
3. Hub 3D: uma sala de arcade com 3–4 máquinas, um painel LED (placeholder de anúncio), luz neon.
4. Andar com WASD/setas (e toque no celular); ver outros players online.
5. Chegar numa máquina → abre um jogo de exemplo em iframe.

## Ferramentas avaliadas (18/11/2026)
- **gamedev-skills/awesome-gamedev-agent-skills** — Apache-2.0, ~9,3 mil estrelas (segundo a página do GitHub). Só arquivos de skill (texto). Risco baixo. **Recomendado:** só `router` + `web-engines`.
- **Donchitos/Claude-Code-Game-Studios** — MIT, ~40 mil estrelas (segundo a página do GitHub). Instala 49 agentes, 18 hooks bash que rodam automaticamente e regras de auto-permissão. Pesado e invasivo para nosso projeto. **Não recomendado agora.**
- **Patch (patch.gg)** — lançado em novembro de 2026, em desenvolvimento inicial. O teste/play exige Windows. Os jogos publicados são **públicos por padrão**. O site não abriu daqui (rede bloqueada). **Adiar.**
- PDF do Drive (skills de motion design) — não se aplica ao jogo agora.
