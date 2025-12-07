#!/usr/bin/env python3
"""
Cliente Python para Apache Atlas
Demonstra conexão e operações básicas com a API REST
"""

import requests
import json
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout


class AtlasClient:
    """
    Cliente para interagir com Apache Atlas via API REST.
    
    Implementa autenticação HTTP Basic e métodos para buscar, criar e obter
    informações sobre entidades no catálogo de dados.
    
    Args:
        url (str): URL base do Apache Atlas (padrão: http://localhost:21000)
        username (str): Nome de usuário para autenticação (padrão: admin)
        password (str): Senha para autenticação (padrão: admin)
    """
    
    def __init__(self, url="http://localhost:21000", username="admin", password="admin"):
        """
        Inicializa o cliente Atlas com autenticação HTTP Basic.
        
        Args:
            url (str): URL base do Apache Atlas
            username (str): Nome de usuário para autenticação
            password (str): Senha para autenticação
        """
        self.url = url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def _handle_response(self, response):
        """
        Trata a resposta HTTP e levanta exceções apropriadas em caso de erro.
        
        Args:
            response: Objeto Response do requests
            
        Returns:
            dict: JSON da resposta se bem-sucedida
            
        Raises:
            HTTPError: Se o status HTTP indicar erro
            ValueError: Se a resposta não for JSON válido
        """
        try:
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_msg = f"Erro HTTP {response.status_code}: {response.text}"
            try:
                error_json = response.json()
                if 'errorMessage' in error_json:
                    error_msg = f"Erro HTTP {response.status_code}: {error_json['errorMessage']}"
            except (ValueError, json.JSONDecodeError):
                pass
            raise HTTPError(error_msg) from e
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Resposta inválida do servidor: {response.text}") from e
    
    def search_entities(self, query):
        """
        Busca entidades no catálogo usando uma query de busca.
        
        Args:
            query (str): Query de busca (ex: "*", "table", "database.northwind")
            
        Returns:
            dict: Dicionário contendo as entidades encontradas com a estrutura:
                {
                    "entities": [...],
                    "queryType": "...",
                    "searchParameters": {...}
                }
                
        Raises:
            HTTPError: Se houver erro na requisição HTTP
            ConnectionError: Se não for possível conectar ao servidor
            Timeout: Se a requisição exceder o tempo limite
            RequestException: Para outros erros de requisição
        """
        try:
            params = {"query": query}
            response = self.session.get(
                f"{self.url}/api/atlas/v2/search/basic",
                params=params,
                timeout=30
            )
            return self._handle_response(response)
        except ConnectionError as e:
            raise ConnectionError(f"Não foi possível conectar ao Atlas em {self.url}") from e
        except Timeout as e:
            raise Timeout("Tempo limite excedido ao buscar entidades") from e
        except RequestException as e:
            raise RequestException(f"Erro ao buscar entidades: {str(e)}") from e
    
    def create_entity(self, entity_data):
        """
        Cria uma nova entidade no catálogo do Atlas.
        
        Args:
            entity_data (dict): Dicionário contendo os dados da entidade a ser criada.
                Deve seguir a estrutura esperada pelo Atlas, incluindo:
                - typeName: tipo da entidade
                - attributes: atributos da entidade
                
        Returns:
            dict: Dicionário contendo informações sobre a entidade criada, incluindo:
                - guid: GUID único da entidade criada
                - entity: dados da entidade
                
        Raises:
            HTTPError: Se houver erro na requisição HTTP (ex: entidade já existe)
            ConnectionError: Se não for possível conectar ao servidor
            Timeout: Se a requisição exceder o tempo limite
            RequestException: Para outros erros de requisição
            ValueError: Se entity_data não for válido
        """
        if not entity_data or not isinstance(entity_data, dict):
            raise ValueError("entity_data deve ser um dicionário não vazio")
        
        try:
            response = self.session.post(
                f"{self.url}/api/atlas/v2/entity",
                json={"entity": entity_data},
                timeout=30
            )
            return self._handle_response(response)
        except ConnectionError as e:
            raise ConnectionError(f"Não foi possível conectar ao Atlas em {self.url}") from e
        except Timeout as e:
            raise Timeout("Tempo limite excedido ao criar entidade") from e
        except RequestException as e:
            raise RequestException(f"Erro ao criar entidade: {str(e)}") from e
    
    def get_entity(self, guid):
        """
        Obtém uma entidade específica do catálogo usando seu GUID.
        
        Args:
            guid (str): GUID único da entidade a ser recuperada
            
        Returns:
            dict: Dicionário contendo os dados completos da entidade:
                {
                    "entity": {...},
                    "referredEntities": {...}
                }
                
        Raises:
            HTTPError: Se houver erro na requisição HTTP (ex: entidade não encontrada)
            ConnectionError: Se não for possível conectar ao servidor
            Timeout: Se a requisição exceder o tempo limite
            RequestException: Para outros erros de requisição
            ValueError: Se guid for inválido
        """
        if not guid or not isinstance(guid, str):
            raise ValueError("guid deve ser uma string não vazia")
        
        try:
            response = self.session.get(
                f"{self.url}/api/atlas/v2/entity/guid/{guid}",
                timeout=30
            )
            return self._handle_response(response)
        except ConnectionError as e:
            raise ConnectionError(f"Não foi possível conectar ao Atlas em {self.url}") from e
        except Timeout as e:
            raise Timeout("Tempo limite excedido ao obter entidade") from e
        except RequestException as e:
            raise RequestException(f"Erro ao obter entidade: {str(e)}") from e
    
    def get_lineage(self, guid):
        """
        Obtém a linhagem (lineage) de uma entidade, mostrando suas relações
        de origem e destino no fluxo de dados.
        
        Args:
            guid (str): GUID único da entidade para a qual obter a linhagem
            
        Returns:
            dict: Dicionário contendo informações de linhagem:
                {
                    "baseEntityGuid": "...",
                    "guidEntityMap": {...},
                    "relations": [...]
                }
                
        Raises:
            HTTPError: Se houver erro na requisição HTTP (ex: entidade não encontrada)
            ConnectionError: Se não for possível conectar ao servidor
            Timeout: Se a requisição exceder o tempo limite
            RequestException: Para outros erros de requisição
            ValueError: Se guid for inválido
        """
        if not guid or not isinstance(guid, str):
            raise ValueError("guid deve ser uma string não vazia")
        
        try:
            response = self.session.get(
                f"{self.url}/api/atlas/v2/lineage/{guid}",
                timeout=30
            )
            return self._handle_response(response)
        except ConnectionError as e:
            raise ConnectionError(f"Não foi possível conectar ao Atlas em {self.url}") from e
        except Timeout as e:
            raise Timeout("Tempo limite excedido ao obter linhagem") from e
        except RequestException as e:
            raise RequestException(f"Erro ao obter linhagem: {str(e)}") from e

def main():
    """Exemplo de uso do cliente Atlas"""
    print("🚀 Conectando ao Apache Atlas...")
    
    client = AtlasClient()
    
    try:
        # Buscar entidades
        results = client.search_entities("*")
        entities = results.get('entities', [])
        print(f"🔍 Entidades encontradas: {len(entities)}")
        
        # Mostrar primeiras entidades
        for i, entity in enumerate(entities[:3]):
            print(f"  {i+1}. {entity.get('displayText', 'N/A')} ({entity.get('typeName', 'N/A')})")
            
        # Exemplo: obter entidade por GUID (se houver entidades)
        if entities:
            first_guid = entities[0].get('guid')
            if first_guid:
                entity_data = client.get_entity(first_guid)
                print(f"\n📋 Dados da primeira entidade: {entity_data.get('entity', {}).get('attributes', {}).get('name', 'N/A')}")
                
                # Exemplo: obter linhagem
                lineage = client.get_lineage(first_guid)
                print(f"🔗 Linhagem obtida: {len(lineage.get('relations', []))} relações encontradas")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()