# ======= utils/validacoes.py =======
import re

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.match(padrao, email)

def validar_senha(senha):
    return (len(senha) >= 8 and any(c.isupper() for c in senha)
            and any(c.islower() for c in senha)
            and any(c.isdigit() for c in senha)
            and any(c in "!@#$%^&*()-_+=" for c in senha))

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11