# Diário do projeto

Uma entrada por sessão de trabalho no Claude Code, no formato do "relatório de passagem" (ver `COMO-TRABALHAMOS.md`).
A entrada mais recente fica no topo.

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
