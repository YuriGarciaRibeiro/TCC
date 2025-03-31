import os
import shutil

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


url_base = "C:/Users/yurig/Documents/GitHub/TCC/Dataset"

# Lista de composições
composicoes = [
    ["01", "01", "03", "02", "01", "01"],  # Composição 1 (mp4)
    ["01", "01", "05", "02", "01", "01"],  # Composição 2 (mp4)
    ["03", "01", "03", "02", "01", "01"],  # Composição 3 (wav)
    ["03", "01", "05", "02", "01", "01"],  # Composição 4 (wav)
]

# Loop de 1 a 24
for i in range(1, 25):
    # Adiciona zero à esquerda para números menores que 10
    if i < 10:
        i = f"0{i}"

    pasta_destino = f"C:/Users/yurig/Documents/GitHub/TCC/filtrado/Actor{i}"
    nome_pasta = f"Actor{i}"

    # Cria a pasta do ator se não existir
    if not os.path.exists(pasta_destino):
        os.mkdir(pasta_destino)

    # Itera sobre as composições
    for composicao in composicoes:
        # Determina a extensão do arquivo com base no primeiro número da composição
        extensao = ".wav" if composicao[0] == "03" else ".mp4"

        # Gera o nome do arquivo com base na composição atual
        nome_arquivo = f"{modalities[composicao[0]]}-{vocal_channel[composicao[1]]}-{emotions[composicao[2]]}-{emotional_intensity[composicao[3]]}-{statement[composicao[4]]}-{repetition[composicao[5]]}-actor{i}{extensao}"

        caminho_pasta = os.path.join(url_base, nome_pasta)
        caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo).replace(" ", "-")

        # Verifica se o arquivo existe e copia para a pasta de destino
        if os.path.exists(caminho_arquivo):
            print(f"Arquivo {nome_arquivo} encontrado")
            shutil.copy(caminho_arquivo, pasta_destino)
