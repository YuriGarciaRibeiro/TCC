import os
from pathlib import Path
from pprint import pprint
from time import sleep

import py_audio2face as pya2f

from config.constants import DATASET_DIR, FPS_DEFAULT


def process_audio_files(directory):
    a2f = pya2f.Audio2Face()
    pprint(a2f.a2e_settings)

    a2f.a2e_set_settings(
        a2e_emotion_strength=1,
        a2e_max_emotions=6,
        a2e_contrast=1,
        a2e_smoothing_exp=0,
    )
    pprint(a2f.a2e_settings)

    a2f.set_enable_auto_generate_on_track_change(True)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                audio_file_path = os.path.join(root, file)
                output_path = os.path.splitext(audio_file_path)[
                    0] + "_animation.usd"

                final_path = a2f.audio2face_single(
                    audio_file_path=audio_file_path,
                    output_path=output_path,
                    fps=FPS_DEFAULT,
                    emotion_auto_detect=True,
                )
                print(f"Processed: {audio_file_path} -> {final_path}")
    a2f.shutdown_a2f()


if __name__ == "__main__":
    process_audio_files(DATASET_DIR)
