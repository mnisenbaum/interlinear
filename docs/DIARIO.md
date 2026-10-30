# Diário do projeto

Uma entrada por sessão de trabalho no Claude Code, no formato do "relatório de passagem" (ver `COMO-TRABALHAMOS.md`).
A entrada mais recente fica no topo.

## 2026-10-30 — Comando de recuperação da venv corrigido e regra 5
**Fase:** 0 — Esqueleto
**O que foi feito:** a §12 do `novo-projeto.md` e o `CLAUDE.md` agora têm só a forma com `--clear` do comando de
recuperação, sem o aviso. O `CLAUDE.md` ganhou a regra 5 em "Com quem você trabalha", com o texto ditado pelo Moises.
**Arquivos principais:** `CLAUDE.md` — seção "Comandos" e regra 5; `docs/novo-projeto.md` — §12.
**Conceitos novos que apareceram:** nenhum.
**Decisões tomadas:**
- Resolve a pendência da entrada anterior: fica só a forma com `--clear`, decisão do Moises, registrada na §12.
- Regra 5: texto ditado tecnicamente errado é testado, corrigido e relatado aqui; decisão de arquitetura continua exigindo
  pergunta. Registrada no `CLAUDE.md`.
- Diferença em relação ao texto ditado: a §12 trocou `python3.12 -m venv .venv && pip install -e '.[dev]'` por
  `python3.12 -m venv --clear .venv && source .venv/bin/activate && pip install -e '.[dev]'`. A entrada anterior ficou
  como estava, como histórico.
**Dúvidas / pontos para o mentor:** nenhuma nova.
**Testes:** `pytest` — `1 passed`. Comando de recuperação copiado do `CLAUDE.md` e rodado em cópia descartável do projeto:
funcionou sem `.venv` e com `.venv` quebrada (`interlinear --version` e `pytest` ok).
**Próximo passo sugerido:** começar a Fase 1. Para o teste A, o Moises precisa rodar o `rsync` que está no `CLAUDE.md`.

## 2026-10-30 — Fase 0: esqueleto do projeto, CLI e primeiro teste
**Fase:** 0 — Esqueleto
**O que foi feito:** criamos o `pyproject.toml` e o pacote em `src/interlinear/`, com Python >= 3.12 e as dependências
da §9 (sem pdfplumber e httpx, como combinado). A venv comum fica em `.venv`, sem usar comandos do uv. A CLI só responde
`--help` e `--version`, e um teste pytest confere o `--version`. A seção "Comandos" do `CLAUDE.md` foi preenchida.
Modelos, importadores e gerador continuam fora: são a Fase 1.
**Arquivos principais:**
- `pyproject.toml` — ficha do projeto: nome, versão, dependências e o comando `interlinear`.
- `src/interlinear/__init__.py` — lê a versão do pacote instalado.
- `src/interlinear/cli.py` — a linha de comando.
- `testes/test_cli.py` — compara a saída de `--version` com a versão do `pyproject.toml`.
**Conceitos novos que apareceram:**
- `pyproject.toml` — arquivo padrão que descreve um projeto Python e como instalá-lo.
- venv — um Python isolado por projeto; os pacotes instalados nele não afetam o resto do sistema.
- `pip install -e` — instalação "editável": o pacote aponta para o código da pasta, e as edições valem na hora.
- `[project.scripts]` — liga o comando de terminal `interlinear` a uma função Python; só passa a valer depois de instalar.
- typer — biblioteca que transforma funções Python em comandos de terminal e gera o `--help` sozinha.
- `CliRunner` — ferramenta do typer que "digita" um comando dentro do teste e captura o que ele respondeu.
- `venv --clear` — esvazia a pasta da venv antes de recriá-la.
**Decisões tomadas:**
- Python 3.12 de `~/.local/bin`: registrado na §12 do `novo-projeto.md`, com o texto ditado pelo Moises.
- Decisões miúdas de implementação, que não mudam a arquitetura e não estão na §12: setuptools para empacotar;
  autocompletar do typer desligado (a Fase 0 pede só `--help` e `--version`); versão escrita só no `pyproject.toml`.
**Dúvidas / pontos para o mentor:**
- **O comando de recuperação registrado não funciona como está.** `python3.12 -m venv .venv && pip install -e '.[dev]'`
  falha com `pip: command not found` (exit 127): `&&` não ativa a venv e não existe `pip` fora dela. Mesmo ativando antes
  do `pip`, o `venv` dá erro se a `.venv` estiver quebrada. A §12 guarda o texto ditado; o `CLAUDE.md` tem o mesmo comando
  e, logo abaixo, um aviso com a forma que funcionou:
  `python3.12 -m venv --clear .venv && source .venv/bin/activate && pip install -e '.[dev]'`.
  Falta decidir se a §12 e o `CLAUDE.md` passam a ter só essa forma.
- O 3.12 vem de uma instalação gerenciada pelo uv (`~/.local/share/uv/python/`). Pelo que se deduz da instalação, não
  testado: se o uv removê-lo ou atualizá-lo, a `.venv` pode quebrar, e é aí que o comando de recuperação entra.
- Consequência do teste, também deduzida: a versão lida vem do pacote instalado. Quem mudar a versão no `pyproject.toml`
  precisa rodar `pip install -e` de novo, ou o teste falha.
