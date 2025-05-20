import os

def gerar_certificado(usuario):
    from services.conteudos import carregar_conteudos
    from services.quiz import carregar_resultados
    from datetime import datetime

    conteudos = carregar_conteudos()
    resultados = carregar_resultados()

    temas = set(c['tema'] for c in conteudos)
    certificados_gerados = 0

    for tema in temas:
        modulos_do_tema = [c['titulo'] for c in conteudos if c['tema'] == tema]
        resultados_usuario = [r for r in resultados if r['cpf'] == usuario['cpf'] and r['conteudo'] in modulos_do_tema]

        if len(resultados_usuario) == len(modulos_do_tema):
            media = round(sum(r['acertos'] for r in resultados_usuario) / len(resultados_usuario), 2)
            data = datetime.now().strftime('%d/%m/%Y')
            certificado = (
                f"==============================\n"
                f"    CERTIFICADO DE CONCLUSÃO\n"
                f"==============================\n"
                f"Aluno: {usuario['nome']}\n"
                f"Tema: {tema}\n"
                f"Data: {data}\n"
                f"Média de Desempenho: {media}/10\n"
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
        print("Você ainda não concluiu nenhum tema completamente para gerar certificado.")