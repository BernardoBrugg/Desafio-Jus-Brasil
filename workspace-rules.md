# Regras de Workspace

- Leia `AGENTS.md` antes de qualquer tarefa.
- Use `/using-superpowers` no inicio de tarefas relevantes.
- Use a skill especifica quando o usuario chamar `/nome-da-skill`.
- Nao sobrescreva trabalho do usuario.
- Nao rode comandos destrutivos sem confirmacao.
- Leia arquivos antes de editar.
- Prefira mudancas pequenas, testaveis e alinhadas ao padrao local.
- Rode testes, lint ou build quando existirem.
- Ao finalizar, diga o que mudou, o que foi testado e riscos restantes.

## Regras Globais da Equipe (OBRIGATÓRIO)

1. **Zero Tolerância para Comentários no Código**: O código gerado NÃO DEVE conter comentários de nenhum tipo (inline, blocos, docstrings, etc.). O código deve ser limpo e auto-explicativo. Remova ativamente comentários existentes ao refatorar.
2. **Arquitetura Altamente Modular**: Evite arquivos/funções monolíticas. Divida o código em partes menores com responsabilidade única. Separe claramente as camadas do projeto.
3. **Documentação via Markdown (.md)**: Todo diretório (módulo ou feature) DEVE conter um arquivo `README.md` explicando sua responsabilidade principal, arquitetura interna e exemplos de uso. Sempre que criar uma pasta, crie seu README.md.
4. **Segurança e Gerenciamento de Configuração**: NUNCA faça hardcode de segredos (API keys, senhas, URLs base). Tudo deve vir de variáveis de ambiente (`.env`).

