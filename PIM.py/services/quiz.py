# ======= services/quiz.py =======
import json
from services.conteudos import carregar_conteudos

def carregar_resultados():
    try:
        with open('data/resultados.json', 'r') as file:
            return json.load(file)
    except:
        return []

def salvar_resultados(resultados):
    with open('data/resultados.json', 'w') as file:
        json.dump(resultados, file, indent=4)

def responder_conteudo(usuario):
    conteudos = carregar_conteudos()
    if not conteudos:
        print('Nenhum conteúdo disponível.')
        return

    for i, c in enumerate(conteudos):
        print(f"{i+1}. {c['titulo']} - {c['tema']}")
    try:
        escolha = int(input('Escolha o conteúdo: ')) - 1
        if escolha < 0 or escolha >= len(conteudos):
            print('Opção inválida.')
            return
    except ValueError:
        print('Entrada inválida.')
        return

    pontuacao = 0
    total = len(conteudos[escolha]['perguntas'])
    for p in conteudos[escolha]['perguntas']:
        print(f"\n{p['pergunta']}")
        for i, alt in enumerate(p['alternativas']):
            print(f"{i+1}. {alt}")
        try:
            resp = int(input('Sua resposta: ')) - 1
            if p['alternativas'][resp] == p['resposta_correta']:
                pontuacao += 1
        except (ValueError, IndexError):
            print('Resposta inválida.')

    print(f"Você acertou {pontuacao}/{total}!")
    resultados = carregar_resultados()
    resultados.append({ 'cpf': usuario['cpf'], 'conteudo': conteudos[escolha]['titulo'], 'acertos': pontuacao, 'total': total })
    salvar_resultados(resultados)

def relatorio_pessoal(cpf):
    resultados = carregar_resultados()
    user_results = [r for r in resultados if r['cpf'] == cpf]

    if not user_results:
        print('Nenhum resultado encontrado.')
        return

    acertos = [r['acertos'] for r in user_results]

    print('\n📋 Relatório de Desempenho:')
    print(f"- Total de Atividades Realizadas: {len(user_results)}")
    print(f"- Média de Acertos: {round(sum(acertos) / len(acertos), 2)}")
    print(f"- Maior Nota: {max(acertos)}")
    print(f"- Menor Nota: {min(acertos)}")
    print("\nContinue estudando para melhorar ainda mais! 🚀")

def relatorio_usuario(cpf):
    resultados = carregar_resultados()
    user_results = [r for r in resultados if r['cpf'] == cpf]
    if not user_results:
        print('Nenhum resultado encontrado.')
        return

    acertos = [r['acertos'] for r in user_results]
    relatorio = {
        'cpf': cpf,
        'total_atividades': len(user_results),
        'media_acertos': round(sum(acertos)/len(acertos), 2),
        'maior_nota': max(acertos),
        'menor_nota': min(acertos)
    }
    print(json.dumps(relatorio, indent=4))