# Claude Code - VITE

Leia `AGENTS.md` primeiro. Para tarefas complexas, use `/confidence-check` primeiro e depois escolha a skill adequada em `.agents/skillset.md`.

## Uso recomendado

- Use subagents para revisao, pesquisa, testes ou auditoria quando a tarefa for grande.
- Mantenha contexto curto: leia arquivos especificos, nao o projeto inteiro.
- Antes de editar UI, identifique componentes, estilos e padroes ja existentes.
- Antes de terminar, rode os comandos disponiveis de lint, test ou build.

## Prompt inicial sugerido

`Leia AGENTS.md e .agents/skillset.md. Depois implemente a tarefa seguindo as regras do workspace.`
