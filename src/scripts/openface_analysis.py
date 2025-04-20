import os
import shutil
import subprocess
from time import sleep

from config.constants import DOCKER_INPUT_DIR, DOCKER_OUTPUT_DIR

for root, _, files in os.walk(DOCKER_INPUT_DIR, topdown=False):
    print(f"{files[::-1]}")
    for video in files[::-1]:
        if video.endswith('.mp4'):
            video_path = os.path.join(root, video)
            folder_name = root.split('/')[-1]
            docker_input_path = f'/input/{folder_name}/{video}'
            docker_output_path = f'/output/{folder_name}/{video.replace(".mp4", "")}'

            command = [
                'docker', 'exec', '-it', 'openface', '/bin/bash', '-c',
                f'build/bin/FeatureExtraction -f {docker_input_path} -out_dir {docker_output_path}'
            ]

            subprocess.run(command, cwd=root, check=True)

            shutil.copy2(video_path, os.path.join(
                DOCKER_OUTPUT_DIR, folder_name, video))
            print(f"File {video} copied to output folder")

        elif video.endswith('.wav'):
            shutil.copy2(os.path.join(root, video), os.path.join(
                DOCKER_OUTPUT_DIR, folder_name, video))
            print(f"File {video} copied to output folder")

print("Processing completed.")
