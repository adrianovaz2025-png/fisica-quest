# IMPÉRIO: contexto para continuar o desenvolvimento

Este documento é para quem (pessoa ou IA) vai continuar o jogo. Leia inteiro antes de mexer.

---

## 1. O que é

O **Império** é um jogo educacional em pixel art, com cara de RPG e Age of Empires. Foi feito pelo professor **Adriano Vaz** (Física, Colégio Império – Unidade III, Três Corações/MG) para os alunos do Ensino Médio.

- **Turmas e tribos:** cada turma é uma tribo, e os pontos dos alunos fazem a aldeia da tribo crescer.
  - 1A: LOBOS
  - 1B: FALCÕES
  - 2A: URSOS
  - 2B: SERPENTES
  - 3A: DRAGÕES
- **Onde se ganha pontos:** respondendo questões reais de vestibular na aba **VESTIBULARES** (a tela chama **Cidadela das Provas**).
- **Bancas:** ENEM 2017–2025, EsPCEx 2025–2026 e IF Sul de Minas 2025–2026.
- **Personalização:** o aluno personaliza o herói (cabelo, pele, cores, armaduras, espadas, escudos) e anda num mapa isométrico de uma ilha.
- **Público e uso:** alunos de 14 a 18 anos, que jogam em grande parte pelo celular (na horizontal) e também no computador.

**URLs**
- Jogo: https://adrianovaz2025-png.github.io/fisica-quest/
- Versão de teste (mesmo código, título "· TESTE"): `.../fisica-quest/teste.html`
- Painel do diretor (estatísticas por turma, com código de acesso): `.../fisica-quest/diretor.html`
- Repositório: GitHub `adrianovaz2025-png/fisica-quest`, publicado via GitHub Pages a partir da branch `main`

---

## 2. Arquitetura (tudo estático)

```
index.html        ← O JOGO INTEIRO (~550 KB): HTML + CSS + JS num arquivo só, sem build, sem framework
teste.html        ← cópia do index (só muda o <title>). TODA alteração vai nos DOIS arquivos.
diretor.html      ← painel do diretor (lê a RPC painel_diretor com um código)
q/                ← bancos de questões (JSON) e imagens
  questoes.json   ← Física (ENEM + EsPCEx)
  matematica.json, quimica.json, biologia.json, linguagens.json, humanas.json
  orig/*.webp     ← recorte de cada questão (as questões são mostradas como IMAGEM)
  img/*.webp      ← imagens antigas de questões de física
  res/fis.json, qui.json, bio.json ← resoluções comentadas
supabase/schema.sql                 ← banco inteiro (tabelas, RLS, funções)
supabase/functions/recuperar-senha  ← Edge Function de recuperação de senha por e-mail
tools/            ← scripts usados para gerar conteúdo (ver §9)
```

**Backend:** Supabase.
- Projeto `deebihpvewibzciwwpyc`.
- URL e chave *publishable* (pública) estão em `CONFIG` no topo do script do index.
- Autenticação: cada aluno tem um e-mail interno `nick@fisicaquest.app`; nenhum e-mail é enviado.
- Toda lógica sensível (pontos, limites, admin) fica em **funções SQL SECURITY DEFINER**. O cliente não grava pontos direto.

**Modo demo:** com `SUPABASE_URL` vazio o jogo roda offline e salva em `localStorage` (útil para testar). `const API = ONLINE ? Supa : Demo`.

---

## 3. Mapa do index.html

O script principal está dividido por banners `/* ====== NOME ====== */`. Use `grep -n "/\* ====" index.html` para navegar.

