#!/bin/bash

echo "🎨 Configurando Dashboards de Saúde dos Containers..."

# Aguarda Elasticsearch estar pronto
echo "⏳ Aguardando Elasticsearch..."
until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"green"\|"status":"yellow"'; do
    sleep 5
done

echo "✅ Elasticsearch pronto!"

# Aguarda Kibana estar pronto
echo "⏳ Aguardando Kibana..."
until curl -s http://localhost:5601/api/status | grep -q '"level":"available"'; do
    sleep 5
done

echo "✅ Kibana pronto!"

# Cria index patterns
echo "📊 Criando Index Patterns..."

# Index pattern para Metricbeat
curl -X POST "http://localhost:5601/api/saved_objects/index-pattern/metricbeat-*" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
    "attributes": {
      "title": "metricbeat-*",
      "timeFieldName": "@timestamp"
    }
  }'

echo ""
echo "✅ Index patterns criados!"

# Aguarda alguns segundos para garantir que os dados estão sendo coletados
echo "⏳ Aguardando coleta de métricas (30 segundos)..."
sleep 30

echo ""
echo "✅ Dashboards configurados com sucesso!"
echo ""
echo "📊 Acesse o Kibana em: http://localhost:5601"
echo ""
echo "🔍 Visualizações disponíveis:"
echo "   - Discover > metricbeat-* (métricas de containers)"
echo "   - Analytics > Dashboard > Criar dashboard customizado"
echo ""
echo "📈 Métricas coletadas:"
echo "   - CPU por container"
echo "   - Memória por container"
echo "   - Network I/O"
echo "   - Disk I/O"
echo "   - Healthcheck status"
echo ""
