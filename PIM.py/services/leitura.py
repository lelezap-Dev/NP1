import json
import os

def carregar_leituras():
    try:
        with open('data/leitura_conteudos.json', 'r') as file:
            return json.load(file)
    except:
        return []

def salvar_leituras(leituras):
    os.makedirs('data', exist_ok=True)
    with open('data/leitura_conteudos.json', 'w') as file:
        json.dump(leituras, file, indent=4, ensure_ascii=False)

def registrar_leitura(nome, conteudo):
    leituras = carregar_leituras()
    usuario = next((u for u in leituras if u['nome'] == nome), None)

    if not usuario:
        leituras.append({"nome": nome, "conteudos_vistos": [conteudo]})
    else:
        if conteudo not in usuario['conteudos_vistos']:
            usuario['conteudos_vistos'].append(conteudo)

    salvar_leituras(leituras)

def ja_visualizou_conteudo(nome, conteudo):
    leituras = carregar_leituras()
    usuario = next((u for u in leituras if u['nome'] == nome), None)
    return usuario and conteudo in usuario['conteudos_vistos']
