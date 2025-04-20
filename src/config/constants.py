from pathlib import Path

# === Diretórios base ===
ROOT_DIR = Path(__file__).resolve().parents[2]

SRC_DIR = ROOT_DIR / "src"
TEST_DIR = ROOT_DIR / "teste"
DATASET_DIR = ROOT_DIR / "dataset"
DOCKER_INPUT_DIR = ROOT_DIR / "DockerC/input"
DOCKER_OUTPUT_DIR = ROOT_DIR / "DockerC/output"
VIDEOS_DIR = ROOT_DIR / "videos"
GRAPHS_DIR = ROOT_DIR / "graphs"
FILTERED_DIR = ROOT_DIR / "filtered"
ANIMATION_DIR = Path("C:/Users/yurig/Documents/Unreal Projects/MyProject/Content/animation")

# === Mapeamento geral de diretórios (opcional) ===
DIRS = {
    "root": ROOT_DIR,
    "src": SRC_DIR,
    "test": TEST_DIR,
    "dataset": DATASET_DIR,
    "docker_input": DOCKER_INPUT_DIR,
    "docker_output": DOCKER_OUTPUT_DIR,
    "videos": VIDEOS_DIR,
    "graphs": GRAPHS_DIR,
    "filtered": FILTERED_DIR,
    "animation": ANIMATION_DIR,
}

def print_all_paths():
    for name, path in DIRS.items():
        print(f"{name.upper():<15}: {path}")

# === Thresholds ===
AU_INTENSITY_THRESHOLD = 2
AEPA_THRESHOLD = 0.7
FPS_DEFAULT = 30

# === Extensões comuns ===
VIDEO_EXTENSION = ".mp4"
AUDIO_EXTENSION = ".wav"
CSV_EXTENSION = ".csv"
USD_EXTENSION = ".usd"
UASSET_EXTENSION = ".uasset"

# === Emoções-alvo (usadas em comparações de AUs)
TARGET_EMOTIONS = ["happy", "angry"]

# === Nome do container Docker usado para o OpenFace
DOCKER_CONTAINER_NAME = "openface"

# === Nome padrão da câmera na Unreal
DEFAULT_CAMERA_NAME = "CineCameraActor_0"

# === Dicionários de código para string ===
modalities = {
    '01': 'full-AV',
    '02': 'video-only',
    '03': 'audio-only'
}

vocal_channel = {
    '01': 'speech',
    '02': 'song'
}

emotions = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

emotional_intensity = {
    '01': 'normal',
    '02': 'strong'
}

statements = {
    '01': 'Kids are talking by the door',
    '02': 'Dogs are sitting by the door'
}

repetition = {
    '01': '1st repetition',
    '02': '2nd repetition'
}

# === Emoções baseadas em AUs ===
emotions_au = {
    "Happiness": [6, 12],
    "Sadness": [1, 4, 15],
    "Surprise": [1, 2, 5, 26],
    "Fear": [1, 2, 4, 5, 7, 20, 26],
    "Anger": [4, 5, 7, 23],
    "Disgust": [9, 15, 16]
    # "Contempt": [12, 14]
}

EMOTION_TEMPLATES = {
    "Happiness": ["AU6", "AU12"],
    "Sadness": ["AU1", "AU4", "AU15"],
    "Surprise": ["AU1", "AU2", "AU5", "AU26"],
    "Fear": ["AU1", "AU2", "AU4", "AU5", "AU7", "AU20", "AU26"],
    "Anger": ["AU4", "AU5", "AU7", "AU23"],
    "Disgust": ["AU9", "AU15", "AU16"]
    # "Contempt": ["AU12", "AU14"]
}