| Seção | O que tem |
|---|---|
| CONFIG (topo) | URL/chave Supabase, `ENEM_DATA`, `NIVEIS` (pontos da tribo), `TURMAS_ABERTAS`, flags |
| TURMAS / TRIBOS | `TURMAS`, `COR` |
| ITENS (catálogo) | `IT_RAW` → `IT` (mapa id→item) e `ITL` (lista). **Itens que estão só em `IT` e não em `ITL` não aparecem em loja nem baú.** |
| AVATARES 64x64 | `sprite(L,eq,fr,back,solo)` desenha o herói; `drawChar(x,L,eq,fr,px,py,escala)` |
| EQUIPAMENTOS / ARMADURAS / ESPADAS / ESCUDOS | `ARMT` (temas de armadura: cores, nível), `eqPeito/eqCabeca/eqBotas/eqDorso`, `armP(t)`, `armT(id)` |
| MOTOR ISOMÉTRICO, TERRENO, MUNDO DAS TRIBOS | mapa da ilha, castelos, vilas que evoluem com os pontos |
| ILHAS DA JORNADA / FORTALEZAS / MAPA-MÚNDI | aba JORNADA (hoje `CONFIG.JORNADA=false`: só exploração, sem pontos) |
| CIDADELA DAS PROVAS | desenho da torre no mapa (botão leva à aba `enem`) |
| API (DEMO + SUPABASE) | objeto `Supa`/`Demo` com todos os métodos (login, cadastro, rpc...) |
| ESTADO DO JOGO / LOOP | `me` (perfil logado), `screen`, `tab` ('jornada','tribos','enem','heroi','admin'), `T0` (tempo) |
| ABA HERÓI | inventário, personalização, armaduras com cor editável (`L.arm={b,a}`) |
| ABA ENEM (= VESTIBULARES) | `ES` (estado), `renderEnem()`, telas `ES.scr`: `home → prova → mat → qtd → q (questões) → res` |
| BANCO ENEM REAL | `MATERIAS`, `QXF` (arquivo de cada matéria), `loadQX`, `qPool`, `PRV(X)` (rótulo da prova), `bancaOk`, resoluções (`loadRes`, `resBlock`) |
| PAINEL DO PROFESSOR (aba ALUNOS, só admin) | lista de alunos, estatísticas, **AO VIVO** (`renderVivo`), **VISÃO POR TURMA**, código do diretor, **modo manutenção** |
| NOVIDADES | cartaz/pop-up `showNews()`; aparece 1x por aluno por versão (`NEWS.v`, `localStorage fq_news_<nick>`) |
| PERSONALIZAÇÃO DO AVATAR | editor do herói |

Há um **segundo `<script>`** no fim do arquivo com as armaduras novas (**Físico da Peste** e **Geada Eterna**). Elas são desenhadas e aparecem no cartaz de novidades, mas **ainda não podem ser obtidas** (estão só em `IT`).

### Telas da aba VESTIBULARES
1. **home:** Cidadela das Provas, contagem regressiva (`PROVAS_DATAS`: ENEM 08/11/2026, IF 06/12/2026, EsPCEx "SET/2027"), botão SIMULADO.
2. **prova:** escolher ENEM / ESPCEX / IF SUL DE MINAS (`PROVAS`).
3. **mat:** matérias da prova:
   - ENEM: Geral, Física, Matemática, Química, Biologia, Linguagens, Humanas.
   - EsPCEx: Prova completa, Física, Matemática, Química, Português+Inglês, Geografia+História (`MAT_ESP`).
   - IF: Prova completa, Matemática, Língua Portuguesa (`MAT_IF`).
4. **qtd:** quantidade, ano, dia (EsPCEx), modo TREINO (corrige a cada questão) ou PROVA (corrige no final).
5. Questões e resultado. No treino e na revisão aparece **📖 VER RESOLUÇÃO**, quando existe.

---

## 4. Bancos de questões (`q/*.json`)

Cada arquivo é um array. Formato de uma questão:

```json
{"id":"x2025d1_21","ano":2025,"num":21,"area":"MEC","lg":"","parts":[],"alts":[{"l":"A","h":""},...],
 "orig":"x2025d1_21.webp","osz":[w,h],"modo":"img","gab":"C","gsrc":"oficial","tema":"MEC",
 "banca":"espcex","dia":1}
```

- **`banca`:** ausente = ENEM; também `'espcex'` e `'ifsul'`. O IF tem **4 alternativas (A–D)**; ENEM e EsPCEx têm 5.
- **Questões anuladas:** `anulada:true` e `gab:null`. São filtradas no carregamento (`q.gab && !q.anulada`).
- **`lg`:** língua estrangeira ('ing'/'esp') nas de Linguagens do ENEM.
- **`tema`:** códigos por matéria. Física: MEC, TER, OPT, OND, ELE, MOD. Os das outras matérias estão em `tools/provas/cls_temas.py`.
- **Prefixos de id:**
  - ENEM: `2019_105`, `m2020_136`, `q...`, `b...`
  - EsPCEx: `x{ano}d{dia}_{n}`
  - IF: `f{ano}_{n}`
- **Contagem atual:**

  | Banco | Total | ENEM | EsPCEx | IF |
  |---|---|---|---|---|
  | Física | 159 | 135 | 24 | — |
  | Matemática | 360 | 270 | 40 | 50 |
  | Química | 119 | 95 | 24 | — |
  | Biologia | 82 | 82 | — | — |
  | Linguagens | 364 | 250 | 64 | 50 |
  | Humanas | 273 | 225 | 48 | — |

