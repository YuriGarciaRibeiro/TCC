import os
import shutil
import subprocess
from time import sleep

input_dir = os.path.expanduser('/Users/yurigarciaribeiro/Documents/TCC/DockerC/input')
output_dir = os.path.expanduser('/Users/yurigarciaribeiro/Documents/TCC/DockerC/output')
 
 
for raiz, _, arquivos in os.walk(input_dir, topdown=False):
    print(f"{arquivos[::-1]}")
    for video in arquivos[::-1]:
        if video.endswith('.mp4'):
            video_dir = os.path.join(raiz, video)
            pasta = raiz.split('/')[-1]
            arquivo = '/input/' + pasta + '/' + video
            
            command = [
                'docker', 'exec', '-it', 'openface', '/bin/bash', '-c',
                f'build/bin/FeatureExtraction -f {arquivo} -out_dir /output/{pasta}/{video.replace(".mp4", "")}'
            ]
            
            subprocess.run(command, cwd=raiz, check=True)
            
            # copa o arquivo para a pasta de saída
            shutil.copy2(os.path.join(raiz, video), os.path.join(output_dir, raiz.split('/')[-1], video))
            print(f"Arquivo {video} copiado para a pasta de saída")
        elif video.endswith('.wav'):
            #copia o arquivo para a pasta de saída
            shutil.copy2(os.path.join(raiz, video), os.path.join(output_dir, raiz.split('/')[-1], video))
            print(f"Arquivo {video} copiado para a pasta de saída")
            
print("Processamento concluído.")
