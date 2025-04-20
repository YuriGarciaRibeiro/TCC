import os

from config.constants import (
    emotional_intensity,
    emotions,
    modalities,
    repetition,
    statements,
    vocal_channel,
    DATASET_DIR,
)


def rename_videos(pasta):
    for raiz, _, arquivos in os.walk(pasta, topdown=False):
        for arquivo in arquivos:
            if arquivo.startswith("01") or arquivo.startswith("03"):
                partes = arquivo.split("-")

                novo_nome = (
                    modalities.get(partes[0]) + "-" +
                    vocal_channel.get(partes[1]) + "-" +
                    emotions.get(partes[2]) + "-" +
                    emotional_intensity.get(partes[3]) + "-" +
                    statements.get(partes[4]).replace(" ", "-") + "-" +
                    repetition.get(partes[5]).replace(" ", "-") + "-" +
                    "actor" + partes[6]
                )

                caminho_antigo = os.path.join(raiz, arquivo)
                caminho_novo = os.path.join(raiz, novo_nome)
                os.rename(caminho_antigo, caminho_novo)

                partes[6] = partes[6].replace(".mp4", "").replace(".wav", "")
                ator_path = os.path.join(pasta, f"Actor{partes[6]}")

                os.makedirs(ator_path, exist_ok=True)

                final_path = os.path.join(ator_path, novo_nome)
                os.rename(caminho_novo, final_path)
                print(f"Arquivo {novo_nome} movido para a pasta Actor{partes[6]}")
            else:
                os.remove(os.path.join(raiz, arquivo))
                print(f"Arquivo {arquivo} removido")

        if not os.listdir(raiz):
            print(f"Pasta {raiz} vazia")
            os.rmdir(raiz)
            print(f"Pasta {raiz} removida")


def main(pasta=DATASET_DIR):
    rename_videos(pasta)


if __name__ == "__main__":
    main()
