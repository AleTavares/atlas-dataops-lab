#!/bin/bash

echo "🔄 Reiniciando Apache Atlas..."

# Para o Atlas
docker-compose stop atlas

# Remove o container
docker-compose rm -f atlas

# Limpa o volume (CUIDADO: remove todos os dados!)
echo "⚠️  Removendo dados do Atlas..."
docker volume rm atlas-dataops-lab_atlas_data 2>/dev/null || true
docker volume rm atlas-dataops-lab_atlas_logs 2>/dev/null || true

# Recria o container
echo "🚀 Iniciando Atlas..."
docker-compose up -d atlas

# Aguarda inicialização
echo "⏳ Aguardando Atlas inicializar (pode levar 3-5 minutos)..."
sleep 30

# Monitora logs
docker-compose logs -f atlas
