import time
import re
import json
import hashlib
import os
from typing import List, Dict, Any

class SistemaEducacional:
    def __init__(self):
        self.usuarios = self.carregar_dados('usuarios.json')
        self.cursos = self.carregar_dados('cursos.json')
        self.modulos = self.carregar_dados('modulos.json')
        self.usuario_atual = None
        self.admin_email = "admin@sistema.com"
        self.admin_senha = self.criptografar_senha("admin123")
        self.verificar_admin()

    def verificar_admin(self):
        """Verifica se existe um usuário admin, se não, cria um"""
        if not any(user['email'] == self.admin_email for user in self.usuarios):
            self.usuarios.append({
                'nome': 'Administrador',
                'email': self.admin_email,
                'senha': self.admin_senha,
                'tipo': 'admin'
            })
            self.salvar_dados('usuarios.json', self.usuarios)
    def validar_email(self, email):
        """Valida o formato do email usando regex"""
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email)

    def menu_cursos(self):
        """Exibe e gerencia o menu de cursos"""
        if not self.cursos:
            print("\nNenhum curso disponível no momento.")
            time.sleep(2)
            return

        while True:
            self.exibir_cabecalho("Cursos Disponíveis")
            for idx, curso in enumerate(self.cursos, 1):
                print(f"{idx}. {curso['nome']}")
            
            print("\n0. Voltar ao menu principal")
            escolha = input("\nEscolha um curso para ver os módulos: ")

            if escolha == '0':
                break

            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(self.cursos):
                    self.acessar_modulos(self.cursos[idx]['nome'])
                else:
                    print("Opção inválida!")
                    time.sleep(1)
            except ValueError:
                print("Por favor, digite um número válido!")
                time.sleep(1)

    def acessar_modulos(self, nome_curso):
        """Acessa os módulos de um curso específico"""
        modulos_curso = [m for m in self.modulos if m['curso'] == nome_curso]
        if modulos_curso:
            print(f"\nMódulos do curso '{nome_curso}':")
            for idx, modulo in enumerate(modulos_curso, 1):
                print(f"\n{idx}. {modulo['modulo']}")
                print(f"   Descrição: {modulo['descricao']}")
            input("\nPressione Enter para continuar...")
        else:
            print("\nEste curso ainda não possui módulos cadastrados.")
            time.sleep(2)


    def carregar_dados(self, arquivo):
        caminho = os.path.join(os.path.dirname(__file__), arquivo)
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar_dados(self, arquivo, dados):
        caminho = os.path.join(os.path.dirname(__file__), arquivo)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_cabecalho(self, titulo):
        """Exibe um cabeçalho formatado"""
        self.limpar_tela()
        print("=" * 50)
        print(f"{titulo:^50}")
        print("=" * 50)

    def validar_senha(self, senha):
        """Valida a força da senha"""
        if len(senha) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres"
        if not re.search(r"[A-Z]", senha):
            return False, "A senha deve conter pelo menos uma letra maiúscula"
        if not re.search(r"[0-9]", senha):
            return False, "A senha deve conter pelo menos um número"
        return True, "Senha válida"

    def criptografar_senha(self, senha: str) -> str:
        """
        Criptografa a senha usando SHA-256
        Args:
            senha: A senha a ser criptografada
        Returns:
            A senha criptografada em formato hexadecimal
        """
        return hashlib.sha256(senha.encode()).hexdigest()
        # ... resto do código continua igual ...

    def fazer_cadastro(self):
        self.exibir_cabecalho("Cadastro de Usuário")
        
        nome = input("Digite seu nome completo: ").strip()
        while len(nome) < 3:
            print("O nome deve ter pelo menos 3 caracteres")
            nome = input("Digite seu nome completo: ").strip()

        email = input("Digite seu email: ").strip()
        while not self.validar_email(email):
            print("Email inválido. Use o formato: leandro@dominio.com")
            email = input("Digite seu email: ").strip()

        if any(usuario['email'] == email for usuario in self.usuarios):
            print("Este email já está cadastrado.")
            time.sleep(2)
            return

        senha = input("Digite sua senha: ")
        valido, mensagem = self.validar_senha(senha)
        while not valido:
            print(mensagem)
            senha = input("Digite sua senha: ")
            valido, mensagem = self.validar_senha(senha)

        tipo = 'usuario'  # Por padrão, novos cadastros são usuários normais
        
        self.usuarios.append({
            'nome': nome,
            'email': email,
            'senha': self.criptografar_senha(senha),
            'tipo': tipo
        })
        self.salvar_dados('usuarios.json', self.usuarios)
        
        print("\nCadastro realizado com sucesso!")
        print("Você será redirecionado para o login...")
        time.sleep(2)

    def fazer_login(self):
        self.exibir_cabecalho("Login")
        
        tentativas = 3
        while tentativas > 0:
            email = input("Email: ").strip()
            senha = input("Senha: ")
            senha_criptografada = self.criptografar_senha(senha)

            usuario = next((user for user in self.usuarios 
                          if user['email'] == email and user['senha'] == senha_criptografada), None)

            if usuario:
                self.usuario_atual = usuario
                print(f"\nBem-vindo, {usuario['nome']}!")
                time.sleep(1)
                return True
            else:
                tentativas -= 1
                print(f"Email ou senha incorretos. Tentativas restantes: {tentativas}")
                time.sleep(1)

        print("Número máximo de tentativas excedido. Tente novamente mais tarde.")
        time.sleep(2)
        return False
    def cadastrar_cursos(self):
        """Cadastra novos cursos no sistema"""
        self.exibir_cabecalho("Cadastro de Cursos")
        
        if not self.usuario_atual or self.usuario_atual['tipo'] != 'admin':
            print("Apenas administradores podem cadastrar cursos!")
            time.sleep(2)
            return

        nome_curso = input("Digite o nome do curso: ").strip()
        if not nome_curso:
            print("O nome do curso não pode estar vazio!")
            time.sleep(2)
            return

        if any(curso['nome'] == nome_curso for curso in self.cursos):
            print("Este curso já está cadastrado!")
            time.sleep(2)
            return

        self.cursos.append({'nome': nome_curso})
        self.salvar_dados('cursos.json', self.cursos)
        print("\nCurso cadastrado com sucesso!")
        time.sleep(2)

    def cadastrar_modulos(self):
        """Cadastra módulos para um curso específico"""
        self.exibir_cabecalho("Cadastro de Módulos")

        if not self.usuario_atual or self.usuario_atual['tipo'] != 'admin':
            print("Apenas administradores podem cadastrar módulos!")
            time.sleep(2)
            return

        if not self.cursos:
            print("Não há cursos cadastrados!")
            time.sleep(2)
            return

        print("\nCursos disponíveis:")
        for idx, curso in enumerate(self.cursos, 1):
            print(f"{idx}. {curso['nome']}")

        try:
            escolha = int(input("\nEscolha o número do curso: ")) - 1
            if 0 <= escolha < len(self.cursos):
                curso = self.cursos[escolha]
                nome_modulo = input("Nome do módulo: ").strip()
                descricao = input("Descrição do módulo: ").strip()

                self.modulos.append({
                    'curso': curso['nome'],
                    'modulo': nome_modulo,
                    'descricao': descricao
                })
                self.salvar_dados('modulos.json', self.modulos)
                print("\nMódulo cadastrado com sucesso!")
            else:
                print("Opção inválida!")
        except ValueError:
            print("Por favor, digite um número válido!")
        time.sleep(2)

    def ver_modulos_curso(self):
        """Visualiza os módulos de um curso específico"""
        self.exibir_cabecalho("Visualização de Módulos")

        if not self.cursos:
            print("Não há cursos cadastrados!")
            time.sleep(2)
            return

        print("\nCursos disponíveis:")
        for idx, curso in enumerate(self.cursos, 1):
            print(f"{idx}. {curso['nome']}")

        try:
            escolha = int(input("\nEscolha o número do curso: ")) - 1
            if 0 <= escolha < len(self.cursos):
                curso = self.cursos[escolha]
                modulos_curso = [m for m in self.modulos if m['curso'] == curso['nome']]
                
                if modulos_curso:
                    print(f"\nMódulos do curso '{curso['nome']}':")
                    for modulo in modulos_curso:
                        print(f"\nMódulo: {modulo['modulo']}")
                        print(f"Descrição: {modulo['descricao']}")
                else:
                    print("\nEste curso ainda não possui módulos cadastrados.")
            else:
                print("Opção inválida!")
        except ValueError:
            print("Por favor, digite um número válido!")
        
        input("\nPressione Enter para continuar...")

    def informacoes_seguranca(self):
        """Exibe informações sobre segurança do sistema"""
        self.exibir_cabecalho("Informações de Segurança")
        print("\nDicas de Segurança:")
        print("\n1. Proteção de Dados:")
        print("   - Seus dados pessoais são criptografados")
        print("   - Utilizamos hash SHA-256 para senhas")
        print("   - Informações sensíveis são protegidas")
        
        print("\n2. Boas Práticas:")
        print("   - Use senhas fortes (letras, números e símbolos)")
        print("   - Não compartilhe suas credenciais")
        print("   - Troque sua senha regularmente")
        print("   - Faça logout após usar o sistema")
        
        print("\n3. Recomendações:")
        print("   - Evite acessar em redes públicas")
        print("   - Mantenha seu email atualizado")
        print("   - Reporte atividades suspeitas")
        print("   - Não salve senhas no navegador")

        input("\nPressione Enter para voltar ao menu principal...")

    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            self.exibir_cabecalho("Sistema Educacional")
            print("\nOpções disponíveis:")
            print("1. Fazer Cadastro")
            print("2. Fazer Login")
            print("3. Acessar Cursos")
            print("4. Cadastrar Cursos")
            print("5. Cadastrar Módulos dos Cursos")
            print("6. Ver Módulos de um Curso")
            print("7. Informações de Segurança")
            print("8. Sair")

            opcao = input("\nEscolha uma opção: ")

            if opcao == '1':
                self.fazer_cadastro()
            elif opcao == '2':
                self.fazer_login()
            elif opcao == '3':
                self.menu_cursos()
            elif opcao == '4':
                self.cadastrar_cursos()
            elif opcao == '5':
                self.cadastrar_modulos()
            elif opcao == '6':
                self.ver_modulos_curso()
            elif opcao == '7':
                self.informacoes_seguranca()
            elif opcao == '8':
                print("\nSaindo do sistema. Até logo!")
                time.sleep(1)
                break
            else:
                print("\nOpção inválida. Tente novamente.")
                time.sleep(1)
if __name__ == "__main__":
    try:
        sistema = SistemaEducacional()
        sistema.menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma encerrado pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
    def validar_email(self, email):
        """Valida o formato do email usando regex"""
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email)

    def menu_cursos(self):
        """Exibe e gerencia o menu de cursos"""
        if not self.cursos:
            print("\nNenhum curso disponível no momento.")
            time.sleep(2)
            return

        while True:
            self.exibir_cabecalho("Cursos Disponíveis")
            for idx, curso in enumerate(self.cursos, 1):
                print(f"{idx}. {curso['nome']}")
            
            print("\n0. Voltar ao menu principal")
            escolha = input("\nEscolha um curso para ver os módulos: ")

            if escolha == '0':
                break

            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(self.cursos):
                    self.acessar_modulos(self.cursos[idx]['nome'])
                else:
                    print("Opção inválida!")
                    time.sleep(1)
            except ValueError:
                print("Por favor, digite um número válido!")
                time.sleep(1)

    