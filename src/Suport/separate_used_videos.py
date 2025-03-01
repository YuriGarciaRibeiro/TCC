import os
import shutil
from Suport.constants import *

url_base = ""

composicao1 = ["01" ,"01", "03", "02", "01", "01"]

composicao2 = ["01", "01", "05", "02", "01", "01"]

# for 1 ao 24
for i in range(1, 25):
    # zero a esquerda
    if i < 10:
        i = f"0{i}"
    
    pasta_destino = f"/Users/yurigarciaribeiro/Documents/TCC/Usados/Actor{i}"
    nome_pasta = f"Actor{i}"
    nome_arquivo1 = f"{modalities[composicao1[0]]}-{vocal_channel[composicao1[1]]}-{emotions[composicao1[2]]}-{emotional_intensity[composicao1[3]]}-{statement[composicao1[4]]}-{repetition[composicao1[5]]}-actor{i}.mp4"
    nome_arquivo2 = f"{modalities[composicao2[0]]}-{vocal_channel[composicao2[1]]}-{emotions[composicao2[2]]}-{emotional_intensity[composicao2[3]]}-{statement[composicao2[4]]}-{repetition[composicao2[5]]}-actor{i}.mp4"
    
    caminho_pasta = os.path.join(url_base, nome_pasta)
    caminho_arquivo1 = os.path.join(caminho_pasta, nome_arquivo1).replace(' ', '-')
    caminho_arquivo2 = os.path.join(caminho_pasta, nome_arquivo2).replace(' ', '-')
    
    
    # cria pasta do ator
    if not os.path.exists(pasta_destino):
        os.mkdir(pasta_destino)
        
    
    if os.path.exists(caminho_arquivo1):
        print(f"Arquivo {nome_arquivo1} encontrado")
        shutil.copy(caminho_arquivo1, pasta_destino)
    
    if os.path.exists(caminho_arquivo2):
        print(f"Arquivo {nome_arquivo2} encontrado")
        shutil.copy(caminho_arquivo2, pasta_destino)
        