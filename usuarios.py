import json
import bcrypt
import os
from login import login

def carregar_usuarios():
    try:
        with open('data/usuarios.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_usuarios(usuarios):
    os.makedirs('data', exist_ok=True)
    with open('data/usuarios.json', 'w') as file:
        json.dump(usuarios, file, indent=4)

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha, senha_hash):
    return bcrypt.checkpw(senha.encode(), senha_hash.encode())

def cadastrar_usuario():
    usuarios = carregar_usuarios()
    cpf = input('Digite seu CPF (apenas números): ')
    if any(u['cpf'] == cpf for u in usuarios):
        print('CPF já cadastrado.')
        return

    nome = input('Nome completo: ')
    email = input('E-mail: ')
    senha = input('Senha: ')
    perfil = input('Perfil (Aluno, Instrutor, Administrador): ').capitalize()
    
    if perfil not in ['Aluno', 'Instrutor', 'Administrador']:
        print('Perfil inválido.')
        return

    senha_hash = hash_senha(senha)
    usuarios.append({
        'cpf': cpf,
        'nome': nome,
        'email': email,
        'senha': senha_hash,
        'perfil': perfil
    })

    salvar_usuarios(usuarios)
    print('Usuário cadastrado com sucesso!')

def carregar_conteudos():
    try:
        with open('data/conteudos.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_conteudos(conteudos):
    os.makedirs('data', exist_ok=True)
    with open('data/conteudos.json', 'w') as file:
        json.dump(conteudos, file, indent=4)

def criar_conteudo():
    conteudos = carregar_conteudos()
    tema = input('Escolha o tema (Tecnologia da Informação, Programação Básica, Segurança Digital): ').capitalize()
    if tema not in ['Tecnologia Da Informação', 'Programação Básica', 'Segurança Digital']:
        print('Tema inválido.')
        return

    titulo = input('Título do conteúdo: ')
    descricao = input('Descrição breve: ')

    # Adicionar perguntas e respostas
    perguntas = []
    while True:
        pergunta = input('Digite a pergunta (ou deixe em branco para finalizar): ')
        if not pergunta:
            break
        resposta_correta = input('Digite a resposta correta: ')
        alternativas = [resposta_correta]
        for i in range(3):
            alternativas.append(input(f'Digite outra alternativa ({i+1}/3): '))
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

def criar_perguntas_padrao():
    conteudos = [
        {
            'tema': 'Tecnologia Da Informação',
            'titulo': 'Introdução à TI',
            'descricao': 'Conceitos básicos sobre Tecnologia da Informação.',
            'perguntas': [
                {
                    'pergunta': 'O que significa a sigla TI?',
                    'resposta_correta': 'Tecnologia da Informação',
                    'alternativas': ['Tecnologia da Informação', 'Técnica Industrial', 'Teoria da Informação', 'Trabalho Integrado']
                },
                {
                    'pergunta': 'Qual é a principal função da TI em uma empresa?',
                    'resposta_correta': 'Gerenciar e processar informações',
                    'alternativas': ['Gerenciar e processar informações', 'Produzir bens materiais', 'Controlar a logística', 'Administrar recursos financeiros']
                }
            ]
        },
        {
            'tema': 'Programação Básica',
            'titulo': 'Fundamentos da Programação',
            'descricao': 'Introdução aos conceitos fundamentais de programação.',
            'perguntas': [
                {
                    'pergunta': 'Qual linguagem é comumente usada para iniciar na programação?',
                    'resposta_correta': 'Python',
                    'alternativas': ['Python', 'Assembly', 'C++', 'Ruby']
                },
                {
                    'pergunta': 'O que é um loop em programação?',
                    'resposta_correta': 'Uma estrutura de repetição',
                    'alternativas': ['Uma estrutura de repetição', 'Uma função de cálculo', 'Um método de ordenação', 'Um sistema de segurança']
                }
            ]
        },
        {
            'tema': 'Segurança Digital',
            'titulo': 'Boas Práticas de Segurança Digital',
            'descricao': 'Aprenda como proteger seus dados na internet.',
            'perguntas': [
                {
                    'pergunta': 'O que é um firewall?',
                    'resposta_correta': 'Uma barreira de segurança para redes',
                    'alternativas': ['Uma barreira de segurança para redes', 'Um software de edição de vídeos', 'Um antivírus', 'Um sistema de backup']
                },
                {
                    'pergunta': 'Qual é uma boa prática para criar senhas seguras?',
                    'resposta_correta': 'Usar combinações de letras, números e símbolos',
                    'alternativas': ['Usar combinações de letras, números e símbolos', 'Utilizar apenas números', 'Reutilizar a mesma senha', 'Anotar senhas em locais públicos']
                }
            ]
        }
    ]
    salvar_conteudos(conteudos)
    print('Perguntas padrão criadas com sucesso!')

def menu_instrutor():
    print('\nBem-vindo ao painel do Instrutor!')
    print('1. Criar conteúdo')
    print('2. Criar perguntas padrão')
    print('3. Visualizar desempenho dos alunos')
    print('4. Sair')
    escolha = input('Escolha uma opção: ')
    if escolha == '1':
        criar_conteudo()
    elif escolha == '2':
        criar_perguntas_padrao()
    elif escolha == '3':
        print('Funcionalidade de visualizar desempenho em desenvolvimento.')
    elif escolha == '4':
        return
    else:
        print('Opção inválida.')


def menu_principal():
    while True:
        print('\n1. Cadastrar usuário')
        print('2. Fazer login')
        print('3. Sair')
        escolha = input('Escolha uma opção: ')

        if escolha == '1':
            cadastrar_usuario()
        elif escolha == '2':
            login()
        elif escolha == '3':
            print('Saindo...')
            break
        else:
            print('Opção inválida.')

if __name__ == '__main__':
    menu_principal()
