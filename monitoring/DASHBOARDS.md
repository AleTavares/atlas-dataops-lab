# 📊 Dashboards de Saúde dos Containers

## Visão Geral

Este guia explica como visualizar e monitorar a saúde de todos os containers da plataforma DataOps usando Kibana.

## 🚀 Inicialização

### 1. Iniciar Metricbeat

```bash
# Iniciar todos os serviços (incluindo Metricbeat)
docker-compose up -d

# Verificar se Metricbeat está rodando
docker-compose ps metricbeat
docker-compose logs -f metricbeat
```

### 2. Configurar Dashboards

```bash
# Executar script de configuração
./monitoring/setup_dashboards.sh
```

## 📈 Métricas Coletadas

### Por Container

| Métrica | Descrição | Campo Kibana |
|---------|-----------|--------------|
| **CPU Usage** | Uso de CPU (%) | `docker.cpu.total.pct` |
| **Memory Usage** | Uso de memória (bytes) | `docker.memory.usage.total` |
| **Memory Limit** | Limite de memória | `docker.memory.limit` |
| **Network RX** | Bytes recebidos | `docker.network.in.bytes` |
| **Network TX** | Bytes transmitidos | `docker.network.out.bytes` |
| **Disk Read** | Leitura de disco | `docker.diskio.read.bytes` |
| **Disk Write** | Escrita de disco | `docker.diskio.write.bytes` |
| **Health Status** | Status do healthcheck | `docker.healthcheck.status` |
| **Container Status** | Status do container | `docker.container.status` |

### Sistema

| Métrica | Descrição | Campo Kibana |
|---------|-----------|--------------|
| **System CPU** | CPU total do host | `system.cpu.total.pct` |
| **System Memory** | Memória total do host | `system.memory.used.pct` |
| **System Load** | Load average | `system.load.1`, `system.load.5`, `system.load.15` |
| **Filesystem** | Uso de disco | `system.filesystem.used.pct` |

## 🎨 Criando Dashboards Personalizados

### 1. Acessar Kibana

```
URL: http://localhost:5601
```

### 2. Criar Dashboard

1. **Menu** → **Analytics** → **Dashboard**
2. Clicar em **Create dashboard**
3. Clicar em **Add panel**

### 3. Visualizações Recomendadas

#### A. CPU por Container (Line Chart)

```
Visualization: Line
Index: metricbeat-*
Metrics:
  - Y-axis: Average of docker.cpu.total.pct
Buckets:
  - X-axis: Date Histogram (@timestamp)
  - Split series: Terms (container.name)
```

#### B. Memória por Container (Area Chart)

```
Visualization: Area
Index: metricbeat-*
Metrics:
  - Y-axis: Average of docker.memory.usage.total
Buckets:
  - X-axis: Date Histogram (@timestamp)
  - Split series: Terms (container.name)
```

#### C. Status dos Containers (Metric)

```
Visualization: Metric
Index: metricbeat-*
Metrics:
  - Unique Count of container.name
Filter: docker.container.status: "running"
```

#### D. Network I/O (Line Chart)

```
Visualization: Line
Index: metricbeat-*
Metrics:
  - Y-axis 1: Rate of docker.network.in.bytes
  - Y-axis 2: Rate of docker.network.out.bytes
Buckets:
  - X-axis: Date Histogram (@timestamp)
  - Split series: Terms (container.name)
```

#### E. Disk I/O (Line Chart)

```
Visualization: Line
Index: metricbeat-*
Metrics:
  - Y-axis 1: Rate of docker.diskio.read.bytes
  - Y-axis 2: Rate of docker.diskio.write.bytes
Buckets:
  - X-axis: Date Histogram (@timestamp)
  - Split series: Terms (container.name)
```

#### F. Healthcheck Status (Table)

```
Visualization: Table
Index: metricbeat-*
Buckets:
  - Split rows: Terms (container.name)
Metrics:
  - Last value of docker.healthcheck.status
  - Last value of docker.container.status
```

#### G. Top Containers por CPU (Bar Chart)

```
Visualization: Horizontal Bar
Index: metricbeat-*
Metrics:
  - Y-axis: Average of docker.cpu.total.pct
Buckets:
  - X-axis: Terms (container.name)
  - Order: Metric (Descending)
  - Size: 10
```

#### H. Top Containers por Memória (Bar Chart)

