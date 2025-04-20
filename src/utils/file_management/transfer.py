import os
import logging

from config.constants import SRC_DIR, TEST_DIR, VIDEO_EXTENSION
from utils.file_operations import safe_copy, safe_mkdir

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def copiar_arquivos(origem, destino, extensao=None):
    """
    Copia arquivos da pasta origem (e subpastas) para a pasta destino.

    :param origem: Caminho da pasta de origem
    :param destino: Caminho da pasta de destino
    :param extensao: Extensão dos arquivos a copiar (sem ponto, ex: 'py'). Se None, copia todos os arquivos.
    """
    safe_mkdir(destino)

    for raiz, _, arquivos in os.walk(origem):
        logging.info(f"Processando diretório: {raiz}")
        for arquivo in arquivos:
            if extensao is None or arquivo.lower().endswith(f".{extensao.lower()}"):
                caminho_origem = os.path.join(raiz, arquivo)
                caminho_destino = os.path.join(destino, arquivo)

                # Se já existir um arquivo com o mesmo nome, renomeia
                contador = 1
                while os.path.exists(caminho_destino):
                    nome_base, ext = os.path.splitext(arquivo)
                    caminho_destino = os.path.join(destino, f"{nome_base}_{contador}{ext}")
                    contador += 1

                safe_copy(caminho_origem, caminho_destino)
                logging.info(f"Copiado: {caminho_origem} -> {caminho_destino}")

def main():
    copiar_arquivos(SRC_DIR, TEST_DIR, VIDEO_EXTENSION.strip("."))  # exemplo com .mp4

if __name__ == "__main__":
    main()
