import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

# Carregar dados
df = pd.read_excel("TCC (respostas) (1).xlsx", sheet_name="Respostas ao formulário 1")

# Selecionar colunas e renomear
df_int = df[[ 
    'O quão intensa é a emoção:',
    'O quão intensa é a emoção:.3',
    'O quão intensa é a emoção:.1',
    'O quão intensa é a emoção:.2'
]].copy()
df_int.columns = ['Original_Felicidade', 'CG_Felicidade', 'Original_Raiva', 'CG_Raiva']
df_int = df_int.apply(pd.to_numeric, errors='coerce')

# Estatísticas
media = df_int.mean()
std = df_int.std()

# Agrupamento
grupos = ['Felicidade', 'Raiva']
bar_width = 0.35
x = np.arange(len(grupos))

means_original = [media['Original_Felicidade'], media['Original_Raiva']]
means_cg = [media['CG_Felicidade'], media['CG_Raiva']]
stds_original = [std['Original_Felicidade'], std['Original_Raiva']]
stds_cg = [std['CG_Felicidade'], std['CG_Raiva']]

# Testes t
_, p_fel = ttest_ind(df_int['Original_Felicidade'].dropna(), df_int['CG_Felicidade'].dropna(), equal_var=False)
_, p_rai = ttest_ind(df_int['Original_Raiva'].dropna(), df_int['CG_Raiva'].dropna(), equal_var=False)
_, p_orig = ttest_ind(df_int['Original_Felicidade'].dropna(), df_int['Original_Raiva'].dropna(), equal_var=False)
_, p_cg = ttest_ind(df_int['CG_Felicidade'].dropna(), df_int['CG_Raiva'].dropna(), equal_var=False)

# Formatar valores de p
p_text_fel = f'p = {p_fel:.3f}' if p_fel >= 0.001 else 'p < 0.001'
p_text_rai = f'p = {p_rai:.3f}' if p_rai >= 0.001 else 'p < 0.001'
p_text_orig = f'p = {p_orig:.3f}' if p_orig >= 0.001 else 'p < 0.001'
p_text_cg = f'p = {p_cg:.3f}' if p_cg >= 0.001 else 'p < 0.001'

# Gráfico
fig, ax = plt.subplots(figsize=(9, 6))

bars1 = ax.bar(x - bar_width/2, means_original, width=bar_width, label='Original', color='#4CAF50')
bars2 = ax.bar(x + bar_width/2, means_cg, width=bar_width, label='CG', color='#2196F3')

# ✅ Anotar médias DENTRO das barras
for bar in bars1 + bars2:
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, altura / 2, f'{altura:.2f}', 
            ha='center', va='center', fontsize=10, color='white')

# Comparações verticais (Original vs CG)
ax.text(x[0], max(means_original[0], means_cg[0]) + 0.4, p_text_fel, ha='center', fontsize=11, color='black')
ax.text(x[1], max(means_original[1], means_cg[1]) + 0.4, p_text_rai, ha='center', fontsize=11, color='black')

# Comparação Original (verde vs verde)
x0_orig = x[0] - bar_width/2
x1_orig = x[1] - bar_width/2
y_orig = max(means_original) + 0.7
ax.plot([x0_orig, x1_orig], [y_orig, y_orig], color='black', linestyle='--')
ax.plot([x0_orig, x0_orig], [y_orig, means_original[0]], color='black', linestyle='--')
ax.plot([x1_orig, x1_orig], [y_orig, means_original[1]], color='black', linestyle='--')
ax.text((x0_orig + x1_orig)/2, y_orig + 0.05, f'Original: {p_text_orig}', ha='center', color='black')

# Comparação CG (azul vs azul)
x0_cg = x[0] + bar_width/2
x1_cg = x[1] + bar_width/2
y_cg = max(means_cg) + 0.7
ax.plot([x0_cg, x1_cg], [y_cg, y_cg], color='black', linestyle='--')
ax.plot([x0_cg, x0_cg], [y_cg, means_cg[0]], color='black', linestyle='--')
ax.plot([x1_cg, x1_cg], [y_cg, means_cg[1]], color='black', linestyle='--')
ax.text((x0_cg + x1_cg)/2, y_cg + 0.05, f'CG: {p_text_cg}', ha='center', color='black')

# Layout
ax.set_xticks(x)
ax.set_xticklabels(grupos)
ax.set_ylabel('Intensidade (1–5)')
ax.set_title('Intensidade média percebida por emoção\ncom todos os testes t')
ax.legend()
ax.set_ylim(0, max(means_original + means_cg) + 1.5)
ax.grid(axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig("intensidade_emocoes.png", dpi=300)
