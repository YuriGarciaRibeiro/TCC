import os
import subprocess
from time import sleep

input_dir = os.path.expanduser('')
output_dir = os.path.expanduser('')
 
for raiz, _, arquivos in os.walk(input_dir, topdown=False):
    for video in arquivos[::-1]:
        if video.endswith('.mp4'):
            video_dir = os.path.join(raiz, video)
            pasta = raiz.split('/')[-1]
            arquivo = '/input/' + pasta + '/' + video
            
            command = [
                'docker', 'exec', '-it', 'openface', '/bin/bash', '-c',
                f'build/bin/FeatureExtraction -f {arquivo} -out_dir /output/{pasta}/{video}'
            ]
            
            subprocess.run(command, cwd=raiz, check=True)
            
            print('================================================================================')
            input('salve')

print("Processamento concluído.")
