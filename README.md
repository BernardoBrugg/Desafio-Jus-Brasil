# Caça-Alucinações — Desafio BRACIS 2026

Pipeline modular de extração, normalização e resolução canônica de citações jurídicas para detecção de alucinações em peças processuais.

## Arquitetura em Camadas (FastAPI Style)

O projeto adota separação estrita de responsabilidades em camadas desacopladas:

- `src/core/`: Configurações centralizadas via variáveis de ambiente e exceções de domínio.
- `src/schemas/`: Modelos Pydantic para validação de entrada, saída, citações e métricas de avaliação.
- `src/repositories/`: Camada de acesso a dados (SQLite `desafio1_bracis.db`, `.txt` e `goldenset.xlsx`).
- `src/services/`: Serviços de negócio puros:
  - `ExtractionService`: Extração de spans candidatos e filtro de distratores de cabeçalho.
  - `NormalizationService`: Tratamento de ruídos OCR, abreviações e formatação canônica de identificadores.
  - `NormativeMatcher`: Mapeamento determinístico dos 18 registros normativos (súmulas e leis).
  - `ResolutionService`: Resolução determinística contra o banco e atribuição de classes (`real`, `inventada`, `incompleta`).
  - `PipelineService`: Orquestrador ponta a ponta por documento.
  - `EvaluationService`: Avaliador local de métricas (IoU $\ge$ 0.5, acurácia de classificação e resolução).
- `src/cli/`: Entry points de linha de comando para processamento em lote e benchmarking.
- `scripts/`: Conversores e empacotadores de submissão (`json_to_submission.py` e `package_submission.py`).
- `tests/`: Suíte automatizada de testes unitários.

## Regras Estruturais do Código

- Código 100% livre de comentários internos.
- Arquivos com limite estrito de no máximo 200 linhas (o maior arquivo possui 132 linhas).
- Cada diretório possui seu próprio arquivo `docs.md` detalhando responsabilidade e fluxo de dados.
- Sem dependências de APIs proprietárias ou conexão de rede em runtime.

## Instruções de Execução

### 1. Configuração do Ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
cp .env.example .env
```

### 2. Executar a Suíte de Testes

```bash
make test
```

### 3. Processar Documentos em Lote

Gera um arquivo JSON por documento na pasta `./output`:

```bash
make run
```

### 4. Executar o Benchmark Local contra o Gabarito

Calcula precisão, recall, F1 e acurácia de classificação/resolução:

```bash
make benchmark
```

### 5. Gerar Pacote de Submissão

Gera `submission.csv` e `submission.zip` prontos para upload no leaderboard:

```bash
make submission
```

### 6. Execução via Docker (Contrato Oficial)

```bash
make docker-build
docker run --rm -v /caminho/para/in:/data/in -v /caminho/para/out:/data/out caca-alucinacoes-bracis --input /data/in --output /data/out
```
