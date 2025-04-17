import os
import shutil


def copiar_arquivos(origem, destino, extensao=None):
    """
    Copia arquivos da pasta origem (e subpastas) para a pasta destino.

    :param origem: Caminho da pasta de origem
    :param destino: Caminho da pasta de destino
    :param extensao: Extensão dos arquivos a copiar (sem ponto, ex: 'usd'). Se None, copia todos os arquivos.
    """
    if not os.path.exists(destino):
        os.makedirs(destino)

    for raiz, _, arquivos in os.walk(origem):
        for arquivo in arquivos:
            if extensao is None or arquivo.lower().endswith(f".{extensao.lower()}"):
                caminho_origem = os.path.join(raiz, arquivo)
                caminho_destino = os.path.join(destino, arquivo)

                # Se já existir um arquivo com o mesmo nome, renomeia
                contador = 1
                while os.path.exists(caminho_destino):
                    nome_base, ext = os.path.splitext(arquivo)
                    caminho_destino = os.path.join(
                        destino, f"{nome_base}_{contador}{ext}"
                    )
                    contador += 1

                shutil.copy2(caminho_origem, caminho_destino)
                print(f"Copiado: {caminho_origem} -> {caminho_destino}")


if __name__ == "__main__":
    origem = r"C:\Users\yurig\Documents\GitHub\TCC\dataset"
    destino = r"C:\Users\yurig\Documents\GitHub\TCC\animations"
    copiar_arquivos(origem, destino, extensao="usd")
