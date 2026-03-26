import pytest
import requests
import json
import os

def get_api_data():
    # busca os dados na api
    response = requests.get("https://jsonplaceholder.typicode.com/todos")
    if response.status_code != 200:
        raise Exception(f"Erro: Status {response.status_code}")
    
    data = response.json()
    return [
        {
            "text": item.get("title"),
            "id": item.get("id"),
            "is_correct": item.get("completed") 
        }
        for item in data
    ]
# fixture de escopo de sessão que garante a existência do mock.json.
# se não existir, baixa da API e salva o arquivo e retorna a lista de dados dele
@pytest.fixture(scope="session") # garante que isso só rode uma vez por execução de testes.
def choices_mock_data():
    filename = "mock.json"
    if not os.path.exists(filename):
        try:
            data_to_save = get_api_data()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            pytest.fail(f"Falha crítica: Não foi possível gerar o mock.json: {e}")

    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)