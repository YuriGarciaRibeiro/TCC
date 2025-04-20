import os
import shutil

from config.constants import emotional_intensity, emotions, modalities
from config.constants import repetition as repetitions
from config.constants import statements
from config.constants import vocal_channel

base_path = "C:/Users/yurig/Documents/GitHub/TCC/Dataset"

# List of file compositions
compositions = [
    ["01", "01", "03", "02", "01", "01"],  # Composition 1 (mp4)
    ["01", "01", "05", "02", "01", "01"],  # Composition 2 (mp4)
    ["03", "01", "03", "02", "01", "01"],  # Composition 3 (wav)
    ["03", "01", "05", "02", "01", "01"],  # Composition 4 (wav)
]

# Loop through actors 1 to 24
for i in range(1, 25):
    actor_id = f"{i:02}"
    actor_folder = f"Actor{actor_id}"
    destination_folder = os.path.join(
        "C:/Users/yurig/Documents/GitHub/TCC/filtered", actor_folder)

    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

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