- **Recortes:** todos foram conferidos visualmente (de A a E, sem cortar a alternativa final).

### Resoluções (`q/res/<mat>.json`)
- **Formato:** `{ "<id>": { "t": "texto", "esq": "<svg>…</svg>" (opcional), "aula": "" } }`.
- **Frações no texto:** `[[a|b]]`.
- **`aula`:** reservado para o futuro (link para a aula que explica a questão).
- **Prontas:** Física 133, Química 94, Biologia 81 (todas do ENEM), conferidas contra o gabarito.
- **Matemática:** **177 prontas, ainda NÃO publicadas**, em `tools/resolucoes/mat_parcial_NAO_PUBLICADO.json` (ENEM 2020, 2021, 2024, 2025). Faltam 2022 e 2023. Para publicar, salve como `q/res/mat.json`.

---

## 5. Banco de dados (resumo; detalhes em `supabase/schema.sql`)

**Tabelas**
- `perfis`: um por aluno.
  - `pontos = fases*10 + (fases/6)*50 + bonus`
  - `equip` (jsonb): inventário, stats do ENEM em `equip.enem`, guardiões em `equip.guard`, flag `equip.manut`.
  - `visual` (jsonb): aparência.
  - presença: `visto_em/visto_dia/min_hoje/primeiro_hoje`.
- `turmas`: inclui a turma `PROF` e o **código de cadastro de cada turma**, que é secreto.
- `registro`: log **imutável** de tudo (cadastro, perfil, simulado…).
- `recuperacao` (e-mail de recuperação), `recup_pedidos`, `diretor_acesso` (hash do código do diretor).

**Regras de pontuação** (em `_registrar_simulado_base`)
- Cada acerto vale +2 pontos.
- Limite diário: **400 pontos e 20 erros**, no fuso America/Sao_Paulo.
- Anti-spam: simulado entregue rápido demais vale 0.
- Só `p_fonte='enem'` pontua.
- Professor não pontua.

**Admin:** é o perfil com `admin=true`, nick `adrianovaz`, turma `PROF`. As funções `admin_*` checam isso.

**Operações comuns** (no SQL Editor do Supabase, como `postgres`)

```sql
-- redefinir senha de um aluno
update auth.users set encrypted_password = extensions.crypt('NOVASENHA', extensions.gen_salt('bf'))
 where id = (select id from perfis where lower(nick)=lower('NICK'));
-- trocar aluno de turma
update perfis set turma='2A' where lower(nick)=lower('NICK');
-- devolver erros do dia a uma turma (ex.: +30 erros para o 2B)
update perfis set erros_dia = greatest(0, least(erros_dia,20) - 30) where turma='2B';
```

O professor também redefine senhas pelo próprio jogo (painel → aluno → redefinir senha, RPC `admin_redefinir_senha`).

**Segredos que NÃO estão no repositório** (pergunte ao professor ou leia no banco):
- senhas
- códigos das turmas (`turmas.codigo`)
- código do diretor
- chave `service_role`

---

## 6. Como trabalhar (fluxo que vinha sendo usado)

1. **Edite `index.html` e `teste.html` igualmente.** O fluxo usado foi um script Python de "patch" com substituições exatas e `assert` de contagem (`rep(a,b)` em `tools/patches/*.py`), aplicado aos dois arquivos:
   ```bash
   for f in index.html teste.html; do python3 tools/patches/patch_x.py $f; done
   ```
2. **Cheque a sintaxe:**
   ```bash
   node -e "const s=require('fs').readFileSync('index.html','utf8');for(const x of s.matchAll(/<script>([\s\S]*?)<\/script>/g))new Function(x[1]);console.log('ok')"
   ```
3. **Teste localmente** com Playwright: `python3 -m http.server`, abrir o index e simular um usuário:
   ```js
   me={nick:'t',turma:'1A',equip:{}}; screen='game'; setTab('enem')
   ```
   - Viewport **horizontal**: na vertical aparece "GIRE O CELULAR".
   - Tire print e confira.
   - Para o painel AO VIVO, substitua `API.aoVivo` por dados falsos.
4. **Commit e push na `main`** (o GitHub Pages publica em ~1 min). Autor usado:
   ```bash
   git -c user.name="adrianovaz2025-png" -c user.email="adrianovaz.2025@gmail.com" commit -m "..."
   ```
5. **Avise o professor para recarregar com Ctrl+F5.** O cache do navegador costuma mostrar a versão antiga, e isso já causou confusão.

