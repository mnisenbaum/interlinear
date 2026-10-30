# Como trabalhamos — vibe coding em dupla

Dois lugares, dois papéis:

| | **claude.ai** (projeto "Criador de edições interlineares") | **Claude Code** (VS Code, WSL `~/dev/interlinear`) |
|---|---|---|
| Papel | mentor: explica, discute, decide, revisa | construtor: escreve código, testa, faz commits |
| O que entra | relatórios de passagem, dúvidas, trechos de código para entender | prompts preparados no claude.ai, decisões tomadas |
| O que sai | decisões, prompts para o Claude Code, explicações | código, testes e uma entrada no `docs/DIARIO.md` |

A **fonte única da verdade é o repositório**: `docs/novo-projeto.md` (o que queremos), `CLAUDE.md` (como trabalhar)
e `docs/DIARIO.md` (o que aconteceu). O que for decidido no claude.ai precisa virar texto nesses arquivos;
caso contrário, o Claude Code não fica sabendo.

## O ciclo
1. **claude.ai** — escolher o próximo passo e montar o prompt para o Claude Code. Entender antes o que vai acontecer.
2. **Claude Code** — colar o prompt, acompanhar e aprovar os diffs. Na dúvida, perguntar ao próprio Claude Code "por quê?".
3. **Claude Code** — no fim, pedir o relatório de passagem (ele grava no `DIARIO.md`).
4. **claude.ai** — colar o relatório. Discutir o que foi feito, o que não ficou claro e o que vem a seguir. Voltar ao 1.

## Relatório de passagem (formato de cada entrada do DIARIO.md)
```markdown
## AAAA-MM-DD — <título curto>
**Fase:** N — <nome>
**O que foi feito:** 3 a 6 linhas
**Arquivos principais:** caminho — para que serve
**Conceitos novos que apareceram:** termo — explicação em uma linha
**Decisões tomadas:** (e se já foram registradas em novo-projeto.md)
**Dúvidas / pontos para o mentor:**
**Testes:** comando e resultado
**Próximo passo sugerido:**
```

## Prompts úteis no Claude Code
- "Leia o CLAUDE.md e o docs/novo-projeto.md e execute a Fase N. Antes de começar, me explique o plano em até 10 linhas."
- "Pare aqui e me explique este arquivo como se eu estivesse aprendendo."
- "Escreva o relatório de passagem desta sessão no docs/DIARIO.md."
- "Rode os testes e me mostre o que falhou antes de corrigir."
