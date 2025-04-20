import logging
import os
import re

from config.constants import DATASET_DIR, VIDEO_EXTENSION, VIDEOS_DIR
from utils.file_operations import (normalize_filename, safe_copy,
                                        safe_mkdir)

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def copy_and_rename_clean_dest(src_root: str, dst_root: str, extension: str = VIDEO_EXTENSION):
    """
    Copia arquivos de src_root para dst_root organizando em subpastas por ator,
    renomeando de *_animation_usd_bsweight.ext para *_animated.ext,
    e removendo no destino qualquer arquivo com sufixo _animation_usd_bsweight.ext
    nas pastas de ator.
    """
    pattern_actor = re.compile(r"(actor\d{2})", re.IGNORECASE)
    pattern_cleanup = re.compile(
        r"_animation_usd_bsweight(\.[^.]+)$", re.IGNORECASE)
    rename_pattern = r"(.*actor\d{2})_.*(\.[^.]+)$"
    rename_replacement = r"\1_animated\2"

    for dirpath, _, filenames in os.walk(src_root):
        for filename in filenames:
            if extension and not filename.lower().endswith(extension.lower()):
                continue

            m = pattern_actor.search(filename)
            if not m:
                logging.warning(f"[SKIP] Não identificou ator em: {filename}")
                continue
            actor = m.group(1).lower()

            src_file = os.path.join(dirpath, filename)
            dest_dir = os.path.join(dst_root, actor)
            safe_mkdir(dest_dir)

            # Remove arquivos antigos no destino
            for existing in os.listdir(dest_dir):
                if pattern_cleanup.search(existing):
                    old_path = os.path.join(dest_dir, existing)
                    os.remove(old_path)
                    logging.info(f"[CLEANED] {old_path}")

            # Renomeia para *_animated.ext
            new_filename = normalize_filename(
                filename, rename_pattern, rename_replacement)
            dest_file = os.path.join(dest_dir, new_filename)

            safe_copy(src_file, dest_file)
            logging.info(f"[COPIED] {src_file} → {dest_file}")


def main():
    copy_and_rename_clean_dest(
        VIDEOS_DIR, DATASET_DIR, extension=VIDEO_EXTENSION)


if __name__ == "__main__":
    main()
