import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint

# Carregar dados
df = pd.read_excel("TCC (respostas) (1).xlsx", sheet_name="Respostas ao formulário 1")

# Selecionar e renomear colunas
realismo = df[[ 
    '  Você acha que o personagem na imagem/vídeo acima é:  .2',
    '  Você acha que o personagem na imagem/vídeo acima é:  .3'
]].copy()
realismo.columns = ['CG_Raiva', 'CG_Felicidade']

estranheza = df[[ 
    '  Você sente algum desconforto (estranheza) ao olhar para esse personagem?  .2',
    '  Você sente algum desconforto (estranheza) ao olhar para esse personagem?  .3'
]].copy()
estranheza.columns = ['CG_Raiva', 'CG_Felicidade']

# Converter para binário
realismo_bin = realismo.applymap(lambda x: 1 if x == "Uma pessoa real" else 0)
estranheza_bin = estranheza.applymap(lambda x: 1 if x == "Sim" else 0)

# Cálculo de proporções
media_realismo = realismo_bin.mean() * 100
media_estranheza = estranheza_bin.mean() * 100

# Plotar
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Subplot 1: Realismo
bars1 = axs[0].bar(media_realismo.index, media_realismo.values, color=['#4CAF50', '#81C784'])
for i, bar in enumerate(bars1):
    altura = bar.get_height()
    axs[0].text(bar.get_x() + bar.get_width() / 2, altura + 2, f'{altura:.1f}%', ha='center', fontsize=10)

axs[0].set_title('Percepção de realismo')
axs[0].set_ylabel('Percentual (%)')

# Subplot 2: Desconforto
bars2 = axs[1].bar(media_estranheza.index, media_estranheza.values, color=['#FF7043', '#FFAB91'])
for i, bar in enumerate(bars2):
    altura = bar.get_height()
    axs[1].text(bar.get_x() + bar.get_width() / 2, altura + 2, f'{altura:.1f}%', ha='center', fontsize=10)

axs[1].set_title('Percepção de desconforto')
axs[1].set_ylabel('Percentual (%)')

# Layout geral
for ax in axs:
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.suptitle("Percepções sobre realismo e desconforto em vídeos CG")
plt.tight_layout()
plt.savefig("realismo_desconforto.png", dpi=300)

