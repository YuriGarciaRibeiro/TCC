import os
from pathlib import Path
from pprint import pprint

import py_audio2face as pya2f


def process_audio_files(directory):
    a2f = pya2f.Audio2Face()
    # Percorre todos os arquivos e subpastas no diretório especificado
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Verifica se o arquivo é um arquivo .wav
            if file.endswith(".wav"):
                # Caminho completo do arquivo de áudio
                audio_file_path = os.path.join(root, file)

                # Caminho de saída com a mesma estrutura de diretórios e nome, mas com extensão .usd
                output_path = (
                    os.path.splitext(audio_file_path)[0] + "_animation" + ".usd"
                )
                a2f.a2e_set_settings(a2e_emotion_strength=1)
                # Executa a função a2f.audio2face_single
                final_path = a2f.audio2face_single(
                    audio_file_path=audio_file_path,
                    output_path=output_path,
                    fps=60,
                    emotion_auto_detect=True,
                )
                print(f"Processed: {audio_file_path} -> {final_path}")
    a2f.shutdown_a2f()


# Substitua 'your_directory_path' pelo caminho da pasta que você deseja processar
directory_path = r"C:\Users\yurig\Documents\GitHub\TCC\dataset"
process_audio_files(directory_path)
