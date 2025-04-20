import logging
import os
import subprocess

from config.constants import (DOCKER_CONTAINER_NAME, DOCKER_INPUT_DIR,
                              DOCKER_OUTPUT_DIR)
from utils.file_operations import safe_copy, safe_mkdir

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def run_openface_analysis(input_dir=DOCKER_INPUT_DIR, output_dir=DOCKER_OUTPUT_DIR):
    for root, _, files in os.walk(input_dir, topdown=False):
        logging.info(f"Verificando diretório: {root}")
        for video in files[::-1]:
            folder_name = os.path.basename(root)
            target_folder = os.path.join(output_dir, folder_name)
            safe_mkdir(target_folder)

            if video.endswith(".mp4"):
                video_path = os.path.join(root, video)
                docker_input_path = f"/input/{folder_name}/{video}"
                docker_output_path = f"/output/{folder_name}/{video.replace('.mp4', '')}"

                command = [
                    "docker", "exec", "-it", DOCKER_CONTAINER_NAME, "/bin/bash", "-c",
                    f"build/bin/FeatureExtraction -f {docker_input_path} -out_dir {docker_output_path}"
                ]

                subprocess.run(command, cwd=root, check=True)
                safe_copy(video_path, os.path.join(target_folder, video))
                logging.info(f"[MP4] Copiado: {video_path} → {target_folder}")

            elif video.endswith(".wav"):
                source_file = os.path.join(root, video)
                dest_file = os.path.join(target_folder, video)
                safe_copy(source_file, dest_file)
                logging.info(f"[WAV] Copiado: {source_file} → {target_folder}")

    logging.info("Processamento finalizado.")


def main():
    run_openface_analysis()


if __name__ == "__main__":
    main()
