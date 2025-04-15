# ======= services/usuarios.py =======
import json, os, bcrypt
from utils.validacoes import validar_email, validar_senha, validar_cpf

def carregar_usuarios():
    try:
        with open('data/usuarios.json', 'r') as file:
            return json.load(file)
    except:
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

    while True:
        cpf = input('Digite seu CPF (apenas números, ex: 12345678900): ')
        if not validar_cpf(cpf):
            print('CPF inválido. Tente novamente.')
        elif any(u['cpf'] == cpf for u in usuarios):
            print('CPF já cadastrado.')
            return
        else:
            break

    nome = input('Nome completo: ')

    while True:
        email = input('E-mail (ex: nome@email.com): ')
        if validar_email(email):
            break
        print('E-mail inválido. Tente novamente.')

    while True:
        senha = input('Senha (mínimo 8 caracteres, com maiúscula, minúscula, número e símbolo): ')
        if validar_senha(senha):
            break
        print('Senha fraca. Tente novamente.')

    while True:
        perfil = input('Perfil (Aluno ou Administrador): ').capitalize()
        if perfil in ['Aluno', 'Administrador']:
            break
        print('Perfil inválido. Tente novamente.')

    senha_hash = hash_senha(senha)
    usuarios.append({ 'cpf': cpf, 'nome': nome, 'email': email, 'senha': senha_hash, 'perfil': perfil })
    salvar_usuarios(usuarios)
    print('Usuário cadastrado com sucesso!')

def autenticar():
    usuarios = carregar_usuarios()
    cpf = input('CPF: ')
    senha = input('Senha: ')
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)

    if usuario and verificar_senha(senha, usuario['senha']):
        print(f"Bem-vindo, {usuario['nome']} ({usuario['perfil']})")
        return usuario
    else:
        print('CPF ou senha inválidos.')
        return None