```
Visualization: Horizontal Bar
Index: metricbeat-*
Metrics:
  - Y-axis: Average of docker.memory.usage.total
Buckets:
  - X-axis: Terms (container.name)
  - Order: Metric (Descending)
  - Size: 10
```

## 🔍 Queries Úteis no Discover

### Containers Rodando

```
docker.container.status: "running"
```

### Containers com Alto Uso de CPU (>80%)

```
docker.cpu.total.pct > 0.8
```

### Containers com Alto Uso de Memória (>80%)

```
docker.memory.usage.pct > 0.8
```

### Healthcheck Falhou

```
docker.healthcheck.status: "unhealthy"
```

### Container Específico (Apache Atlas)

```
container.name: "apache-atlas"
```

### Todos os Containers da Plataforma

```
container.name: ("apache-atlas" OR "postgres-erp" OR "pyspark_aula_container" OR "airflow-standalone" OR "elasticsearch" OR "kibana" OR "filebeat" OR "metricbeat")
```

## 📊 Dashboard Completo Sugerido

### Layout (Grid 48 colunas)

```
┌─────────────────────────────────────────────────┐
│  Containers Ativos (Metric)    │  CPU Total (%)  │
│  [24 cols x 4 rows]            │  [24 cols x 4]  │
├─────────────────────────────────────────────────┤
│  CPU por Container (Line Chart)                  │
│  [48 cols x 12 rows]                            │
├─────────────────────────────────────────────────┤
│  Memória por Container (Area Chart)              │
│  [48 cols x 12 rows]                            │
├─────────────────────────────────────────────────┤
│  Network I/O (Line)  │  Disk I/O (Line)         │
│  [24 cols x 12]      │  [24 cols x 12]          │
├─────────────────────────────────────────────────┤
│  Top CPU (Bar)       │  Top Memória (Bar)       │
│  [24 cols x 12]      │  [24 cols x 12]          │
├─────────────────────────────────────────────────┤
│  Status dos Containers (Table)                   │
│  [48 cols x 12 rows]                            │
└─────────────────────────────────────────────────┘
```

## 🚨 Alertas Recomendados

### 1. CPU Alta

```
Condição: docker.cpu.total.pct > 0.9
Duração: 5 minutos
Ação: Notificar equipe
```

### 2. Memória Alta

```
Condição: docker.memory.usage.pct > 0.9
Duração: 5 minutos
Ação: Notificar equipe
```

### 3. Container Parado

```
Condição: docker.container.status != "running"
Duração: 1 minuto
Ação: Notificar equipe imediatamente
```

### 4. Healthcheck Falhou

```
Condição: docker.healthcheck.status == "unhealthy"
Duração: 2 minutos
Ação: Notificar equipe
```

## 🔧 Troubleshooting

### Metricbeat não está coletando dados

```bash
# Verificar logs
docker-compose logs metricbeat

# Verificar se está rodando
docker-compose ps metricbeat

# Reiniciar
docker-compose restart metricbeat
```

### Dados não aparecem no Kibana

```bash
# Verificar se índices foram criados
curl http://localhost:9200/_cat/indices?v | grep metricbeat

# Verificar documentos
curl http://localhost:9200/metricbeat-*/_count

# Recriar index pattern
./monitoring/setup_dashboards.sh
```

### Elasticsearch sem espaço

```bash
# Verificar uso de disco
docker exec elasticsearch df -h

# Limpar índices antigos (cuidado!)
curl -X DELETE "http://localhost:9200/metricbeat-$(date -d '30 days ago' +%Y.%m.%d)"
```

## 📝 Exportar/Importar Dashboards

### Exportar Dashboard

1. **Menu** → **Stack Management** → **Saved Objects**
2. Selecionar dashboard
3. Clicar em **Export**
4. Salvar arquivo `.ndjson`

### Importar Dashboard

1. **Menu** → **Stack Management** → **Saved Objects**
2. Clicar em **Import**
3. Selecionar arquivo `.ndjson`
4. Clicar em **Import**

## 🎯 Próximos Passos

- [ ] Configurar alertas automáticos
- [ ] Criar dashboard de comparação histórica
- [ ] Adicionar métricas de aplicação (Atlas, Airflow)
- [ ] Configurar retenção de dados
- [ ] Integrar com sistema de notificações

## 📚 Referências

- [Metricbeat Docker Module](https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-module-docker.html)
- [Kibana Visualizations](https://www.elastic.co/guide/en/kibana/current/dashboard.html)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
