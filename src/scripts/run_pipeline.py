import logging

from config.constants import (ANIMATION_DIR, DATASET_DIR, DOCKER_INPUT_DIR,
                              DOCKER_OUTPUT_DIR, GRAPHS_DIR, VIDEO_EXTENSION)
from core.animations.animation_generator import process_audio_files
from core.emotion_analysis.aepa.analyze_video_emotions_aepa import \
    main as analyze_emotions
from core.emotion_analysis.visualization.generate_au_intensity_comparison import \
    generate_au_intensity_comparison
from scripts.openface_analysis import run_openface_analysis
from scripts.organize_and_rename_animated_files import \
    copy_and_rename_clean_dest
from services.unreal.create_sequences import \
    criar_level_sequences_para_animacoes

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def run_pipeline():
    logging.info("[1/6] Iniciando análise com OpenFace...")
    run_openface_analysis(DOCKER_INPUT_DIR, DOCKER_OUTPUT_DIR)

    logging.info("[2/6] Gerando animações com Audio2Face...")
    process_audio_files(DATASET_DIR)

    logging.info("[3/6] Organizando e renomeando animações...")
    copy_and_rename_clean_dest(
        "videos", DATASET_DIR, extension=VIDEO_EXTENSION)

    logging.info("[4/6] Analisando emoções nos vídeos com AEPA...")
    analyze_emotions(DATASET_DIR)

    logging.info("[5/6] Comparando intensidade dos AUs...")
    generate_au_intensity_comparison()

    logging.info("[6/6] Criando Level Sequences na Unreal...")
    criar_level_sequences_para_animacoes(ANIMATION_DIR)

    logging.info("Pipeline finalizada com sucesso!")


if __name__ == "__main__":
    run_pipeline()
