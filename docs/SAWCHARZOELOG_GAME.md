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
- **Donchitos/Claude-Code-Game-Studios** — MIT, ~40 mil estrelas, v1.3.0 (09/11/2026). Código revisado: as únicas chamadas de rede são a checagem de versão (api.github.com) e o download do three.js (jsdelivr). Não achei nada malicioso. Tem suporte a jogos web com Three.js. **Plano:** usar só `.claude/agents` + `.claude/skills`, **sem** `settings.json`, `hooks/` e `statusline.sh`, para não mudar nossa config.
- **Patch (patch.gg)** — **ABORTADO** (decisão do time em 18/11/2026). Muito novo, testes só no Windows e público por padrão.
- PDF do Drive (skills de motion design) — não se aplica ao jogo agora.

## Repositórios validados para a stack (dados do GitHub em 18/11/2026)
| Repo | ★ | Licença | Uso |
|---|---|---|---|
| mrdoob/three.js | ~119k | MIT | Motor 3D |
| pmndrs/react-three-fiber | ~34k | MIT | Three.js com React |
| pmndrs/drei | ~10k | MIT | Helpers prontos (texto, luzes, telas, vídeo nos painéis LED) |
| pmndrs/react-three-rapier | ~1,7k | MIT | Física e colisão |
| pmndrs/ecctrl | ~0,8k | MIT | Controle de personagem 3ª pessoa |
| pmndrs/zustand | ~59k | MIT | Estado do jogo |
| supabase/supabase | ~115k | Apache-2.0 | Login Google/e-mail, banco, realtime |
| colyseus/colyseus | ~7,5k | MIT | Servidor multiplayer (fase 2) |
| kevinshen56714/SkyOffice | ~1,3k | MIT | Referência de "escritório virtual" multiplayer (2D) |
| workadventure/workadventure | ~5,9k | verificar | Referência de mundo social; licença não identificada pela API |
