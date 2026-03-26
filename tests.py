import pytest
from model import Question, Choice 
import requests
import json
import os

#funcao de extracao do mock
def get_api_data():
    response = requests.get("https://jsonplaceholder.typicode.com/todos")
    
    # valida o status code
    if response.status_code != 200:
        raise Exception(f"Erro: Status {response.status_code}")
    
    # valida o cabeçalho do JSON
    if "application/json" not in response.headers.get("Content-Type", ""):
        raise Exception("Erro: Resposta não é JSON")
    
    data = response.json()
    
    # valida se é uma lista e se não está vazia
    if not isinstance(data, list) or len(data) == 0:
        raise Exception("Erro: API retornou uma lista vazia ou formato inválido")
    
    dados_convertidos = [
    {
        "text": item.get("title"),
        "id": item.get("id"),
        "is_correct": item.get("completed") 
    }
    for item in data
    ]

        
    return dados_convertidos


def ensure_mock_exists(filename="mock.json"):
    # verifica se o arquivo já existe
    if os.path.exists(filename):
        print(f"O arquivo {filename} já existe. Pulando criação.")
        return

    # se não existir, busca os dados da API
    print(f"Arquivo {filename} não encontrado. Buscando dados da API...")
    try:
        data_to_save = get_api_data()
        
        # salva no arquivo JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
            
        print(f"Sucesso: Mock criado com {len(data_to_save)} itens.")
    except Exception as e:
        print(f"Falha ao criar o mock: {e}")


ensure_mock_exists()
# pega os dados do mock
def load_mock_data(filename="mock.json"):
    # verifica se o arquivo existe antes de tentar abrir
    if not os.path.exists(filename):
        print(f"Erro: O arquivo {filename} não foi encontrado.")
        return None

    # abre o arquivo em modo de leitura ('r')
    with open(filename, 'r', encoding='utf-8') as f:
        # converte o conteúdo do arquivo para uma variável
        data = json.load(f)
    
    return data

choices_list = load_mock_data()


  

def test_create_question():
    question = Question(title='q1')
    assert question.id != None
    #teste 1(verifica se a lista do construtor está vazia ao ser criada)
    assert question.choices == [] 




def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id
    #teste2(verifica se as listas não apontam para o mesmo endereço de memória)
    assert question1.choices is not question2.choices 

    


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1 
    question = Question(title='q1', points=100)
    assert question.points == 100
    #teste 3(verifica se é uma string)
    assert isinstance(question.id, str) 
    #teste 4(verifica o comprimento UUID hex tem 32 caracteres)
    assert len(question.id) == 32
    #teste 5(verifica se todos os caracteres são hexadecimais)
    assert all(c in "0123456789abcdef" for c in question.id)

def test_create_choice():
    question = Question(title='q1')
    question.add_choice('a', False)
    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    assert isinstance(question.choices[0], Choice) #teste 6 (verifica o tipo do objeto criado)



#roda para cada linha do arquivo
@pytest.mark.parametrize("data", choices_list)
def test_choice_instantiation_from_mock(data):
    # validação dos limites de tamanho do text
    if len(data['text']) > 100:
        with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
            Choice(id=data['id'], text=data['text'], is_correct=data['is_correct'])
    else:
        # teste de sucesso
        choice = Choice(id=data['id'], text=data['text'], is_correct=data['is_correct'])
        
        assert choice.id == data['id']
        assert choice.text == data['text']
        assert choice.is_correct == data['is_correct']
   #teste 7(robustez: de 200 itens testados nenhum foi corrompido ou longo demais, caso contrário a classe iria disparar a excessão)
   #teste 8(conformidade: todos os itens foram transformados no objeto desejado)
   #teste 9(mapeamento de tipos:conversão adequada false/true do JSON para o tipo booleano e dos ID's para inteiros)
   #teste 10(testes de integridade do JSON lidos da API, teste se a leitura foi bem sucedida, se o arquivo não veio vazio, código de retorno 200 da API, etc.)
   