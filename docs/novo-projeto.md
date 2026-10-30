# Criador de edições interlineares — documento de partida

> Nome provisório da ferramenta: **`interlinear`**. Pode ser trocado na Fase 0.
> Este documento é a base comum entre o projeto no Claude.ai (decisões) e o Claude Code (construção).
> Toda decisão nova entra aqui ou no `CLAUDE.md` do repositório.

## 1. Objetivo
Um programa que **gera edições interlineares** de textos hebraicos e aramaicos (Chassidut, Chumash, Sidur,
Guemará…) como **sites estáticos**: cada trecho no original e, abaixo dele, uma ou mais traduções, com
abreviações explicadas, glossário, resumos, transliteração e áudio.

**O software não é o HTML.** O HTML é o produto que sai dele. O programa recebe uma fonte (PDF, Sefaria, doc…),
passa por etapas revisáveis e gera o site.

## 2. Princípios
1. **Etapas com arquivos intermediários.** Cada etapa grava um arquivo legível (YAML ou texto) que o Moises pode
   abrir, revisar e corrigir antes da etapa seguinte. Nada fica escondido na memória do programa.
2. **O texto-fonte revisado é sagrado.** Depois de aprovado, o original não muda. Toda saída é verificada
   letra a letra contra ele.
3. **Nada amarrado a um livro.** Títulos, capítulos, línguas, convenções e regras de divisão ficam em `livro.yaml`.
   O código não pode ter o nome de nenhum livro.
4. **Fontes trocáveis.** Cada tipo de fonte é um *importador* com a mesma interface de saída.
5. **Origem e licença registradas.** Cada texto e cada tradução importada guarda de onde veio e sob qual licença.
   O site mostra isso no rodapé automaticamente.
6. **Línguas configuráveis.** O padrão é he → en → pt-BR, mas a lista vem do livro.
7. **Script onde dá, IA onde é difícil, humano aprova.** Extrair, dividir, montar YAML, verificar e gerar são scripts
   determinísticos. A IA entra em traduzir, interpretar e resolver ambiguidades que os scripts apontam (abreviação
   com mais de um sentido, referência sem marcação, erro de OCR). Toda saída da IA passa pelo `verificar` antes de
   ser aceita, e cada item de camada tem `status: rascunho | revisado | aprovado`.

## 3. Teste de referência: refazer o site do Kuntres HaTefilah
O Kuntres já está pronto (tradução completa e revisada) e no ar em https://kuntres.netlify.app.
A ferramenta é considerada funcional quando **gerar esse mesmo site a partir dos mesmos dados**.

Material de referência, **somente leitura**, mantido pelo projeto do Claude.ai (não alterar):
`/mnt/c/Users/conta/Documents/dev/tefila-dev`
- `projeto/content/*.yaml`: conteúdo trilíngue (formato descrito no CLAUDE.md dessa pasta)
- `projeto/content/abreviacoes.yaml`, `glossario.yaml`, `resumo.html`
- `projeto/sections/secao-NN.txt`: texto-fonte revisado
- `projeto/build.py`, `assets/style.css`, `assets/app.js`: o gerador atual (é a referência visual e de comportamento)
- `projeto/tools/extrair.py`: extrator do PDF (fonte "Mirror" com tabela de letras própria)
- `fontes/*.pdf`: o PDF original (fica fora do git)

O que for necessário para os testes é copiado para `testes/referencia/kuntres/` (sem o PDF, que fica fora do git).
**A cópia é feita pelo Moises**, com o comando que está no `CLAUDE.md`: o Claude Code não roda nenhum comando de
terminal nessa pasta (bloqueado no `.claude/settings.json`) e só pode lê-la com a ferramenta Read.

**Dois níveis de teste:**
- **A — Geração:** importar os YAML do Kuntres → gerar o site → mesmas páginas, mesmos trechos (texto idêntico),
  mesmos recursos: toggles EN/PT, A−/A+, popup de abreviações, glossário, קיצור, notas, títulos, sumário e navegação.
  Comparação automática do texto extraído do HTML, mais conferência visual.
- **B — Pipeline:** PDF → texto extraído e dividido → igual, letra por letra, a `sections/secao-NN.txt`.

