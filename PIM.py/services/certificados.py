import os
from datetime import datetime

def gerar_certificado(usuario):
    from services.conteudos import carregar_conteudos
    from services.quiz import carregar_resultados
    from services.leitura import carregar_leituras

    conteudos = carregar_conteudos()
    resultados = carregar_resultados()
    leituras = carregar_leituras()

    temas = set(c['tema'] for c in conteudos)
    certificados_gerados = 0

    for tema in temas:
        modulos = [c for c in conteudos if c['tema'] == tema]
        titulos_modulos = [m['titulo'] for m in modulos]

        # Verificar se o aluno leu todos os conteúdos do tema
        usuario_leitura = next((l for l in leituras if l['nome'] == usuario['nome']), None)
        if not usuario_leitura:
            continue

        conteudos_lidos = usuario_leitura.get('conteudos_vistos', [])
        if not all(t in conteudos_lidos for t in titulos_modulos):
            continue

        # Verificar se o aluno fez todas as provas
        resultados_usuario = [r for r in resultados if r['cpf'] == usuario['cpf'] and r['conteudo'] in titulos_modulos]
        if len(resultados_usuario) < len(titulos_modulos):
            continue

        media = round(sum(r['acertos'] for r in resultados_usuario) / len(resultados_usuario), 2)
        
        data = datetime.now().strftime('%d/%m/%Y')
        certificado = (
            f"==============================\n"
            f"    CERTIFICADO DE CONCLUSÃO\n"
            f"==============================\n"
            f"Aluno: {usuario['nome']}\n"
            f"Tema: {tema}\n"
            f"Data: {data}\n"
            f"Média de Desempenho: {media}/2\n"
            f"\nParabéns pela sua dedicação e empenho!\n"
            f"Assinado: Plataforma Educação Segura\n"
        )

        os.makedirs('certificados', exist_ok=True)
        caminho = f"certificados/certificado_{usuario['nome'].replace(' ', '_')}_{tema.replace(' ', '_')}.txt"
        with open(caminho, 'w', encoding='utf-8') as file:
            file.write(certificado)

        certificados_gerados += 1
        print(f"✅ Certificado gerado para o tema '{tema}' em: {caminho}")

    if certificados_gerados == 0:
        print("Você ainda não completou todos os requisitos para emitir certificados.")