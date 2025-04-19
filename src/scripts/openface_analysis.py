import os
import shutil
import subprocess
from time import sleep

input_directory = os.path.expanduser(
    '/Users/yurigarciaribeiro/Documents/TCC/DockerC/input')
output_directory = os.path.expanduser(
    '/Users/yurigarciaribeiro/Documents/TCC/DockerC/output')

for root, _, files in os.walk(input_directory, topdown=False):
    print(f"{files[::-1]}")
    for video in files[::-1]:
        if video.endswith('.mp4'):
            video_path = os.path.join(root, video)
            folder_name = root.split('/')[-1]
            docker_input_path = '/input/' + folder_name + '/' + video

            command = [
                'docker', 'exec', '-it', 'openface', '/bin/bash', '-c',
                f'build/bin/FeatureExtraction -f {docker_input_path} -out_dir /output/{folder_name}/{video.replace(".mp4", "")}'
            ]

            subprocess.run(command, cwd=root, check=True)

            shutil.copy2(os.path.join(root, video), os.path.join(
                output_directory, root.split('/')[-1], video))
            print(f"File {video} copied to output folder")

        elif video.endswith('.wav'):
            shutil.copy2(os.path.join(root, video), os.path.join(
                output_directory, root.split('/')[-1], video))
            print(f"File {video} copied to output folder")

print("Processing completed.")
