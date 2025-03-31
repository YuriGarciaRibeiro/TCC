import os

modalities = {"01": "full-AV", "02": "video-only", "03": "audio-only"}


vocal_channel = {"01": "speech", "02": "song"}


emotions = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised",
}

emotional_intensity = {"01": "normal", "02": "strong"}

statement = {"01": "Kids are talking by the door", "02": "Dogs are sitting by the door"}

repetition = {"01": "1st repetition", "02": "2nd repetition"}

"""
Modality (01 = full-AV, 02 = video-only, 03 = audio-only).
Vocal channel (01 = speech, 02 = song).
Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the ‘neutral’ emotion.
Statement (01 = “Kids are talking by the door”, 02 = “Dogs are sitting by the door”).
Repetition (01 = 1st repetition, 02 = 2nd repetition).
Actor (01 to 24. Odd numbered actors are male, even numbered actors are female).
"""


pasta_principal = "C:/Users/yurig/Documents/GitHub/TCC/Dataset"


def renomear_videos(pasta):
    for raiz, _, arquivos in os.walk(pasta, topdown=False):
        for arquivo in arquivos:
            if arquivo.startswith("01") or arquivo.startswith("03"):
                novo_nome = ""
                partes = arquivo.split("-")
                novo_nome += modalities.get(partes[0])
                novo_nome += "-"
                novo_nome += vocal_channel.get(partes[1])
                novo_nome += "-"
                novo_nome += emotions.get(partes[2])
                novo_nome += "-"
                novo_nome += emotional_intensity.get(partes[3])
                novo_nome += "-"
                novo_nome += statement.get(partes[4]).replace(" ", "-")
                novo_nome += "-"
                novo_nome += repetition.get(partes[5]).replace(" ", "-")
                novo_nome += "-"
                novo_nome += "actor"
                novo_nome += partes[6]
                novo_nome.replace("-", "_")
                caminho_antigo = os.path.join(raiz, arquivo)
                caminho_novo = os.path.join(raiz, novo_nome)
                os.rename(caminho_antigo, caminho_novo)
                # move o arquivo para a pasta principal

                partes[6] = partes[6].replace(".mp4", "")
                partes[6] = partes[6].replace(".wav", "")

                # verifica se na pasta raiz tem alguma pasta com o nome do ator atual
                if not os.path.exists(os.path.join(pasta, f"Actor{partes[6]}")):
                    os.mkdir(os.path.join(pasta, f"Actor{partes[6]}"))
                    print(f"Actor{partes[6]} criada")
                    os.rename(
                        caminho_novo,
                        os.path.join(pasta, f"Actor{partes[6]}", novo_nome),
                    )
                    print(f"Arquivo {novo_nome} movido para a pasta Actor{partes[6]}")
                else:
                    os.rename(
                        caminho_novo,
                        os.path.join(pasta, f"Actor{partes[6]}", novo_nome),
                    )
                    print(f"Arquivo {novo_nome} movido para a pasta Actor{partes[6]}")

                if not os.listdir(raiz):
                    print(f"Pasta {raiz} vazia")
                    os.rmdir(raiz)
                    print(f"Pasta {raiz} removida")
            else:
                os.remove(os.path.join(raiz, arquivo))
                print(f"Arquivo {arquivo} removido")
                # se a pasta ficar vazia, remove
                if not os.listdir(raiz):
                    print(f"Pasta {raiz} vazia")
                    os.rmdir(raiz)
                    print(f"Pasta {raiz} removida")


renomear_videos(pasta_principal)
