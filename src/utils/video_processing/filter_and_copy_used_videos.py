import os
import shutil

from config.constants import (DATASET_DIR, FILTERED_DIR, emotional_intensity,
                              emotions, modalities)
from config.constants import repetition as repetitions
from config.constants import statements, vocal_channel


def filter_and_copy_used_videos(base_path=DATASET_DIR, destination_root=FILTERED_DIR):
    compositions = [
        ["01", "01", "03", "02", "01", "01"],  # Composition 1 (mp4)
        ["01", "01", "05", "02", "01", "01"],  # Composition 2 (mp4)
        ["03", "01", "03", "02", "01", "01"],  # Composition 3 (wav)
        ["03", "01", "05", "02", "01", "01"],  # Composition 4 (wav)
    ]

    for i in range(1, 25):
        actor_id = f"{i:02}"
        actor_folder = f"Actor{actor_id}"
        destination_folder = os.path.join(destination_root, actor_folder)

        os.makedirs(destination_folder, exist_ok=True)

        for composition in compositions:
            extension = ".wav" if composition[0] == "03" else ".mp4"

            file_name = (
                f"{modalities[composition[0]]}-{vocal_channel[composition[1]]}-"
                f"{emotions[composition[2]]}-{emotional_intensity[composition[3]]}-"
                f"{statements[composition[4]].replace(' ', '-')}-"
                f"{repetitions[composition[5]].replace(' ', '-')}-actor{actor_id}{extension}"
            )

            source_path = os.path.join(
                base_path, actor_folder, file_name).replace(" ", "-")

            if os.path.exists(source_path):
                print(f"Found file: {file_name}")
                shutil.copy(source_path, destination_folder)


def main():
    filter_and_copy_used_videos()


if __name__ == "__main__":
    main()
