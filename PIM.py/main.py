# ======= main.py =======
from services.usuarios import cadastrar_usuario, autenticar
from services.conteudos import criar_conteudo, visualizar_conteudos
from services.quiz import responder_conteudo, relatorio_usuario, relatorio_pessoal
from services.graficos import (
    gerar_grafico_media_usuarios,
    gerar_grafico_distribuicao,
    gerar_grafico_por_conteudo
)
from services.relatorios import exportar_relatorio_txt
from services.relatorios import exportar_relatorio_txt, exportar_relatorio_json

def menu_aluno(usuario):
    while True:
        print('\n--- Menu do Aluno ---')
        print('1. Visualizar conteúdos')
        print('2. Realizar avaliações')
        print('3. Ver seu desempenho')
        print('4. Sair')
        op = input('Escolha: ')

        if op == '1':
            visualizar_conteudos()
        elif op == '2':
            responder_conteudo(usuario)
        elif op == '3':
            relatorio_pessoal(usuario['cpf'])
        elif op == '4':
            break
        else:
            print('Opção inválida.')

def menu_administrador(usuario):
    while True:
        print('\n--- Menu do Administrador ---')
        print('1. Criar conteúdo')
        print('2. Ver relatório de usuário')
        print('3. Gráfico: média por usuário')
        print('4. Gráfico: distribuição de acertos')
        print('5. Gráfico: desempenho por conteúdo')
        print('6. Exportar relatório em TXT')
        print('7. Exportar relatório em JSON')
        print('8. Sair')
        op = input('Escolha: ')

        if op == '1':
            criar_conteudo()
        elif op == '2':
            cpf = input('Digite o CPF do usuário: ')
            relatorio_usuario(cpf, usuario)
        elif op == '3':
            gerar_grafico_media_usuarios()
        elif op == '4':
            gerar_grafico_distribuicao()
        elif op == '5':
            gerar_grafico_por_conteudo()
        elif op == '6':
            cpf = input('Digite o CPF do usuário para exportar TXT: ')
            exportar_relatorio_txt(cpf)
        elif op == '7':
            cpf = input('Digite o CPF do usuário para exportar JSON: ')
            exportar_relatorio_json(cpf)
        elif op == '8':
            break
        else:
            print('Opção inválida.')

if __name__ == '__main__':
    while True:
        print('\n--- Sistema Educacional ---')
        print('1. Cadastrar usuário')
        print('2. Entrar')
        print('3. Sair')
        escolha = input('Escolha: ')

        if escolha == '1':
            cadastrar_usuario()
        elif escolha == '2':
            usuario = autenticar()
            if usuario:
                if usuario['perfil'] == 'Aluno':
                    menu_aluno(usuario)
                elif usuario['perfil'] == 'Administrador':
                    menu_administrador(usuario)
        elif escolha == '3':
            break
        else:
            print('Opção inválida.')