## 4. Arquitetura — etapas
```
fonte ──importar──▶ fonte.txt/blocos ──[revisão]──▶ estruturar ──▶ segmentar ──▶ anotar (abreviações, glossário)
      ──▶ traduzir ──▶ enriquecer (nikud, transliteração, áudio) ──▶ verificar ──▶ gerar site ──▶ publicar
```
| Etapa | Entrada | Saída | Observação |
|---|---|---|---|
| importar | PDF, Sefaria, docx, txt, html | `fonte/` com blocos de texto Unicode + `origem.yaml` (URL, versão, licença) | um importador por tipo de fonte |
| estruturar | fonte | capítulos/seções/resumos | regras (regex de marcadores) no `livro.yaml` |
| segmentar | capítulos | trechos curtos (`seg`) | automático pela pontuação, com ajuste manual |
| anotar | trechos | `abreviacoes.yaml`, `glossario.yaml` | detecta siglas (`X"Y`, `X'`) sem verbete |
| traduzir | trechos + glossário + convenções | campos de tradução por língua | ver §7 |
| enriquecer | trechos | camadas `vocalizado` (nq), `transliteracao` (tl) e `audio` | nikud já vem pronto em fontes como o Sefaria |
| verificar | tudo | relatório de erros e avisos | evolução do `verificar.py` do Kuntres |
| gerar | livro completo | `saida/site/` | templates Jinja2 + tema |
| publicar | site | Netlify | `netlify.toml` gerado por livro |

Comandos (CLI):
`interlinear novo <livro>` · `importar` · `estruturar` · `segmentar` · `anotar` · `traduzir` · `verificar` · `gerar` · `servir` (preview local) · `publicar`

## 5. Formato de um livro
Um livro é um **texto-base** (o original segmentado, com IDs estáveis) mais **camadas** (§5.1). Nada que seja
derivado do original (tradução, vocalização, transliteração, áudio) fica dentro da base.
```
livros/kuntres-hatefilah/
  livro.yaml            metadados, línguas, convenções, regras de divisão, perfis, tema
  origem.yaml           fonte(s), versão, licença
  fonte/                texto importado e revisado (a referência letra a letra)
  base/NN-*.yaml        original segmentado: id + type + he (intocável)
  camadas/*.yaml        traduções, vocalizado, transliteração, comentários, referências, áudio (ver §5.1)
  abreviacoes.yaml
  glossario.yaml
  paginas/              páginas livres (resumo didático etc.) em Markdown ou HTML
  audio/                (gerado)
```
Exemplo de `livro.yaml`:
```yaml
id: kuntres-hatefilah
titulo: {he: 'קונטרס התפלה', la: 'Kuntres HaTefilah', en: 'Tract on Prayer', pt: 'Opúsculo sobre a Oração'}
autor: 'Rabi Shalom DovBer Schneersohn, o Rebe Rashab'
data: 'Tevet 5660 (1899/1900)'
linguas: [he, en, pt-BR]
convencoes:
  nome_divino: {en: 'G-d', pt: 'D''us', tetragrama: 'Hashem'}
  transliteracao: moderna-br        # ou ashkenazi
estrutura:
  capitulo: {marcador: '^(?P<n>[א-ת]{1,2})\. ?', rotulo: 'Seção'}
  resumo: {marcador: 'קיצור:', rotulo: {he: 'קיצור', en: 'Summary', pt: 'Resumo'}}
tema: classico
```
Trecho do texto-base (`base/03-*.yaml`):
```yaml
- id: s03.004       # estável: camadas apontam para ele
  type: seg
  he: '...'         # original, intocável
```
A tradução, o vocalizado e a transliteração desse trecho ficam nas camadas, apontando para `s03.004`.

**Formato de entrada do importador do Kuntres (não é o formato do livro).** Os YAML atuais do Kuntres guardam tudo
no mesmo trecho:
```yaml
- type: seg
  he: '...'
  nq: '...'          # vocalizado
  tl: '...'          # transliteração
  tr: {en: '...', pt: '...'}
```
O importador `kuntres_yaml` lê isso e grava `base/` (id + type + he) e uma camada para cada campo derivado
(`traducao-en`, `traducao-pt`, `vocalizado`, `transliteracao`).

Os modelos são validados com **pydantic**. Erros de formato são apontados com o arquivo e a linha.

