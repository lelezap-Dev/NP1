# ======= services/relatorios.py =======
import os
import json
from services.quiz import carregar_resultados
from services.usuarios import carregar_usuarios

def exportar_relatorio_txt(cpf):
    resultados = carregar_resultados()
    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)

    if not usuario:
        print('Usuário não encontrado.')
        return

    user_results = [r for r in resultados if r['cpf'] == cpf]
    if not user_results:
        print('Nenhum resultado para exportar.')
        return

    os.makedirs('relatorios', exist_ok=True)
    caminho = f"relatorios/relatorio_{usuario['nome'].replace(' ', '_')}.txt"

    with open(caminho, 'w') as file:
        file.write(f"Relatório de Desempenho\n")
        file.write(f"Nome: {usuario['nome']}\n")
        file.write(f"CPF: {usuario['cpf']}\n")
        file.write(f"Perfil: {usuario['perfil']}\n")
        file.write("\nAtividades:\n")
        for r in user_results:
            file.write(f"- Conteúdo: {r['conteudo']} | Acertos: {r['acertos']} de {r['total']}\n")

        medias = [r['acertos'] for r in user_results]
        file.write("\nResumo:\n")
        file.write(f"Total de Atividades: {len(user_results)}\n")
        file.write(f"Média de Acertos: {round(sum(medias)/len(medias), 2)}\n")
        file.write(f"Maior Nota: {max(medias)}\n")
        file.write(f"Menor Nota: {min(medias)}\n")

    print(f'Relatório exportado com sucesso: {caminho}')

def exportar_relatorio_json(cpf):
    resultados = carregar_resultados()
    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)

    if not usuario:
        print('Usuário não encontrado.')
        return

    user_results = [r for r in resultados if r['cpf'] == cpf]
    if not user_results:
        print('Nenhum resultado para exportar.')
        return

    medias = [r['acertos'] for r in user_results]
    relatorio = {
        'nome': usuario['nome'],
        'cpf': usuario['cpf'],
        'perfil': usuario['perfil'],
        'atividades': user_results,
        'resumo': {
            'total_atividades': len(user_results),
            'media_acertos': round(sum(medias)/len(medias), 2),
            'maior_nota': max(medias),
            'menor_nota': min(medias)
        }
    }

    os.makedirs('relatorios', exist_ok=True)
    caminho = f"relatorios/relatorio_{usuario['nome'].replace(' ', '_')}.json"
    with open(caminho, 'w') as file:
        json.dump(relatorio, file, indent=4)

    print(f'Relatório JSON exportado com sucesso: {caminho}')