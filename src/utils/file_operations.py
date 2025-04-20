import os
import shutil
import pandas as pd
from pathlib import Path


def list_files_by_extension(directory, extension):
    """
    Retorna todos os arquivos com uma extensão em uma pasta (recursivo).
    """
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(directory)
        for file in files
        if file.lower().endswith(extension.lower())
    ]


def safe_mkdir(path):
    """
    Cria um diretório se ele não existir.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def safe_copy(src, dst):
    """
    Copia um arquivo de src para dst. Cria a pasta destino se necessário.
    """
    safe_mkdir(os.path.dirname(dst))
    shutil.copy2(src, dst)


def normalize_filename(filename, pattern, replacement):
    """
    Aplica um padrão regex de substituição a nomes de arquivos.
    """
    import re
    return re.sub(pattern, replacement, filename, flags=re.IGNORECASE)


def safe_read_csv(path):
    """
    Tenta ler um arquivo CSV com tratamento de erro.
    """
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"[ERRO] Falha ao ler {path}: {e}")
        return None