### 5.1 Camadas (decisão de arquitetura)
O livro **não fica amarrado a duas línguas**. Ele é formado por um **texto-base** (o original, com IDs estáveis
por trecho) mais um número livre de **camadas**, cada uma num arquivo YAML próprio:
```
livros/<livro>/
  base/NN-*.yaml              original segmentado: id + type + he (intocável)
  camadas/
    traducao-pt.yaml          tipo: linha
    traducao-en.yaml          tipo: linha
    vocalizado.yaml           tipo: linha   (nq: com nikud e abreviações por extenso)
    transliteracao.yaml       tipo: linha
    kavanot-<autor>.yaml      tipo: comentario
    referencias.yaml          tipo: referencia
```
Cabeçalho de cada camada:
```yaml
camada: kavanot-siddur-rav
tipo: comentario              # linha | comentario | nota | referencia | audio
lingua: pt-BR
titulo: {pt: 'Kavanot', en: 'Kavanot'}
autor: '...'
origem: {fonte: '...', licenca: '...'}
itens:
  - alvo: s03.004             # um trecho
    texto: '...'
  - alvo: s03.004-s03.009     # ou um intervalo de trechos
    texto: '...'
```
Referências são **dados estruturados** (padrão de referência do Sefaria, ex.: `Psalms 145:1`), não texto livre.
O gerador cria o link, traduz o nome do livro e pode mostrar o versículo num popup.

Tipos e exibição:
- **linha**: aparece embaixo do original (tradução, vocalizado, transliteração).
- **comentario**: bloco recolhível ligado a um trecho ou intervalo (Kavaná, explicação).
- **nota / referencia**: marcador com popup (como as abreviações do Kuntres).
- **audio**: ▶ no trecho.

O formato antigo do Kuntres (tudo no mesmo seg) é convertido pelo importador em base + camadas de linha (ver §5).

### 5.2 Perfis de leitura
- O número de **linhas** visíveis ao mesmo tempo tem limite, padrão **2** e configurável no `livro.yaml`.
  As demais camadas continuam acessíveis como comentário ou popup.
- **Perfis** pré-definidos por livro escolhem quais camadas ficam ligadas e como:
```yaml
perfis:
  iniciante:     {linhas: [transliteracao, traducao-pt], comentarios: abertos, abreviacoes: por-extenso}
  intermediario: {linhas: [traducao-pt], audio: true, comentarios: recolhidos}
  avancado:      {linhas: [], popups: [traducao-pt, referencias], comentarios: recolhidos}
```
- O leitor escolhe um perfil na primeira visita e pode ajustar camada por camada. A escolha fica no navegador.

**Princípio:** o gerador de site só *exibe* camadas. A inteligência está nas etapas que *criam* as camadas
(importar, traduzir, vocalizar, transliterar, achar referências, importar comentários).

