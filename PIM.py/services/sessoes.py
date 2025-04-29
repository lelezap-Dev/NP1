import json
import os
from datetime import datetime

def carregar_sessoes():
    try:
        with open('data/sessoes.json', 'r') as file:
            return json.load(file)
    except:
        return []

def salvar_sessoes(sessoes):
    os.makedirs('data', exist_ok=True)
    with open('data/sessoes.json', 'w') as file:
        json.dump(sessoes, file, indent=4, ensure_ascii=False)

def registrar_login(cpf):
    sessoes = carregar_sessoes()
    sessao = {
        'cpf': cpf,
        'inicio': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'fim': None,
        'duracao_minutos': None
    }
    sessoes.append(sessao)
    salvar_sessoes(sessoes)

def registrar_logout(cpf):
    sessoes = carregar_sessoes()
    for sessao in reversed(sessoes):
        if sessao['cpf'] == cpf and sessao['fim'] is None:
            sessao['fim'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            inicio = datetime.strptime(sessao['inicio'], '%Y-%m-%d %H:%M:%S')
            fim = datetime.strptime(sessao['fim'], '%Y-%m-%d %H:%M:%S')
            sessao['duracao_minutos'] = round((fim - inicio).total_seconds() / 60, 2)
            break
    salvar_sessoes(sessoes)

def exibir_sessoes_usuario(cpf):
    sessoes = carregar_sessoes()
    user_sessions = [s for s in sessoes if s['cpf'] == cpf]
    if not user_sessions:
        print('Nenhuma sessão encontrada para este usuário.')
        return

    print('\n📋 Histórico de Sessões:')
    for sessao in user_sessions:
        print(f"Início: {sessao['inicio']} | Fim: {sessao['fim']} | Duração: {sessao['duracao_minutos']} minutos")
