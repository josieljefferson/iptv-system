import os
import re

# ✅ Regex corrigido (aceita hífen)
regex_attr = re.compile(r'([\w\-]+)="(.*?)"')

# ✅ Lista de EPG organizada
EPG_URLS = [
    "https://m3u4u.com/epg/jq2zy9epr3bwxmgwyxr5",
    "https://m3u4u.com/epg/3wk1y24kx7uzdevxygz7",
    "https://m3u4u.com/epg/782dyqdrqkh1xegen4zp",
    "https://www.open-epg.com/files/brazil1.xml.gz",
    "https://www.open-epg.com/files/brazil2.xml.gz",
    "https://www.open-epg.com/files/brazil3.xml.gz",
    "https://www.open-epg.com/files/brazil4.xml.gz",
    "https://www.open-epg.com/files/portugal1.xml.gz",
    "https://www.open-epg.com/files/portugal2.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz"
]

def extrair_atributos(linha):
    attrs = dict(regex_attr.findall(linha))
    return {
        "tvg_id": attrs.get("tvg-id", ""),
        "tvg_name": attrs.get("tvg-name", ""),
        "tvg_logo": attrs.get("tvg-logo", ""),
        "group": attrs.get("group-title", "OUTROS")
    }

def extrair_nome(linha):
    return linha.split(",")[-1].strip() if "," in linha else "Sem Nome"

def limpar_texto(txt):
    return txt.strip() if txt else ""

def processar_lista(pasta_entrada, pasta_saida):
    urls_vistas = set()
    canais = []

    for arquivo in os.listdir(pasta_entrada):
        caminho = os.path.join(pasta_entrada, arquivo)

        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            dados_extinf = None

            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                if linha.startswith("#EXTINF"):
                    attrs = extrair_atributos(linha)
                    nome = extrair_nome(linha)

                    dados_extinf = {
                        "nome": limpar_texto(nome) or "Sem Nome",
                        "tvg_id": limpar_texto(attrs["tvg_id"]),
                        "tvg_name": limpar_texto(attrs["tvg_name"]) or nome,
                        "tvg_logo": limpar_texto(attrs["tvg_logo"]),
                        "group": limpar_texto(attrs["group"]) or "OUTROS"
                    }

                elif linha.startswith("http"):
                    if linha not in urls_vistas:
                        urls_vistas.add(linha)

                        canal = dados_extinf.copy() if dados_extinf else {
                            "nome": "Sem Nome",
                            "tvg_id": "",
                            "tvg_name": "Sem Nome",
                            "tvg_logo": "",
                            "group": "OUTROS"
                        }

                        canal["url"] = linha
                        canais.append(canal)

                    dados_extinf = None

    # 🚀 HEADER PROFISSIONAL
    epg_string = ",".join(EPG_URLS)

    header = (
        f'#EXTM3U url-tvg="{epg_string}"\n'
        '#PLAYLISTV: '
        'pltv-logo="https://cdn-icons-png.flaticon.com/256/25/25231.png" '
        'pltv-name="☆Josiel Jefferson☆" '
        'pltv-description="Playlist GitHub Pages" '
        'pltv-cover="https://images.icon-icons.com/2407/PNG/512/gitlab_icon_146171.png" '
        'pltv-author="☆Josiel Jefferson☆" '
        'pltv-site="https://josieljefferson12.github.io/" '
        'pltv-email="josielluz@proton.me"\n'
    )

    # 💾 salvar
    caminho_saida = os.path.join(pasta_saida, "playlists.m3u")

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(header)

        for c in canais:
            f.write(
                f'#EXTINF:-1 tvg-id="{c["tvg_id"]}" '
                f'tvg-name="{c["tvg_name"]}" '
                f'tvg-logo="{c["tvg_logo"]}" '
                f'group-title="{c["group"]}",{c["nome"]}\n'
            )
            f.write(c["url"] + "\n\n")

    return canais