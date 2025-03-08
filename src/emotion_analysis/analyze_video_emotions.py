import os

import matplotlib.pyplot as plt
import pandas as pd
from emotion_aus import emotions_au
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image


# Função para listar todos os arquivos recursivamente
def list_all_files_in_directory(directory_path):
    all_files = []

    # Percorre o diretório e subdiretórios
    for root, dirs, files in os.walk(directory_path):
        # Para cada arquivo, adiciona o caminho completo à lista
        for file in files:
            all_files.append(
                os.path.join(root, file)
            )  # Adiciona o caminho completo do arquivo

    return all_files


# Função para analisar as emoções em um vídeo
def analyze_video_emotions(video_path, threshold=0.6):
    # Carregar o CSV
    df = pd.read_csv(video_path)

    # Filtrar as colunas AU (intensidade)
    filtered_df = df[
        [col for col in df.columns if col.startswith(" AU") and col.endswith("r")]
    ]

    # Dicionário para armazenar as emoções atribuídas aos frames
    frame_emotions = {}

    # Criar um dicionário de contagem das emoções para visualização
    emotion_counts = {emotion: 0 for emotion in emotions_au}

    dominant_frame = 0

    # Iterar sobre as linhas e somar os AUs para cada emoção
    for idx, row in filtered_df.iterrows():
        # Dicionário para armazenar a soma das AUs por emoção
        emotion_sums = {emotion: 0 for emotion in emotions_au}

        # Somar os valores dos AUs associados a cada emoção
        for emotion, aus in emotions_au.items():
            for au in aus:
                col_name = f" AU{au:02}_r"
                if (
                    col_name in row and row[col_name] > threshold
                ):  # Verifica se o AU está ativo
                    emotion_sums[emotion] += row[col_name]

        # A emoção com a maior soma será a atribuída ao frame
        dominant_emotion = max(emotion_sums, key=emotion_sums.get)

        # Atribuir a emoção dominante ao frame
        frame_emotions[idx] = dominant_emotion

        # Atualizar a contagem de ativações das emoções
        emotion_counts[dominant_emotion] += 1

        # Atualizar o frame que teve a maior expressão emocional
        if emotion_sums[dominant_emotion] > emotion_sums.get(dominant_frame, 0):
            dominant_frame = idx

    # /Users/yurigarciaribeiro/Documents/TCC/DockerC/output/Actor01/full-AV-speech-angry-strong-Kids-are-talking-by-the-door-1st-repetition-actor01.mp4/full-AV-speech-angry-strong-Kids-are-talking-by-the-door-1st-repetition-actor01_aligned

    # Caminho da imagem do frame
    dominant_frame_path = f"{video_path.replace('.csv', '')}_aligned/frame_det_00_{str(dominant_frame).zfill(6)}.bmp"

    # Encontrar a emoção predominante no vídeo (a que mais apareceu)
    dominant_emotion_video = max(emotion_counts, key=emotion_counts.get)

    # Tamanho da figura
    plt.figure(figsize=(16, 6))  # Ajuste o tamanho conforme necessário

    # Cria uma grade de subplots: 1 linha, 2 colunas
    ax1 = plt.subplot(1, 2, 1)  # Subplot para o gráfico de barras
    ax2 = plt.subplot(1, 2, 2)  # Subplot para a imagem do frame

    # Título geral da figura
    video_name = os.path.basename(video_path)
    plt.suptitle(f"Contagem das Emoções ao Longo do Vídeo: {video_name}", fontsize=16)

    # Gráfico de barras no primeiro subplot
    ax1.bar(emotion_counts.keys(), emotion_counts.values())
    ax1.set_xlabel("Emoções")
    ax1.set_ylabel("Número de ativações")
    ax1.tick_params(axis="x", rotation=45)

    # Adiciona o texto da emoção predominante no subplot do gráfico de barras
    ax1.text(
        0.5,
        1.1,
        f"Emoção predominante: {dominant_emotion_video}",
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax1.transAxes,
        fontsize=12,
        color="blue",
    )

    # Carrega a imagem do frame
    frame_image = Image.open(
        dominant_frame_path
    )  # Substitua pelo caminho correto da imagem
    frame_image = frame_image.resize((300, 300))  # Redimensiona a imagem, se necessário

    # Adiciona a imagem no segundo subplot
    imagebox = OffsetImage(frame_image, zoom=0.8)  # Ajuste o zoom conforme necessário
    ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False)
    ax2.add_artist(ab)

    # Adiciona o texto do frame com maior expressão emocional em cima da imagem
    ax2.text(
        0.5,
        1.05,
        f"Frame com maior expressão emocional: {dominant_frame}",
        horizontalalignment="center",
        verticalalignment="center",
        transform=ax2.transAxes,
        fontsize=12,
        color="green",
    )

    # Remove os eixos do subplot da imagem
    ax2.axis("off")

    # Ajusta o layout para evitar cortes
    plt.tight_layout()

    # Salva a figura
    # verifique se a pasta 'graphs' existe, se não, crie
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    # verifica se a pasta do ator existe, se não, cria
    if not os.path.exists(f"graphs/{video_name.replace('.csv','').split('-')[-1]}"):
        os.makedirs(f"graphs/{video_name.replace('.csv','').split('-')[-1]}")

    plt.savefig(
        f"graphs/{video_name.replace('.csv','').split('-')[-1]}/{video_name.replace('.csv', '')}.png"
    )
    plt.close()  # Fecha a figura
    # Exibe o gráfico
    # plt.show()


if __name__ == "__main__":
    # Caminho da pasta onde estão os vídeos
    video_directory = "C:/Users/yurig/Documents/GitHub/TCC/dataset"

    # Obter todos os arquivos CSV recursivamente
    video_files = list_all_files_in_directory(video_directory)

    # Rodar a função para cada arquivo de vídeo (CSV)
    for video in video_files:
        if video.endswith(".csv"):  # Verifique se o arquivo é CSV
            analyze_video_emotions(video)
