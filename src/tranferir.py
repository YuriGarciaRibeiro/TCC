import os
import shutil

def copiar_videos_mp4(pasta_origem, pasta_destino):
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    for raiz, dirs, arquivos in os.walk(pasta_origem):
        for arquivo in arquivos:
            if arquivo.lower().endswith('.mp4'):
                caminho_origem = os.path.join(raiz, arquivo)
                caminho_destino = os.path.join(pasta_destino, arquivo)
                
                if not os.path.exists(caminho_destino):
                    shutil.copy(caminho_origem, caminho_destino)
                    print(f'Arquivo copiado: {arquivo}')
                else:
                    print(f'O arquivo {arquivo} já existe na pasta de destino.')

pasta_origem = '' # Substitua com o caminho correto
pasta_destino = ''  # Substitua com o caminho desejado

# Chamar a função
copiar_videos_mp4(pasta_origem, pasta_destino)
