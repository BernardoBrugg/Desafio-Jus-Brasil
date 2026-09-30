# Desafio Caça-Alucinações (BRACIS 2026 × Jusbrasil)

Solução determinística de alta performance para detecção, extração, classificação e resolução canônica de citações jurídicas em documentos processuais.

---

## 1. Abordagem Técnica

A solução foi projetada sob uma arquitetura modular e determinística, eliminando dependências de modelos de linguagem pesados, alucinações de inferência e variações de amostragem estocástica. O pipeline executa em poucos segundos e opera de forma 100% offline.

### 1.1 Extração de Spans e Filtragem de Distratores
- **Expressões Regulares Especializadas**: Cobertura abrangente de formatos processuais brasileiros, contemplando padrões complexos de recursos encadeados (ex.: `ED no AgR no AREspEl`, `AgInt no AREsp`, `AgRg no REsp`), súmulas (vinculantes e comuns dos tribunais superiores STF, STJ, TST, TSE, STM), temas de repercussão geral e dispositivos de legislação (`CPC`, `CC`, `CLT`, `CF/88`, `CPP`, etc.).
- **Filtragem de Distratores**: Remoção precisa de cabeçalhos de petição, números de autuação do próprio processo e narrativas históricas que não caracterizam citações a precedentes externos.
- **Resolução de Sobreposição**: Algoritmo determinístico baseado em prioridade de escopo que preserva a maior entidade jurídica identificada quando ocorrem sobreposições de padrões.

### 1.2 Normalização de Ruídos de OCR
- Correção de trocas de caracteres decorrentes de OCR em peças digitalizadas (ex.: `5úmula` para `Súmula`, `profcrido` para `proferido`, confusão entre `l`/`I`/`1` em identificadores de classe recursal como `AREspEl`).
- Extração e unificação de sequências numéricas e máscaras de processo CNJ.

### 1.3 Resolução Canônica Indexada em SQLite
A camada de persistência indexa a base relacional (`desafio1_bracis.db`) em estruturas em memória com ordenação e hierarquia:
1. **Prioridade de Cabeçalho / Ementa**: O número CNJ padronizado (20 dígitos) é mapeado prioritariamente ao acórdão que formalmente julga aquele processo (`recs[0]`), evitando associações indevidas a decisões que apenas citam o precedente no corpo do texto.
2. **Resolução por Número Sequencial e Desambiguação**: Para citações sem formato CNJ completo, a correspondência é validada considerando tribunal de origem e classe recursal.
3. **Casamento Normativo**: Dispositivos de legislação e súmulas são resolvidos diretamente aos registros canônicos correspondentes por tipo e numeração.

### 1.4 Classificação Tripartite Rigorosa
- **`real`**: Citação cujos identificadores formais apontam de forma unívoca a um acórdão, dispositivo legal ou súmula existente na base canônica fornecida.
- **`inventada`**: Citação completa que traz identificadores formais específicos (tribunal, número de processo, classe recursal), mas cuja existência não é confirmada na base canônica.
- **`incompleta`**: Citação que remete a uma decisão concreta com contexto identificador (relator, ano, classe, tribunal), mas cujos elementos fornecidos são insuficientes para individualizar um registro único na base canônica (em estrita conformidade com o critério oficial do desafio).

### 1.5 Calibração de Confiança e Brier Score
Em razão da natureza determinística e da validação cruzada exaustiva sobre a base canônica, o pipeline calibra a probabilidade em `1.0000` para predições confirmadas, maximizando o termo de bônus na métrica oficial do desafio:
$$\text{Score} = \text{Score}_{\text{base}} + 0.1 \times (1 - \text{Brier})$$

---

## 2. Requisitos de Ambiente

- **Python**: 3.12+
- **Docker**: Qualquer versão padrão com suporte a `docker build` e `docker run`
- **Hardware**: Roda com folga em CPU padrão (tempo total de execução < 5 segundos para 26 documentos; consumo de memória RAM < 100 MB). Não requer GPU.
- **Execução Offline**: Nenhuma chamada de rede, API externa ou download de pesos em runtime.

---

## 3. Estrutura do Repositório

```text
├── Dockerfile                  # Definição do container para execução limpa
├── .dockerignore               # Otimização de contexto para build do container
├── Makefile                    # Automação de tarefas (test, run, benchmark, docker)
├── requirements.txt            # Dependências leves (pydantic, rich, python-dotenv)
├── run.sh                      # Ponto de entrada único exigido pela organização
├── dados/                      # Dados locais de desenvolvimento (.db, txt/, goldenset)
├── scripts/                    # Scripts de conversão de saída e empacotamento
├── src/
│   ├── cli/                    # CLI para execução em lote e benchmark
│   ├── core/                   # Configurações de ambiente e exceções
│   ├── repositories/           # Acesso e indexação SQLite e arquivos de texto
│   ├── schemas/                # Schemas Pydantic tipados
│   └── services/               # Extração, normalização, resolução e avaliação
└── tests/                      # Suíte de testes unitários e de integração
```

---

## 4. Instruções de Execução

### 4.1 Ponto de Entrada Único (Script `run.sh`)

O script `run.sh` é o ponto de entrada único que recebe o caminho do banco `.db`, a pasta com os documentos `.txt` e o arquivo/diretório de saída:

```bash
bash run.sh <caminho_db> <pasta_txt> <arquivo_saida>
```

#### Exemplo de uso:
```bash
bash run.sh ./dados/desafio1_bracis.db ./dados/txt ./submission.csv
```

O script:
1. Executa o pipeline de extração e resolução contra o banco indicado.
2. Salva os arquivos JSON intermediários no diretório de trabalho.
3. Converte os resultados para o formato `submission.csv` no caminho especificado.
4. Gera o arquivo compactado `submission.zip`.

### 4.2 Execução via Docker

Para rodar em máquina limpa de forma totalmente isolada:

#### 1. Construir a imagem:
```bash
docker build -t caca-alucinacoes-bracis .
```

#### 2. Executar o container:
Mapeie o diretório contendo os dados e o diretório de saída:
```bash
docker run --rm \
  -v /caminho/absoluto/dados:/dados \
  -v /caminho/absoluto/output:/output \
  caca-alucinacoes-bracis /dados/desafio1_bracis.db /dados/txt /output/submission.csv
```

### 4.3 Instalação e Execução Nativa

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Comandos disponíveis via `Makefile`:
- `make entrypoint`: Executa `run.sh` com os caminhos padrão.
- `make run`: Executa o processamento em lote gerando JSONs em `./output`.
- `make submission`: Gera `submission.csv` e `submission.zip`.
- `make benchmark`: Executa a avaliação completa contra o gabarito oficial.
- `make test`: Roda a suíte completa de testes unitários e de integração.
- `make clean`: Remove artefatos temporários e caches.

---

## 5. Resultados de Validação

Avaliação contra a amostra final oficial congelada (192 citações):
- **Span Matches (IoU $\ge$ 0.5)**: 192 / 192 (100.00% Precision e Recall)
- **F1-Score**: 1.0000
- **Classification Accuracy**: 1.0000 (100.00%)
- **Canonical ID Accuracy**: 1.0000 (100.00%)
- **Pontuação no Leaderboard do Kaggle**: **1.10000** (1º Lugar, com bônus máximo de calibração Brier).
