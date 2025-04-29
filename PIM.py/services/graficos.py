# ======= services/graficos.py =======
import matplotlib.pyplot as plt
from services.quiz import carregar_resultados
from services.usuarios import carregar_usuarios
from collections import defaultdict
import statistics

def gerar_grafico_media_usuarios():
    resultados = carregar_resultados()
    usuarios = carregar_usuarios()

    if not resultados:
        print("Nenhum dado disponível para gerar gráfico.")
        return

    nomes_usuarios = {u['cpf']: u['nome'] for u in usuarios}
    dados = defaultdict(list)
    for r in resultados:
        dados[nomes_usuarios.get(r['cpf'], r['cpf'])].append(r['acertos'])

    labels = list(dados.keys())
    medias = [round(sum(v)/len(v), 2) for v in dados.values()]
    todas_as_notas = [nota for sublist in dados.values() for nota in sublist]

    # Calcular moda, média e mediana geral
    media_geral = round(statistics.mean(todas_as_notas), 2)
    try:
        moda_geral = statistics.mode(todas_as_notas)
    except statistics.StatisticsError:
        moda_geral = 'Sem moda única'
    mediana_geral = statistics.median(todas_as_notas)

    plt.figure(figsize=(10,6))
    plt.bar(labels, medias, color='skyblue')
    plt.xlabel('Usuário')
    plt.ylabel('Média de Acertos')
    plt.title(f'Média | Moda: {moda_geral} | Mediana: {mediana_geral}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def gerar_grafico_distribuicao():
    resultados = carregar_resultados()
    if not resultados:
        print("Nenhum dado disponível.")
        return

    acertos = [r['acertos'] for r in resultados]
    plt.figure(figsize=(8,6))
    plt.hist(acertos, bins=range(min(acertos), max(acertos)+2), color='orange', edgecolor='black')
    plt.xlabel('Número de Acertos')
    plt.ylabel('Frequência')
    plt.title('Distribuição de Acertos')
    plt.tight_layout()
    plt.show()

def gerar_grafico_por_conteudo():
    resultados = carregar_resultados()
    if not resultados:
        print("Nenhum dado disponível.")
        return

    conteudos = defaultdict(list)
    for r in resultados:
        conteudos[r['conteudo']].append(r['acertos'])

    labels = list(conteudos.keys())
    medias = [statistics.mean(v) for v in conteudos.values()]

    plt.figure(figsize=(10,6))
    plt.bar(labels, medias, color='lightgreen')
    plt.xlabel('Conteúdo')
    plt.ylabel('Média de Acertos')
    plt.title('Desempenho Médio por Conteúdo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()