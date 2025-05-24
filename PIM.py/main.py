# ======= main.py =======
from services.usuarios import cadastrar_usuario, autenticar
from services.conteudos import criar_conteudo
from services.quiz import responder_conteudo, relatorio_usuario, relatorio_pessoal
from services.graficos import (
    gerar_grafico_media_usuarios,
    gerar_grafico_distribuicao,
    gerar_grafico_por_conteudo
)
from services.relatorios import exportar_relatorio_txt
from services.relatorios import exportar_relatorio_txt, exportar_relatorio_json
from services.conteudos import criar_conteudo, deletar_conteudo
from services.sessoes import registrar_login, registrar_logout, exibir_sessoes_usuario
from services.usuarios import cadastrar_usuario, autenticar, redefinir_senha
from services.sessoes import visualizar_conteudos_por_tema, listar_conteudos, editar_conteudo, listar_usuarios, excluir_usuario, editar_usuario
from services.sessoes import ranking_geral
from services.certificados import gerar_certificado

def menu_aluno(usuario):
    while True:
        print('\n--- Menu do Aluno ---')
        print('1. Visualizar conteúdos')
        print('2. Realizar avaliações')
        print('3. Ver seu desempenho')
        print('4. Emitir certificado de curso')
        print('5. Ver ranking dos alunos')
        print('6. Sair')
        
        op = input('Escolha: ')
        
        if op == '1':
            visualizar_conteudos_por_tema(usuario['nome'])
        elif op == '2':
            responder_conteudo(usuario)
        elif op == '3':
            relatorio_pessoal(usuario['cpf'])
        elif op == '4':
            gerar_certificado(usuario)
        elif op == '5':
            ranking_geral() 
        elif op == '6':
            registrar_logout(usuario['cpf'])
            break
        else:
            print('Opção inválida.')


# ======= Submenus para administrador =======
def crud_usuarios():
    while True:
        print("\n--- CRUD de Usuários ---")
        print("1. Listar usuários")
        print("2. Editar usuário")
        print("3. Excluir usuário")
        print("4. Voltar")
        escolha = input("Escolha: ")

        if escolha == '1':
            listar_usuarios()
        elif escolha == '2':
            editar_usuario()
        elif escolha == '3':
            excluir_usuario()
        elif escolha == '4':
            break
        else:
            print("Opção inválida.")

def crud_conteudos():
    while True:
        print("\n--- Gerenciar Conteúdos ---")
        print("1. Criar conteúdo")
        print("2. Listar conteúdos")
        print("3. Editar conteúdo")
        print("4. Deletar conteúdo")
        print("5. Voltar")
        escolha = input("Escolha: ")

        if escolha == '1':
            criar_conteudo()
        elif escolha == '2':
            listar_conteudos()
        elif escolha == '3':
            editar_conteudo()
        elif escolha == '4':
            deletar_conteudo()
        elif escolha == '5':
            break
        else:
            print("Opção inválida.")

def menu_administrador(usuario):
    while True:
        print('\n--- Menu do Administrador ---')
        print('1. Gerenciar conteúdos')
        print('2. Gerenciar usuários')
        print('3. Ver relatório de usuário')
        print('4. Gráficos de desempenho')
        print('5. Exportar relatórios')
        print('6. Ver sessões de um usuário')
        print('7. Sair')

        op = input('Escolha: ')

        if op == '1':
            crud_conteudos()
        elif op == '2':
            crud_usuarios()
        elif op == '3':
            cpf = input('Digite o CPF do usuário: ')
            relatorio_usuario(cpf)
        elif op == '4':
            gerar_grafico_media_usuarios()
            gerar_grafico_distribuicao()
            gerar_grafico_por_conteudo()
        elif op == '5':
            cpf = input('Digite o CPF do usuário para exportar: ')
            exportar_relatorio_txt(cpf)
            exportar_relatorio_json(cpf)
        elif op == '6':
            cpf = input('Digite o CPF do usuário: ')
            exibir_sessoes_usuario(cpf)
        elif op == '7':
            registrar_logout(usuario['cpf'])
            break
        else:
            print('Opção inválida.')

if __name__ == '__main__':
    while True:
        print('\n--- Sistema Educacional ---')
        print('1. Cadastrar usuário')
        print('2. Entrar')
        print('3. Esqueci minha senha')
        print('4. Sair')
        escolha = input('Escolha: ')

        if escolha == '1':
            cadastrar_usuario()
        elif escolha == '2':
            usuario = autenticar()
            registrar_login(usuario['cpf'])
            if usuario:
                if usuario['perfil'] == 'Aluno':
                    menu_aluno(usuario)
                elif usuario['perfil'] == 'Administrador':
                    menu_administrador(usuario)
        elif escolha == '3':
            redefinir_senha()
        elif escolha == '4':
            registrar_logout(usuario['cpf'])
            break
        else:
            print('Opção inválida.')