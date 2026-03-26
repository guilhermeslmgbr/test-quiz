import pytest
from model import Question, Choice 
import requests
import json
import os

#fixture de escopo 'function' 
@pytest.fixture
#cria uma questão nova para cada teste que a solicitar.
def question_with_choices():
    question = Question(title="Pergunta padrao", max_selections=1)
    question.add_choice("choice_1", is_correct=True)  # ID 1
    question.add_choice("choice_2", is_correct=False) # ID 2
    question.add_choice("choice_3", is_correct=False)  # ID 3
    return question

def test_remove_choice_by_id(question_with_choices):
    question_with_choices.remove_choice_by_id(2)
    assert len(question_with_choices.choices) == 2
    # verifica se o ID 2 realmente sumiu da lista de IDs
    assert 2 not in [c.id for c in question_with_choices.choices]

def test_remove_all_choices(question_with_choices):
    question_with_choices.remove_all_choices()
    assert len(question_with_choices.choices) == 0

def test_correct_selected_choices_valid(question_with_choices):
    # testa se acertou
    acertos = question_with_choices.correct_selected_choices([1])
    assert acertos == [1]

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

#roda para cada linha do arquivo, baseado no tamanho do mock
@pytest.mark.parametrize("index", range(200)) 
def test_choice_instantiation_from_mock(choices_mock_data, index): #carrega os dados da fixture que vem do conftest.py
    data = choices_mock_data[index] # pega o item específico da rodada
    
    if len(data['text']) > 100:
        with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
            Choice(id=data['id'], text=data['text'], is_correct=data['is_correct'])
    else:
        choice = Choice(id=data['id'], text=data['text'], is_correct=data['is_correct'])
        
        assert choice.id == data['id']
        assert choice.text == data['text']
        assert isinstance(choice.is_correct, bool)
   #teste 7(robustez: de 200 itens testados nenhum foi corrompido ou longo demais, caso contrário a classe iria disparar a excessão)
   #teste 8(conformidade: todos os itens foram transformados no objeto desejado)
   #teste 9(mapeamento de tipos:conversão adequada false/true do JSON para o tipo booleano e dos ID's para inteiros)
   #teste 10(testes de integridade do JSON lidos da API, teste se a leitura foi bem sucedida, se o arquivo não veio vazio, código de retorno 200 da API, etc.)
   