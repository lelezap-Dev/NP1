# ======= services/conteudos.py =======
import json, os
from services.leitura import registrar_leitura

def carregar_conteudos():
    try:
        with open('data/conteudos.json', 'r') as file:
            return json.load(file)
    except:
        return []

def salvar_conteudos(conteudos):
    with open('data/conteudos.json', 'w') as file:
        json.dump(conteudos, file, indent=4)

def criar_conteudo():
    conteudos = carregar_conteudos()

    while True:
        tema = input('Escolha o tema (TI, Programação Básica, Segurança Digital): ').capitalize()
        if tema in ['Ti', 'Programação básica', 'Segurança digital']:
            break
        print('Tema inválido. Tente novamente.')

    while True:
        titulo = input('Título: ').strip()
        if titulo:
            break
        print('Título não pode ser vazio.')

    while True:
        descricao = input('Descrição do conteúdo para estudo: ').strip()
        if descricao:
            break
        print('Descrição não pode ser vazia.')

    perguntas = []
    while True:
        pergunta = input('Digite uma pergunta (ou pressione Enter para finalizar): ').strip()
        if not pergunta:
            if perguntas:
                break
            else:
                print('É necessário ter pelo menos uma pergunta!')
                continue

        resposta_correta = input('Resposta correta: ').strip()
        alternativas = [resposta_correta]
        for i in range(3):
            alt = input(f'Digite outra alternativa ({i+1}/3): ').strip()
            alternativas.append(alt)
        
        perguntas.append({
            'pergunta': pergunta,
            'resposta_correta': resposta_correta,
            'alternativas': alternativas
        })

    conteudos.append({
        'tema': tema,
        'titulo': titulo,
        'descricao': descricao,
        'perguntas': perguntas
    })
    salvar_conteudos(conteudos)
    print('Conteúdo criado com sucesso!')

def visualizar_conteudos(nome_usuario):
    conteudos = carregar_conteudos()
    for c in conteudos:
        print(f"\nTítulo: {c['titulo']}\nTema: {c['tema']}\nDescrição: {c['descricao']}\n")
        registrar_leitura(nome_usuario, c['titulo'])
        
def deletar_conteudo():
    conteudos = carregar_conteudos()
    if not conteudos:
        print('Nenhum conteúdo disponível para exclusão.')
        return

    print('\n--- Conteúdos Disponíveis ---')
    for idx, c in enumerate(conteudos):
        print(f"{idx+1}. {c['titulo']} - {c['tema']}")

    try:
        escolha = int(input('Digite o número do conteúdo que deseja excluir: ')) - 1
        if escolha < 0 or escolha >= len(conteudos):
            print('Opção inválida.')
            return

        confirmacao = input(f"Tem certeza que deseja excluir '{conteudos[escolha]['titulo']}'? (s/n): ").lower()
        if confirmacao == 's':
            conteudos.pop(escolha)
            salvar_conteudos(conteudos)
            print('Conteúdo excluído com sucesso!')
        else:
            print('Exclusão cancelada.')

    except ValueError:
        print('Entrada inválida.')
