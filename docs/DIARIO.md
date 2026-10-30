# Diário do projeto

Uma entrada por sessão de trabalho no Claude Code, no formato do "relatório de passagem" (ver `COMO-TRABALHAMOS.md`).
A entrada mais recente fica no topo.

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