- Continuam abertos, da sessão anterior: o teste do `deny` de `Edit` e a escolha do modo de permissão.
**Testes:**
- `pytest` — `1 passed`.
- Teste do teste: com a CLI quebrada de propósito, `1 failed`; restaurada, `1 passed`.
- `interlinear --version` — `interlinear 0.1.0`, exit 0. `interlinear --help` — mostra só `--version` e `--help`, exit 0.
- Recuperação da venv, em cópia descartável do projeto: comando registrado sem `.venv` — falhou (exit 127). Com `--clear`,
  sem `.venv` e com `.venv` quebrada — funcionou nos dois casos (`--version` e `pytest` ok; testado com `pip install -q`).
- Variante só com `source` antes do `pip`: funcionou sem `.venv`, falhou com `.venv` quebrada.
**Próximo passo sugerido:** decidir o texto final do comando de recuperação e começar a Fase 1 (modelos pydantic,
importador do Kuntres e gerador). Para o teste A, o Moises precisa rodar o `rsync` que está no `CLAUDE.md`.

## 2026-10-30 — Proteção da pasta de referência e repositório no GitHub
**Fase:** pré-Fase 0
**O que foi feito:** testamos a proteção do tefila-dev: o bloqueio de comandos de terminal (`Bash(*tefila-dev*)`)
funciona; a regra de `Edit` **não foi testada**. Corrigimos o `.claude/settings.json`: os caminhos do tefila-dev agora
são absolutos, com `//` no início, e a regra `Write` saiu. Descobrimos que a sessão estava no **modo Auto**. Por fim,
rodamos um teste de permissões (`git status` e `whoami`) e criamos o repositório público
https://github.com/mnisenbaum/interlinear (branch `main`, ligado como `origin`).
**Arquivos principais:** `.claude/settings.json` — regras de permissão do Claude Code; `docs/DIARIO.md` — este relatório.
**Conceitos novos que apareceram:**
- modo Auto — modo de permissão em que o Claude Code executa ações sem pedir aprovação a cada passo.
- `//` em regras de permissão — indica caminho absoluto, a partir da raiz do sistema; um único `/` é lido como relativo
  ao projeto.
- `allow` e `deny` — listas do `settings.json` com o que pode rodar sem perguntar e o que fica sempre bloqueado.
**Decisões tomadas:** corrigir as regras do `settings.json`, o que não muda a arquitetura. A proteção em si já estava
registrada na §12 do `novo-projeto.md`, e o texto de lá continua correto.
**Dúvidas / pontos para o mentor:**
- O teste do `whoami` só se conclui com o que apareceu na tela do Moises. O comando não está no `allow`, então, fora do
  modo Auto, deveria ter pedido aprovação. O Claude Code vê o resultado, mas não vê se houve pedido.
- O `deny` de `Edit` continua sem teste. Até lá, a proteção contra escrita nessa pasta é uma expectativa, não um fato
  verificado. Vale decidir como testar sem arriscar a pasta, por exemplo com uma regra igual apontando para uma pasta
  descartável.
- A regra `Bash(*tefila-dev*)` compara o texto do comando. Ela bloqueia até uma mensagem de commit que cite o nome, e
  não pegaria um comando que chegasse à pasta sem escrever o nome inteiro (por exemplo, com curinga ou variável). Isso é
  uma dedução da regra, não foi testado.
- Faltou definir em qual modo de permissão queremos trabalhar na Fase 0.
- Origem das informações: o teste do bloqueio, o motivo da correção e o modo Auto vêm do resumo do Moises no prompt de
  fechamento. O conteúdo do `settings.json` e os dados do repositório foram conferidos direto no git e no GitHub.
**Testes:** sem pytest (ainda não há código).
- `git status` — rodou: `main` em dia com `origin/main`, nada a commitar.
- `whoami` — rodou e respondeu `conta`.
- `Bash(*tefila-dev*)` — bloqueou (relato do Moises).
- `deny` de `Edit` — não testado.
**Próximo passo sugerido:** confirmar o resultado do teste do `whoami`, decidir o modo de permissão e começar a Fase 0.

## 2026-10-30 — Correções antes da Fase 0 (feitas no claude.ai)
**Fase:** pré-Fase 0
**O que foi feito:** revisão dos documentos com o mentor e pacote inicial refeito.
**Arquivos principais:** `docs/novo-projeto.md` — §5 reescrita (base + camadas), princípio 7, zip na Fase 1, §12
"Registro de decisões"; `CLAUDE.md` — tefila-dev só por Read, cópia feita pelo Moises, espelho dos docs no fim da
sessão; `.claude/settings.json` — `deny` de Bash para o tefila-dev.
**Decisões tomadas:** registradas na §12 do `novo-projeto.md`.
**Dúvidas / pontos para o mentor:** confirmar se a regra `Bash(*tefila-dev*)` é aceita pela versão do Claude Code.
**Testes:** nenhum (ainda não há código).
**Próximo passo sugerido:** testar a proteção do tefila-dev e começar a Fase 0.

## 2026-10-30 — Ponto de partida
**Fase:** pré-Fase 0
**O que foi feito:** projeto concebido no claude.ai a partir da experiência do Kuntres HaTefilah (site interlinear
he/en/pt já pronto). Definidos: arquitetura em etapas, formato de livro, camadas, perfis de leitura, importadores
(Sefaria e PDF primeiro) e o Kuntres como teste de referência.
**Arquivos principais:** `docs/novo-projeto.md` — especificação; `CLAUDE.md` — regras para o Claude Code;
`docs/COMO-TRABALHAMOS.md` — o ciclo entre claude.ai e Claude Code.
**Decisões tomadas:** repositório público `mnisenbaum/interlinear`; código no WSL (`~/dev/interlinear`);
documentos de apoio também em `C:\Users\conta\Documents\dev\interlinear`.
**Próximo passo sugerido:** Fase 0 (esqueleto do projeto, venv, pytest, git e GitHub).
