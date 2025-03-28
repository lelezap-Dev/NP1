import json
import bcrypt
import os

def carregar_usuarios():
    try:
        with open('data/usuarios.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def carregar_conteudos():
    try:
        with open('data/conteudos.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def verificar_senha(senha, senha_hash):
    return bcrypt.checkpw(senha.encode(), senha_hash.encode())

def salvar_conteudos(conteudos):
    os.makedirs('data', exist_ok=True)
    with open('data/conteudos.json', 'w') as file:
        json.dump(conteudos, file, indent=4)

def menu_aluno():
    while True:
        print('\nBem-vindo ao painel do Aluno!')
        print('1. Visualizar conteúdos')
        print('2. Realizar avaliações')
        print('3. Ver seu desempenho')
        print('4. Sair')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            conteudos = carregar_conteudos()
            if conteudos:
                print('\nConteúdos Disponíveis:')
                for idx, conteudo in enumerate(conteudos, start=1):
                    print(f'{idx}. {conteudo.get("titulo", "Sem título")}')

                escolha = input('\nDigite o número do conteúdo para visualizar ou 0 para voltar: ')
                if escolha.isdigit() and 1 <= int(escolha) <= len(conteudos):
                    conteudo_escolhido = conteudos[int(escolha) - 1]
                    print(f"\nTítulo: {conteudo_escolhido.get('titulo', 'Sem título')}")
                    print(f"Descrição: {conteudo_escolhido.get('descricao', 'Sem descrição disponível')}")
                    if 'perguntas' in conteudo_escolhido:
                        print('\nQuestionário:')
                        for pergunta in conteudo_escolhido['perguntas']:
                            print(f"Pergunta: {pergunta['pergunta']}")
                            print("Alternativas:")
                            for alt in pergunta['alternativas']:
                                print(f"- {alt}")
                    else:
                        print('Nenhum questionário disponível para este conteúdo.')
                elif escolha == '0':
                    continue
                else:
                    print('Opção inválida.')
            else:
                print('Nenhum conteúdo disponível no momento.')

        elif opcao == '2':
            print('Funcionalidade de realizar avaliações em desenvolvimento.')
        elif opcao == '3':
            print('Funcionalidade de ver desempenho em desenvolvimento.')
        elif opcao == '4':
            break
        else:
            print('Opção inválida.')
            
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

def menu_administrador():
    while True:
        print('\nBem-vindo ao painel do Administrador!')
        print('1. Gerenciar usuários')
        print('2. Visualizar relatórios')
        print('3. Configurações do sistema')
        print('4. Sair')
        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            print('Funcionalidade de gerenciar usuários em desenvolvimento.')
        elif opcao == '2':
            print('Funcionalidade de visualizar relatórios em desenvolvimento.')
        elif opcao == '3':
            print('Funcionalidade de configurações do sistema em desenvolvimento.')
        elif opcao == '4':
            break
        else:
            print('Opção inválida.')

def login():
    usuarios = carregar_usuarios()
    cpf = input('Digite seu CPF: ')
    senha = input('Digite sua senha: ')

    for usuario in usuarios:
        if usuario['cpf'] == cpf and verificar_senha(senha, usuario['senha']):
            print(f'Login bem-sucedido! Bem-vindo, {usuario["nome"]}.')
            if usuario['perfil'] == 'Instrutor':
                menu_instrutor()
            elif usuario['perfil'] == 'Aluno':
                menu_aluno()
            elif usuario['perfil'] == 'Administrador':
                menu_administrador()
            else:
                print('Perfil não reconhecido.')
            return
    print('CPF ou senha inválidos.')
