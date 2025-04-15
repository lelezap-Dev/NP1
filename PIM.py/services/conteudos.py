# ======= services/conteudos.py =======
import json, os

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

    titulo = input('Título: ')
    descricao = input('Descrição do conteúdo para estudo: ')
    perguntas = []
    while True:
        pergunta = input('Pergunta (enter para sair): ')
        if not pergunta: break
        correta = input('Resposta correta: ')
        alternativas = [correta] + [input(f'Outra alternativa ({i+1}/3): ') for i in range(3)]
        perguntas.append({ 'pergunta': pergunta, 'resposta_correta': correta, 'alternativas': alternativas })

    conteudos.append({ 'tema': tema, 'titulo': titulo, 'descricao': descricao, 'perguntas': perguntas })
    salvar_conteudos(conteudos)
    print('Conteúdo criado com sucesso!')

def visualizar_conteudos():
    conteudos = carregar_conteudos()
    for c in conteudos:
        print(f"\nTítulo: {c['titulo']}\nTema: {c['tema']}\nDescrição: {c['descricao']}\n")