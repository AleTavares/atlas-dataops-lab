# Monitoring com Elastic Stack

## Componentes

### Elasticsearch
- **Porta**: 9200
- **Função**: Armazenamento e indexação de logs
- **Índices**:
  - `airflow-logs-*`: Logs das DAGs do Airflow
  - `docker-logs-*`: Logs dos containers Docker

### Kibana
- **Porta**: 5601
- **URL**: http://localhost:5601
- **Função**: Visualização e análise de logs

### Filebeat
- **Função**: Coleta e envio de logs para Elasticsearch
- **Fontes**:
  - Logs do Airflow (`/logs`)
  - Logs dos containers Docker

## Dashboards Disponíveis

### 1. DataOps Platform - Overview
- Visão geral da plataforma
- Métricas de todos os serviços
- Status dos containers

### 2. Airflow DAG Executions
- Execuções de DAGs
- Taxa de sucesso/falha
- Duração das tasks
- Logs de erros

### 3. Spark Jobs Monitoring
- Jobs Spark em execução
- Performance dos jobs
- Logs de processamento

## Como Usar

### Acessar Kibana
```bash
# Abrir navegador
http://localhost:5601
```

### Importar Dashboards
```bash
# Via Kibana UI
1. Acessar Stack Management > Saved Objects
2. Import > Selecionar monitoring/kibana_dashboards.ndjson
3. Confirmar importação
```

### Consultas Úteis

#### Logs de DAG específica
```
service:airflow AND dag_id:"catalog_postgres_to_atlas"
```

#### Erros do Airflow
```
service:airflow AND level:ERROR
```

#### Jobs Spark
```
container.name:pyspark* AND message:*spark-submit*
```

#### Logs do Atlas
```
container.name:atlas AND level:ERROR
```

## Métricas Monitoradas

### Airflow
- Execuções de DAGs (sucesso/falha)
- Duração das tasks
- Erros e exceções
- Uso de recursos

### Spark
- Jobs submetidos
- Tempo de execução
- Erros de processamento
- Métricas de performance

### Atlas
- Requisições API
- Erros de catalogação
- Performance de queries

### PostgreSQL
- Conexões ativas
- Queries lentas
- Erros de conexão

## Alertas Configuráveis

### Exemplos de Alertas
1. **DAG Failure**: Notificar quando DAG falha
2. **Spark Job Timeout**: Alertar se job excede tempo
3. **Atlas Down**: Notificar se Atlas não responde
4. **Disk Space**: Alertar quando espaço < 10%

## Retenção de Dados

- **Logs Airflow**: 30 dias
- **Logs Docker**: 7 dias
- **Métricas**: 90 dias

## Troubleshooting

### Elasticsearch não inicia
```bash
# Verificar logs
docker-compose logs elasticsearch

# Aumentar memória se necessário
# Editar docker-compose.yml: ES_JAVA_OPTS=-Xms1g -Xmx1g
```

### Filebeat não envia logs
```bash
# Verificar configuração
docker exec filebeat filebeat test config

# Verificar conectividade
docker exec filebeat filebeat test output
```

### Kibana não conecta
```bash
# Verificar se Elasticsearch está rodando
curl http://localhost:9200

# Reiniciar Kibana
docker-compose restart kibana
```