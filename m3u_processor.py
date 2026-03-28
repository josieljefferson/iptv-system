import os

def processar_lista(pasta_entrada, pasta_saida):
    urls = set()
    canais = []

    for arquivo in os.listdir(pasta_entrada):
        with open(os.path.join(pasta_entrada, arquivo), "r", encoding="utf-8", errors="ignore") as f:
            nome = None

            for linha in f:
                linha = linha.strip()

                if linha.startswith("#EXTINF"):
                    nome = linha.split(",")[-1]

                elif linha.startswith("http"):
                    if linha not in urls:
                        urls.add(linha)

                        canais.append({
                            "nome": nome,
                            "url": linha
                        })

    # salvar M3U
    with open(os.path.join(pasta_saida, "final.m3u"), "w") as f:
        f.write("#EXTM3U\n")
        for c in canais:
            f.write(f"#EXTINF:-1,{c['nome']}\n{c['url']}\n")

    return canais