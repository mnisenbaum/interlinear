# interlinear — criador de edições interlineares

Ferramenta em Python que **gera** edições interlineares de textos hebraicos e aramaicos (Chassidut, Chumash,
Sidur, Guemará…) como sites estáticos. **O software não é o HTML: o HTML é o produto que sai dele.**

O documento de referência é **`docs/novo-projeto.md`**: objetivo, arquitetura, formato de livro, camadas, perfis e fases.
Leia-o antes de qualquer tarefa nova.

## Com quem você trabalha
- **Moises**, educador (redes, automação Python, física) e coordenador de uma yeshivá. Fale em **português do Brasil**.
- Ele está **aprendendo vibe coding** enquanto constrói. O mentor dele é o Claude no app claude.ai, num projeto
  separado. Moises leva e traz informação entre os dois. Por isso:
  1. **Explique o que vai fazer antes de fazer**, em poucas linhas e sem jargão desnecessário. Quando usar um conceito
     novo (pydantic, fixture, Jinja2, venv…), diga numa frase o que ele é e por que está sendo usado.
  2. **Passos pequenos e verificáveis.** Uma fase de cada vez, com commits pequenos e mensagens claras em português.
  3. **No fim de cada sessão**, acrescente uma entrada em `docs/DIARIO.md` no formato descrito em
     `docs/COMO-TRABALHAMOS.md` (o "relatório de passagem"). É o que o Moises leva para o claude.ai.
     Depois, atualize o espelho dos docs na pasta do Windows (ela é só cópia; **a fonte da verdade é este repositório**):
     `cp CLAUDE.md docs/*.md /mnt/c/Users/conta/Documents/dev/interlinear/`
  4. Se uma decisão de arquitetura não estiver em `docs/novo-projeto.md`, **pergunte** em vez de decidir sozinho,
     e depois registre a decisão no documento.
  5. Se um texto ditado pelo mentor ou pelo Moises estiver tecnicamente errado, teste a versão correta, aplique-a e
     registre a diferença no relatório. Decisões de arquitetura continuam exigindo pergunta (item 4).

## Regras do projeto
- **Nada amarrado a um livro.** Nenhum nome de livro, título de capítulo ou língua fixa no código; isso tudo fica em `livros/<id>/livro.yaml`.
- **Texto-base intocável.** Depois de revisado, o original não muda; toda saída é verificada letra a letra contra ele.
- **Camadas** (tradução, vocalizado, transliteração, comentário, referência, áudio) ficam em arquivos próprios,
  ligados ao texto-base por IDs estáveis (ver §5 e §5.1 do documento). A base guarda só `id`, `type` e `he`.
- Sempre UTF-8. Hebraico em YAML usa aspas simples, com o apóstrofo duplicado (`'בחי'''`).
- Todo arquivo de livro passa por validação pydantic. Escreva testes (pytest) junto com o código.

## Material de referência — somente leitura
O site do Kuntres HaTefilah (https://kuntres.netlify.app) é o **teste de referência** (§3 do documento).
Os dados ficam em `/mnt/c/Users/conta/Documents/dev/tefila-dev`, uma pasta mantida por outro projeto.
**Nunca altere nada lá.** Leia só com a ferramenta Read: comandos de terminal nessa pasta estão bloqueados no
`.claude/settings.json`. A cópia para `testes/referencia/kuntres/` é feita **pelo Moises**; quando precisar dela,
peça que ele rode (sem o PDF, que não vai para o git):
```bash
rsync -a --exclude='*.pdf' /mnt/c/Users/conta/Documents/dev/tefila-dev/projeto/ testes/referencia/kuntres/
```

## Comandos
```bash
source .venv/bin/activate   # ativa a venv do projeto (uma vez por terminal)
pytest                      # roda os testes
interlinear --help
interlinear --version
```
Se a `.venv` quebrar, recriar com:
```bash
python3.12 -m venv --clear .venv && source .venv/bin/activate && pip install -e '.[dev]'
```
