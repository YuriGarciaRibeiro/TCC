import os
import shutil

from config.constants import DATASET_DIR, DOCKER_INPUT_DIR, VIDEO_EXTENSION


def gather_dirs_with_matches(src_root: str, extension: str = None):
    """
    Retorna um conjunto de diretórios que contêm ao menos
    um arquivo com a extensão dada, mais todos os ancestrais
    desses diretórios (para manter a estrutura).
    """
    matches = set()
    for dirpath, _, filenames in os.walk(src_root):
        for fname in filenames:
            if extension is None or fname.lower().endswith(extension.lower()):
                matches.add(dirpath)
                break

    all_dirs = set()
    for d in matches:
        p = d
        while True:
            all_dirs.add(p)
            if os.path.abspath(p) == os.path.abspath(src_root):
                break
            p = os.path.dirname(p)
    return all_dirs


def copy_filtered_structure(src_root: str, dst_root: str, extension: str = None):
    """
    Copia apenas os diretórios que contêm arquivos com a extensão
    especificada, e dentro deles copia só esses arquivos.
    """
    valid_dirs = gather_dirs_with_matches(src_root, extension)

    for dirpath in valid_dirs:
        rel_path = os.path.relpath(dirpath, src_root)
        dest_dir = os.path.join(dst_root, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        for fname in os.listdir(dirpath):
            src_file = os.path.join(dirpath, fname)
            if os.path.isfile(src_file):
                if extension is None or fname.lower().endswith(extension.lower()):
                    dst_file = os.path.join(dest_dir, fname)
                    shutil.copy2(src_file, dst_file)
                    print(f"Copiado: {src_file} → {dst_file}")


def main():
    copy_filtered_structure(DATASET_DIR, DOCKER_INPUT_DIR, extension=VIDEO_EXTENSION)


if __name__ == "__main__":
    main()
