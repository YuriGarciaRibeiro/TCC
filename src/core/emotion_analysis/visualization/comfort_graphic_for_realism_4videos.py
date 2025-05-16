import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_excel("TCC (respostas) (1).xlsx", sheet_name="Respostas ao formulário 1")

# Selecionar colunas automaticamente
realismo_cols = df.filter(like='realista').columns
desconforto_cols = df.filter(like='estranheza').columns

# Ordenar: felicidade (original + CG), depois raiva (original + CG)
df_realismo = df[realismo_cols[[0, 3, 1, 2]]].copy()
df_desconforto = df[desconforto_cols[[0, 3, 1, 2]]].copy()

df_realismo.columns = ['Original_Felicidade', 'CG_Felicidade', 'Original_Raiva', 'CG_Raiva']
df_desconforto.columns = ['Original_Felicidade', 'CG_Felicidade', 'Original_Raiva', 'CG_Raiva']

# Mapear respostas para valores numéricos
map_realismo = {'Irrealista': 1, 'Moderadamente realista': 2, 'Muito realista': 3}
realismo_num = df_realismo.replace(map_realismo)

# Mapear desconforto: Sim = 1 (sentiu desconforto), Não = 0
desconforto_num = df_desconforto.applymap(lambda x: 1 if x == 'Sim' else 0)

# Calcular conforto: 1 - desconforto
conforto_num = 1 - desconforto_num

# Calcular médias
media_realismo = realismo_num.mean()
media_conforto = conforto_num.mean()

# Criar DataFrame com ordem desejada
ordem = ['Original_Felicidade', 'CG_Felicidade', 'Original_Raiva', 'CG_Raiva']
df_plot = pd.DataFrame({
    'Realismo Médio': media_realismo,
    'Conforto Médio': media_conforto
}).loc[ordem]

# Plotar gráfico
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#4CAF50', '#81C784', '#f44336', '#2196F3']
bars = ax.bar(df_plot.index, df_plot['Conforto Médio'], color=colors)

# Anotar valores nas colunas
for bar in bars:
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, altura + 0.02, f'{altura:.2f}', ha='center', fontsize=10)

# Layout
ax.set_ylim(0, 1.1)
ax.set_ylabel('Conforto médio (0 = nenhum, 1 = máximo)')
ax.set_xlabel('Vídeos (agrupados por emoção)')
ax.set_title('Conforto percebido em função do realismo médio (4 vídeos)')
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig("grafico_conforto_por_realismo_4videos.png", dpi=300)
plt.show()
