import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from collections import defaultdict

# Caminhos absolutos
DATASET_ROOT = Path("/Users/yurigarciaribeiro/Documents/GitHub/TCC/dataset")
OUTPUT_BASE = Path("/Users/yurigarciaribeiro/Documents/GitHub/TCC/graphs")

# Emoções que vamos processar
EMOTIONS = ["happy", "angry"]

# Função para extrair médias dos AUs
def extract_au_means(csv_path):
    df = pd.read_csv(csv_path)
    au_cols = [col for col in df.columns if col.startswith(" AU") and col.endswith("_r")]
    means = df[au_cols].mean().to_dict()
    return {col.strip(): val for col, val in means.items()}

# Mapeia arquivos por ator e emoção
actor_files = defaultdict(lambda: defaultdict(lambda: {"real": None, "animated": None}))

for path in DATASET_ROOT.rglob("*.csv"):
    name = path.name.lower()
    if "actor" not in name:
        continue

    # Extrai o número do ator
    actor_id = name.split("actor")[-1].split("_")[0].split(".")[0]
    actor_key = f"actor{actor_id}"

    # Define emoção
    emotion = "happy" if "happy" in name else "angry" if "angry" in name else None
    if not emotion:
        continue

    # Classifica como real ou animado
    if name.startswith("audio-only") and "animated" in name:
        actor_files[actor_key][emotion]["animated"] = path
    elif name.startswith("full-av"):
        actor_files[actor_key][emotion]["real"] = path

# Gera os gráficos
for actor_key, emotion_dict in actor_files.items():
    for emotion in EMOTIONS:
        real_csv = emotion_dict[emotion]["real"]
        cg_csv = emotion_dict[emotion]["animated"]

        if not real_csv or not cg_csv:
            print(f"[!] Pulando {actor_key} - {emotion}: CSV real ou animado ausente.")
            continue

        real_means = extract_au_means(real_csv)
        cg_means = extract_au_means(cg_csv)

        aus = sorted(set(real_means.keys()).union(cg_means.keys()))
        real_vals = [real_means.get(au, 0) for au in aus]
        cg_vals = [cg_means.get(au, 0) for au in aus]

        x = np.arange(len(aus))
        width = 0.35

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(x - width/2, real_vals, width, label='Real (RAVDESS)')
        ax.bar(x + width/2, cg_vals, width, label='CG (MetaHuman)')

        ax.set_ylabel('Intensidade Média dos AUs')
        ax.set_title(f'{actor_key.upper()} - {emotion.capitalize()}: Comparação de AUs')
        ax.set_xticks(x)
        ax.set_xticklabels(aus, rotation=45)
        ax.legend()
        plt.tight_layout()

        # Cria subpasta específica para emoção
        output_dir = OUTPUT_BASE / f"{actor_key}_au_intensity_comparison" / emotion
        output_dir.mkdir(parents=True, exist_ok=True)

        # Nome do arquivo
        filename = f"au_intensity_real_vs_cg_{actor_key}_{emotion}"
        plt.savefig(output_dir / f"{filename}.png")
        plt.savefig(output_dir / f"{filename}.pdf")
        plt.savefig(output_dir / f"{filename}.svg")
        plt.close()

        print(f"[✓] {actor_key} - {emotion} → {output_dir}")
