# ======= services/sessoes.py =======
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
            fim = datetime.now()
            inicio = datetime.strptime(sessao['inicio'], '%Y-%m-%d %H:%M:%S')
            sessao['fim'] = fim.strftime('%Y-%m-%d %H:%M:%S')
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
        fim = sessao['fim'] if sessao['fim'] else '(sessão em andamento)'
        duracao = sessao['duracao_minutos'] if sessao['duracao_minutos'] else '-'
        print(f"Início: {sessao['inicio']} | Fim: {fim} | Duração: {duracao} minutos")
        
def visualizar_conteudos_por_tema(nome_usuario):
    from services.conteudos import carregar_conteudos
    from services.leitura import registrar_leitura

    conteudos = carregar_conteudos()
    if not conteudos:
        print("Nenhum conteúdo disponível.")
        return

    temas_disponiveis = list(set(c['tema'] for c in conteudos))

    print("\nTemas disponíveis:")
    for i, tema in enumerate(temas_disponiveis):
        print(f"{i+1}. {tema}")

    try:
        escolha = int(input("Escolha o tema para visualizar os conteúdos: ")) - 1
        if escolha < 0 or escolha >= len(temas_disponiveis):
            print("Opção inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    tema_escolhido = temas_disponiveis[escolha]
    conteudos_filtrados = [c for c in conteudos if c['tema'] == tema_escolhido]

    print(f"\nConteúdos do tema '{tema_escolhido}':")
    for c in conteudos_filtrados:
        print(f"\nTítulo: {c['titulo']}\nDescrição: {c['descricao']}")
        registrar_leitura(nome_usuario, c['titulo'])
