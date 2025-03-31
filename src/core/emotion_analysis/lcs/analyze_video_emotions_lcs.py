from pprint import pprint
import pandas as pd

from emotion_aus import EMOTION_TEMPLATES

# Definir os templates das emoções baseados nas AUs mais relevantes


def lcs(seq1, seq2):
    """Calcula a maior subsequência comum entre duas listas."""
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Construção da matriz LCS
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]  # Retorna o comprimento do LCS

def process_openface_csv(csv_file):
    """Lê o CSV do OpenFace e infere a emoção predominante."""
    df = pd.read_csv(csv_file)

    # Filtrar apenas as colunas de Action Units (AUs)
    au_columns = [col for col in df.columns if "AU" in col and "_r" in col]  # Usa AUs normalizadas
    print("=" * 50)
    print("AU columns:")
    pprint(au_columns)
    print("=" * 50)
    
    # Criar uma lista de sequências de AUs detectadas
    detected_au_sequences = []
    for _, row in df.iterrows():
        active_aus = [col.replace("_r", "") for col in au_columns if row[col] >= 2]  # Threshold de ativação
        if active_aus:
            detected_au_sequences.append(active_aus)
            
    print("=" * 50)
    print("Detected AU sequences:")
    pprint(detected_au_sequences)
    print("=" * 50)

    # Criar um dicionário para armazenar a pontuação de LCS para cada emoção
    emotion_scores = {emotion: 0 for emotion in EMOTION_TEMPLATES}

    # Comparar cada sequência detectada com os templates usando LCS
    for detected_sequence in detected_au_sequences:
        for emotion, template in EMOTION_TEMPLATES.items():
            lcs_var = lcs(detected_sequence, template)
            emotion_scores[emotion] += lcs_var

    # Determinar a emoção predominante
    predominant_emotion = max(emotion_scores, key=emotion_scores.get)
    return predominant_emotion, emotion_scores

# Exemplo de uso
csv_file = "/Users/yurigarciaribeiro/Documents/GitHub/TCC/dataset/Actor01/full-AV-speech-happy-strong-Kids-are-talking-by-the-door-1st-repetition-actor01/full-AV-speech-happy-strong-Kids-are-talking-by-the-door-1st-repetition-actor01.csv"  # Substitua pelo nome do seu arquivo
predicted_emotion, scores = process_openface_csv(csv_file)
print(f"Emoção predominante: {predicted_emotion}")
print("Pontuação LCS por emoção:", scores)