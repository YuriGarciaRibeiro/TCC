import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_excel("TCC (respostas) (1).xlsx", sheet_name="Respostas ao formulário 1")

# Selecionar colunas e renomear
df_emocoes = df[[ 
    'Qual a emoção você percebe no vídeo?',
    'Qual a emoção você percebe no vídeo?.3',
    'Qual a emoção você percebe no vídeo?.1',
    'Qual a emoção você percebe no vídeo?.2'
]].copy()
df_emocoes.columns = ['Original_Felicidade', 'CG_Felicidade', 'Original_Raiva', 'CG_Raiva']

# Calcular proporções
proporcoes = df_emocoes.apply(lambda col: col.value_counts(normalize=True)).fillna(0) * 100

# Reordenar colunas
proporcoes = proporcoes[['Original_Felicidade', 'CG_Felicidade', 'Original_Raiva', 'CG_Raiva']]

# Plotar
fig, ax = plt.subplots(figsize=(10, 6))
bottom = [0] * proporcoes.shape[1]

colors = plt.cm.tab20.colors  # paleta com várias cores

for idx, emocao in enumerate(proporcoes.index):
    valores = proporcoes.loc[emocao]
    bars = ax.bar(proporcoes.columns, valores, bottom=bottom, label=emocao, color=colors[idx % len(colors)])

    # Adicionar valores em cima de cada segmento
    for bar, valor in zip(bars, valores):
        if valor > 4:  # evita sobreposição em blocos muito pequenos
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_y() + bar.get_height() / 2,
                f'{valor:.0f}%',
                ha='center',
                va='center',
                fontsize=9,
                color='white'
            )

    # Atualizar "base" para a próxima barra empilhar corretamente
    bottom = [i + j for i, j in zip(bottom, valores)]

# Ajustes visuais
ax.set_title("Distribuição percentual das emoções percebidas por vídeo")
ax.set_ylabel("Percentual (%)")
ax.set_xlabel("Vídeo (agrupado por emoção)")
ax.set_xticks(range(len(proporcoes.columns)))
ax.set_xticklabels(proporcoes.columns, rotation=15)
ax.legend(title="Emoção", bbox_to_anchor=(1.05, 1))
ax.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("distribuicao_emocoes.png", dpi=300)