## 6. Importadores (ordem de prioridade)
1. **YAML do Kuntres**: para o teste A. Converte o formato atual para o formato novo.
2. **Sefaria**: API aberta, texto em Unicode, frequentemente com nikud (o Chumash vem até com te'amim),
   traduções inglesas e comentários ligados por referência. Escolher a versão do texto e registrar a licença
   (ex.: a tradução do Steinsaltz na William Davidson Edition é CC BY-NC). Conteúdo disponível, entre outros:
   Chumash completo; Siddur Ashkenaz, Sefard, Edot HaMizrach, Koren; **Weekday Siddur Chabad** (só dias de semana);
   Talmud Bavli completo. Conferir os endpoints atuais na documentação da API antes de implementar.
3. **PDF com texto Unicode** (pdfplumber), tratando a ordem RTL.
4. **PDF com fonte codificada**: tabela de mapeamento por fonte em arquivo de configuração (a do Kuntres é a "Mirror").
5. **docx / txt**.
6. **HTML de sites**: regras por site.
7. **PDF escaneado (OCR)**: por último. OCR de hebraico rabínico exige revisão pesada.

Fica de fora: NotebookLM como fonte (o conteúdo dele vem de outras fontes e é gerado por IA). Fica como ideia para a
**saída**: subir o livro pronto num notebook para os alunos estudarem.

## 7. Tradução
- **Modo assistido (começar por este):** o programa prepara um lote (capítulo + glossário + convenções + exemplos de
  trechos já aprovados), o Claude Code traduz escrevendo no YAML, e o `verificar` confere.
- **Modo API (depois):** a mesma coisa, chamando a API da Anthropic. É pago por uso, então precisa de estimativa de custo antes de rodar.
- Traduções existentes (ex.: inglês do Sefaria) podem entrar como **referência** ou como **coluna**, com crédito e licença.
- Regras herdadas do Kuntres: tradução fiel e fluente; complementos entre [colchetes]; referências entre parênteses;
  terminologia fixa do glossário; o original nunca é alterado.

## 8. Saída (site)
- Templates **Jinja2** e um tema padrão derivado do Kuntres (`style.css`/`app.js`), com tipografia
  Frank Ruhl Libre / Literata / IBM Plex Sans.
- Recursos: liga/desliga por língua, tamanho da letra, popup de abreviações, glossário, sumário, navegação
  anterior/próxima, resumos, notas, linha de transliteração (TL) e ▶ de áudio quando houver.
- Mobile primeiro, RTL correto, acessível (teclado, aria), sem dependências externas além das fontes.
- Página de créditos e licenças gerada automaticamente.

## 9. Stack
Python 3.12 · venv (ou uv) · **typer** (CLI) · **pydantic** · **jinja2** · **ruamel.yaml** (preserva comentários e
formatação ao regravar) · pdfplumber · httpx · **pytest**. Sempre UTF-8.

```
interlinear/
  CLAUDE.md
  pyproject.toml
  src/interlinear/
    cli.py
    modelo.py            pydantic: Livro, Capitulo, Trecho, Abreviacao, Termo
    importadores/        kuntres_yaml.py, sefaria.py, pdf_texto.py, pdf_mapeado.py, docx.py ...
    etapas/              estruturar.py, segmentar.py, anotar.py, traduzir.py, enriquecer.py, verificar.py
    gerador/             gerar.py, templates/, temas/classico/{style.css, app.js}
  livros/                (os livros de trabalho; cada um pode virar repositório próprio no futuro)
  testes/
    referencia/kuntres/  cópia dos dados do Kuntres para os testes A e B
```

## 10. Fases
- **Fase 0 — Esqueleto:** repositório no WSL (`~/dev/interlinear`), `pyproject.toml`, CLI vazia, pytest rodando,
  `CLAUDE.md`, git e GitHub (público, `mnisenbaum/interlinear`).
- **Fase 1 — Modelo + gerador:** modelos pydantic, importador "YAML do Kuntres" e gerador Jinja2.
  **Meta: o teste A passa**, gerando o site do Kuntres equivalente ao atual.
  Saída: `saida/site/` + `saida/<livro>.zip`, pronto para arrastar no Netlify (deploy automático fica para a Fase 7).
- **Fase 2 — Verificar, abreviações e glossário genéricos:** portar o `verificar.py` (termos vindos do glossário, não do código).
- **Fase 3 — Importador PDF** (Unicode e mapeado) + estruturar: **meta: o teste B passa**.
- **Fase 4 — Importador Sefaria + segmentação:** piloto pequeno, por exemplo Bereshit 1, ou Modeh Ani e o Shemá do sidur.
- **Fase 5 — Tradução assistida** em lote, de ponta a ponta no piloto. Depois, o modo API.
- **Fase 6 — Enriquecer:** camada vocalizada (`nq`), transliteração por tabela (moderna-br / ashkenazi) e áudio (navegador → TTS de nuvem).
- **Fase 6b — Novas camadas:** comentários (Kavanot), referências estruturadas com popup do Sefaria e perfis de leitura completos.
  O *modelo* de camadas e perfis já nasce na Fase 1; só os tipos novos ficam para esta fase.
- **Fase 7 — Publicar:** `netlify.toml` por livro, deploy automático; empacotar como skill/plugin do Claude Code.

## 11. Decisões em aberto
- Nome definitivo da ferramenta.
- Pronúncia padrão da transliteração e do áudio (moderna × ashkenazi de Chabad × as duas).
- Abreviações na transliteração e no áudio: ler por extenso (sugestão) × soletrar.
- Livros num repositório só (`livros/`) ou um repositório por livro (o que facilita um site Netlify por livro).
- Primeiro texto do Sefaria para o piloto.
- Licença das traduções próprias do projeto (ex.: CC BY-SA) e como exibi-la no rodapé.

## 12. Registro de decisões
- **2026-10-30** — A base guarda só `id`, `type` e `he`. Vocalizado (`nq`), transliteração (`tl`) e traduções são
  camadas. O formato "tudo no mesmo seg" existe apenas como entrada do importador do Kuntres.
- **2026-10-30** — O tefila-dev é protegido também contra comandos de terminal (`deny` no `.claude/settings.json`).
  A cópia para `testes/referencia/kuntres/` é feita pelo Moises.
- **2026-10-30** — A fonte da verdade é o repositório no WSL. A pasta `C:\Users\conta\Documents\dev\interlinear`
  é um espelho dos docs, atualizado pelo Claude Code no fim de cada sessão.
- **2026-10-30** — Princípio 7: script onde dá, IA onde é difícil, humano aprova. Itens de camada têm `status`.
- **2026-10-30** — A primeira saída é `saida/<livro>.zip` para arrastar no Netlify; deploy automático só na Fase 7.
- **2026-10-30** — Python 3.12 instalado em ~/.local/bin (via uv); o 3.14 do sistema não tem venv sem python3-venv. Se a .venv quebrar, recriar com: python3.12 -m venv .venv && pip install -e '.[dev]'
