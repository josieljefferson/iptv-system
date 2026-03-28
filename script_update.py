import requests
import os
from m3u_processor import processar_lista

# 🔗 API do GitHub
API_URL = "https://api.github.com/repos/josieljefferson/iptv-system/contents/"

PASTA = "downloads"
OUTPUT = "docs"

os.makedirs(PASTA, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

def listar_arquivos():
    r = requests.get(API_URL)
    arquivos = []

    for item in r.json():
        nome = item["name"]
        if nome.endswith((".m3u", ".m3u8", ".txt")):
            arquivos.append(item["download_url"])

    return arquivos

def baixar_arquivos(urls):
    for url in urls:
        nome = url.split("/")[-1]
        caminho = os.path.join(PASTA, nome)

        print(f"⬇️ {nome}")

        try:
            r = requests.get(url, timeout=15)
            with open(caminho, "wb") as f:
                f.write(r.content)
        except:
            print(f"❌ erro: {nome}")

def gerar_epg():
    # exemplo simples (pode integrar real depois)
    epg = {
        "channels": []
    }

    with open("epg.json", "w") as f:
        import json
        json.dump(epg, f)

def main():
    urls = listar_arquivos()
    baixar_arquivos(urls)
    canais = processar_lista(PASTA, OUTPUT)

    # salvar JSON
    import json
    with open(os.path.join(OUTPUT, "playlists.json"), "w") as f:
        json.dump(canais, f, indent=2)

    gerar_epg()

    print("✅ Tudo atualizado")

if __name__ == "__main__":
    main()