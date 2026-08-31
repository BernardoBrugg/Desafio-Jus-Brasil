# Desafio Caça-Alucinações (BRACIS 2026 / Jusbrasil)

Pipeline determinístico para extração, normalização e resolução canônica de citações jurídicas em documentos processuais.

## Estrutura do Projeto

- `src/core/`: Configurações centralizadas e tratamento de exceções.
- `src/schemas/`: Modelos Pydantic para validação dos dados de entrada e saída.
- `src/repositories/`: Camada de acesso à base SQLite (`desafio1_bracis.db`) e aos arquivos de texto.
- `src/services/`: Serviços de extração de spans, normalização de ruídos OCR, resolução canônica e avaliação de métricas.
- `src/cli/`: Entry points para execução em lote e benchmark local.
- `scripts/`: Conversores para geração do `submission.csv` e empacotamento do `submission.zip`.
- `tests/`: Suíte de testes unitários e de integração.

## Instalação e Configuração

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Execução

### 1. Processamento em Lote

Gera um arquivo JSON por documento no diretório de saída:

```bash
python src/cli/run_pipeline.py --input /caminho/para/txt --output ./output
```

Ou usando o Makefile:

```bash
make run
```

### 2. Benchmark Local

Calcula as métricas de IoU, precisão, recall, F1 e acurácia de resolução contra o gabarito oficial:

```bash
make benchmark
```

### 3. Gerar Submissão

Gera o arquivo `submission.csv` e empacota o `submission.zip` para o leaderboard:

```bash
make submission
```

### 4. Execução via Docker

```bash
make docker-build
docker run --rm -v /caminho/para/in:/data/in -v /caminho/para/out:/data/out caca-alucinacoes-bracis --input /data/in --output /data/out
```

### 5. Testes

```bash
make test
```
