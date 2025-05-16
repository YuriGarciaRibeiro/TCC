import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar dados
df = pd.read_excel("TCC (respostas) (1).xlsx", sheet_name="Respostas ao formulário 1")

# Selecionar respostas
df_realismo = df[[
    'Se foi criado por computação gráfica, quão realista ele parece?.2',
    'Se foi criado por computação gráfica, quão realista ele parece?.3'
]].copy()
df_realismo.columns = ['CG_Raiva', 'CG_Felicidade']

# Mapear categorias para escala de 1 a 3
mapa = {
    'Irrealista': 1,
    'Moderadamente realista': 2,
    'Muito realista': 3
}
df_numerico = df_realismo.replace(mapa)

# Calcular médias
medias = df_numerico.mean()
stds = df_numerico.std()

# Plotar gráfico
x = np.arange(len(medias))
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(x, medias.values, color=['#4CAF50', '#81C784'])

# Adicionar valores numéricos acima das barras
for i, bar in enumerate(bars):
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, altura + 0.05, f'{altura:.2f}', ha='center', fontsize=10)

# Configurações do gráfico
ax.set_xticks(x)
ax.set_xticklabels(medias.index)
ax.set_ylim(0.8, 3.2)
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(['Irrealista (1)', 'Moderadamente realista (2)', 'Muito realista (3)'])
ax.set_ylabel('Nível médio de realismo percebido')
ax.set_title('Avaliação média do realismo percebido (escala 1–3)')
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("realismo_escalar_cg.png", dpi=300)
plt.show()
