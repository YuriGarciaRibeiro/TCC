import os
import pandas as pd
import matplotlib.pyplot as plt
from emotion_aus import emotions_au

# Função para listar todos os arquivos recursivamente
def list_all_files_in_directory(directory_path):
    all_files = []
    
    # Percorre o diretório e subdiretórios
    for root, dirs, files in os.walk(directory_path):
        # Para cada arquivo, adiciona o caminho completo à lista
        for file in files:
            all_files.append(os.path.join(root, file))  # Adiciona o caminho completo do arquivo
    
    return all_files

# Função para analisar as emoções em um vídeo
def analyze_video_emotions(video_path, threshold=0.6):
    # Carregar o CSV
    df = pd.read_csv(video_path)

    # Filtrar as colunas AU (intensidade)
    filtered_df = df[[col for col in df.columns if col.startswith(" AU") and col.endswith("r")]]

    # Dicionário para armazenar as emoções atribuídas aos frames
    frame_emotions = {}

    # Criar um dicionário de contagem das emoções para visualização
    emotion_counts = {emotion: 0 for emotion in emotions_au}

    # Iterar sobre as linhas e somar os AUs para cada emoção
    for idx, row in filtered_df.iterrows():
        # Dicionário para armazenar a soma das AUs por emoção
        emotion_sums = {emotion: 0 for emotion in emotions_au}

        # Somar os valores dos AUs associados a cada emoção
        for emotion, aus in emotions_au.items():
            for au in aus:
                col_name = f" AU{au:02}_r"
                if col_name in row and row[col_name] > threshold:  # Verifica se o AU está ativo
                    emotion_sums[emotion] += row[col_name]

        # A emoção com a maior soma será a atribuída ao frame
        dominant_emotion = max(emotion_sums, key=emotion_sums.get)

        # Atribuir a emoção dominante ao frame
        frame_emotions[idx] = dominant_emotion

        # Atualizar a contagem de ativações das emoções
        emotion_counts[dominant_emotion] += 1

    # Exibir as emoções atribuídas a cada frame (opcional)
    print(f"\nEmoções atribuídas a cada frame do vídeo {video_path}:")
    for idx, emotion in frame_emotions.items():
        print(f"Frame {idx}: {emotion}")

    # Exibir a contagem de ativações das emoções
    print("\nContagem de ativações das emoções:")
    print(emotion_counts)

    # Encontrar a emoção predominante no vídeo (a que mais apareceu)
    dominant_emotion_video = max(emotion_counts, key=emotion_counts.get)
    print(f"\nA emoção predominante no vídeo é: {dominant_emotion_video}")

    # Visualizar as contagens das emoções com um gráfico de barras
    plt.bar(emotion_counts.keys(), emotion_counts.values())
    plt.xlabel('Emoções')
    plt.ylabel('Número de ativações')
    plt.title(f'Contagem das Emoções ao Longo do Vídeo: {video_path}')
    plt.xticks(rotation=45)
    plt.show()

# Bloco para rodar a função para múltiplos arquivos
if __name__ == "__main__":
    # Caminho da pasta onde estão os vídeos
    video_directory = ""
    
    # Obter todos os arquivos CSV recursivamente
    video_files = list_all_files_in_directory(video_directory)

    # Rodar a função para cada arquivo de vídeo (CSV)
    for video in video_files:
        if video.endswith(".csv"):  # Verifique se o arquivo é CSV
            analyze_video_emotions(video)