**Atenção a:**
- **Constantes globais:** o script é um arquivo só, com `'use strict'` e muitas constantes de nome curto (`el`, `$`, `T`, `ES`, `AD`, `IT`…). Antes de criar um nome novo, cheque se ele já existe (`grep`).
- **Cores e estética:** o estilo visual é forte (marrom, dourado, fonte "Press Start 2P", pixel art). Mantenha a paleta e use `el()`, `eBtn()` e as classes existentes (`.box`, `.ov`, `.big`, `.lnk`, `.echip`, `.eopt`, `.estats`, `.adt`).
- **Pop-ups:** são `.ov` + `.ov.on`. O pedido de e-mail não abre se outro `.ov` estiver aberto.
- **Mobile primeiro:** sempre confira a largura estreita. A barra de abas é desenhada em canvas, e as posições ficam em `['jornada','JORNADA','flag',x,w]…`; há uma versão compacta quando `VW<470`.

---

## 7. Preferências do professor

- **Comunicação:** direta e curta. Mostre **prévia (print) antes de publicar** quando for algo visual ou um anúncio para os alunos; ele pede isso explicitamente.
- **Alterações:** pequenas e em sequência. Ele manda prints apontando o problema ("corrija essa coluna", "desalinhado").
- **Fontes:** prefere conteúdo verificado em fonte oficial (gabaritos oficiais, editais).
- **Propriedade intelectual:** **não copiar personagens com direitos** (ex.: Cavaleiros do Zodíaco). Ele pediu o "Cavaleiro de Cisne", e foi feita a **Geada Eterna**, original e inspirada em gelo.
- **Idioma:** português do Brasil, em tudo.

---

## 8. Pendências / próximos passos

1. **Armaduras novas: Físico da Peste, Geada Eterna e Guardião do Natal.**
   - O visual já está pronto (protótipos em `tools/armaduras/`, prancha em `prancha.js`).
   - Físico e Geada já estão no index (2º script), mas **ninguém consegue obter**.
   - Falta o professor decidir **como serão ganhas** (por pontos como `ARM_PTS`, como prêmio de simulado, ou liberadas para todos).
   - Depois disso, falta criar a entrada em `ITL` e na regra de recompensa.
   - O **Guardião do Natal** (`natal_arm.js`) é para um cartaz próprio em dezembro.
2. **Resoluções:**
   - terminar Matemática ENEM 2022 e 2023 e publicar `q/res/mat.json`;
   - depois fazer Humanas (225) e Linguagens (250);
   - depois EsPCEx e IF. O IF publica **gabaritos comentados oficiais**, que podem virar o texto da resolução.
   - Futuro: preencher `aula` para levar o aluno à aula que explica a questão.
3. **Data da EsPCEx 2027:** quando sair o edital, troque `null` pela data em `PROVAS_DATAS` (a prova de 2026 foi em 12–13/09).
4. **Novas provas:** o professor pode pedir mais vestibulares e anos. O fluxo foi:
   - baixar o PDF da prova e o gabarito oficial;
   - recortar com `tools/provas/x3_*.py` (âncoras "QUESTÃO NN", textos compartilhados, colunas);
   - montar com `build_*.py`;
   - adicionar a banca em `PROVAS`, `MATERIAS`, `QXF`, `loadQX` e `PRV`, como foi feito para `espcex` e `ifsul` (ver `tools/patches/patch_ifsul.py`).
5. **Cartaz de novidades:** para um novo anúncio, edite `NEWS` (mude `v` para a data nova, `cards`, `sub`, `arm`) e ele volta a aparecer uma vez para todos.
6. **Nome do jogo:** ele cogitou trocar "Império" por outro nome na mesma linha (Dinastia, Legião, Reino…). Ainda não foi decidido.

---

## 9. Pasta `tools/`

- `patches/`: todos os scripts de alteração já aplicados, em ordem aproximada. São um bom exemplo de como cada recurso foi feito.
- `provas/`: recorte de PDF com texto (`x3_espcex.py`, `x3_ifsul.py`), montagem dos bancos (`build_*.py`) e classificador de temas (`cls_temas.py`). Dependências: PyMuPDF, Pillow.
- `resolucoes/`:
  - `esq.py`: diagramas SVG das resoluções de física;
  - `m2.py` e `mont.py`: montagens de imagens das questões, para ler em lote;
  - resoluções de matemática ainda não publicadas.
- `armaduras/`: desenho das armaduras novas (`novas_arm.js`, `natal_arm.js`) e `prancha.js` (gera a prancha de aprovação via Playwright).
