import os
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from PIL import Image

def generate_plot(analysis_result,sufix = ""):
    emotion_counts = analysis_result["emotion_counts"]
    dominant_emotion_video = analysis_result["dominant_emotion_video"]
    dominant_frame = analysis_result["dominant_frame"]
    dominant_frame_path = analysis_result["dominant_frame_path"]
    video_name = analysis_result["video_name"]
    data = analysis_result["data"]

    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[2, 1])

    ax1 = plt.subplot(gs[0, 0])
    ax2 = plt.subplot(gs[0, 1])
    ax3 = plt.subplot(gs[1, 0])

    plt.suptitle(f"Contagem das Emoções ao Longo do Vídeo: {video_name}", fontsize=16)

    ax1.bar(emotion_counts.keys(), emotion_counts.values())
    ax1.set_xlabel("Emoções")
    ax1.set_ylabel("Número de ativações")
    ax1.tick_params(axis="x", rotation=45)
    ax1.text(0.5, 1.1, f"Emoção predominante: {dominant_emotion_video}", horizontalalignment="center", verticalalignment="center", transform=ax1.transAxes, fontsize=12, color="blue")

    frame_image = Image.open(dominant_frame_path)
    frame_image = frame_image.resize((300, 300))
    imagebox = OffsetImage(frame_image, zoom=0.8)
    ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False)
    ax2.add_artist(ab)
    ax2.text(0.5, 1.05, f"Frame com maior expressão emocional: {dominant_frame}", horizontalalignment="center", verticalalignment="center", transform=ax2.transAxes, fontsize=12, color="green")
    ax2.axis("off")

    pprint(data)
    
    cell_text = [[key, value] for key, value in data.items()]
    table = ax3.table(cellText=cell_text, colLabels=["Chave", "Valor"], loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax3.axis("off")

    # aumenta o tamanho do plot
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)

    if not os.path.exists(f"/Users/yurigarciaribeiro/Documents/GitHub/TCC/graphs/{video_name.replace('.csv','').split('-')[-1]}"):
        os.makedirs(f"/Users/yurigarciaribeiro/Documents/GitHub/TCC/graphs/{video_name.replace('.csv','').split('-')[-1]}")

    plt.savefig(f"/Users/yurigarciaribeiro/Documents/GitHub/TCC/graphs/{video_name.replace('.csv','').split('-')[-1]}/{video_name.replace('.csv', '')}_{sufix}.png")
    plt.close()