import os
from pathlib import Path
from pprint import pprint

import py_audio2face as pya2f

from config.constants import DATASET_DIR, FPS_DEFAULT
from utils.file_operations import list_files_by_extension


def process_audio_files(directory):
    a2f = pya2f.Audio2Face()
    pprint(a2f.a2e_settings)

    # Define configurações do Audio2Face
    a2f.a2e_set_settings(
        a2e_emotion_strength=1,
        a2e_max_emotions=6,
        a2e_contrast=1,
        a2e_smoothing_exp=0,
    )
    pprint(a2f.a2e_settings)

    a2f.set_enable_auto_generate_on_track_change(True)

    audio_files = list_files_by_extension(directory, ".wav")

    for audio_file_path in audio_files:
        output_path = os.path.splitext(audio_file_path)[0] + "_animation.usd"

        final_path = a2f.audio2face_single(
            audio_file_path=audio_file_path,
            output_path=output_path,
            fps=FPS_DEFAULT,
            emotion_auto_detect=True,
        )
        print(f"Processed: {audio_file_path} -> {final_path}")

    a2f.shutdown_a2f()


def main(directory=DATASET_DIR):
    process_audio_files(directory)


if __name__ == "__main__":
    main()
