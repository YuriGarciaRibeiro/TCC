
# ? (Análise de Emoções por Predominância de AUs)
# ? AEPA

import os
import re
import pandas as pd
from emotion_aus import emotions_au
from generate_plot import generate_plot  # Importa a função de geração do plot

def list_all_files_in_directory(directory_path):
    all_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                all_files.append(os.path.join(root, file))
    return all_files

def break_string(s):
    pattern = r"(?P<type>full-AV-speech)-(?P<emotion>\w+)-(?P<intensity>\w+)-(?P<phrase>[\w\s-]+)-(?P<repetition>\d+[a-zA-Z-]+)-(?P<actor>actor\d+)"
    result = re.match(pattern, s)
    if result:
        return result.groupdict()
    else:
        return None

def analyze_video_emotions(video_path, threshold=2):
    df = pd.read_csv(video_path)
    filtered_df = df[[col for col in df.columns if col.startswith(" AU") and col.endswith("r")]]
    frame_emotions = {}
    emotion_counts = {emotion: 0 for emotion in emotions_au}
    dominant_frame = 0

    for idx, row in filtered_df.iterrows():
        emotion_sums = {emotion: 0 for emotion in emotions_au}
        for emotion, aus in emotions_au.items():
            for au in aus:
                col_name = f" AU{au:02}_r"
                if col_name in row and row[col_name] > threshold:
                    emotion_sums[emotion] += row[col_name]
        dominant_emotion = max(emotion_sums, key=emotion_sums.get)
        frame_emotions[idx] = dominant_emotion
        emotion_counts[dominant_emotion] += 1
        if emotion_sums[dominant_emotion] > emotion_sums.get(dominant_frame, 0):
            dominant_frame = idx

    dominant_frame_path = f"{video_path.replace('.csv', '')}_aligned/frame_det_00_{str(dominant_frame+1).zfill(6)}.bmp"
    dominant_emotion_video = max(emotion_counts, key=emotion_counts.get)
    video_name = os.path.basename(video_path)
    data = break_string(video_name)

    # Retorna os dados para o plot
    return {
        "emotion_counts": emotion_counts,
        "dominant_emotion_video": dominant_emotion_video,
        "dominant_frame": dominant_frame,
        "dominant_frame_path": dominant_frame_path,
        "video_name": video_name,
        "data": data
    }

if __name__ == "__main__":
    # Caminho da pasta onde estão os vídeos
    video_directory = "/Users/yurigarciaribeiro/Documents/GitHub/TCC/dataset"

    # Obter todos os arquivos CSV recursivamente
    video_files = list_all_files_in_directory(video_directory)

    # Rodar a função para cada arquivo de vídeo (CSV)
    for video in video_files:
        if video.endswith(".csv"):  # Verifique se o arquivo é CSV
            analysis_result = analyze_video_emotions(video, threshold=0.7)  # Analisa o vídeo
            generate_plot(analysis_result,"AEPA")  # Gera o plot com os dados analisados