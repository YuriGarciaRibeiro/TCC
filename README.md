# 🧠 Projeto de TCC: Pipeline de Análise de Emoções e Animação Facial

Este projeto tem como objetivo criar uma pipeline automatizada para análise de expressões faciais em vídeos e geração de animações faciais expressivas utilizando OpenFace, Audio2Face e Unreal Engine.

---

## 📂 Estrutura Geral do Projeto

```
src/
├── config/
│   ├── __init__.py
│   └── constants.py
├── core/
│   ├── __init__.py
│   ├── animations/
│   │   ├── __init__.py
│   │   └── animation_generator.py
│   └── emotion_analysis/
│       ├── __init__.py
│       ├── aepa/
│       │   ├── __init__.py
│       │   └── analyze_video_emotions_aepa.py
│       └── visualization/
│           ├── __init__.py
│           ├── generate_aepa_plot.py
│           └── generate_au_intensity_comparison.py
├── scripts/
│   ├── __init__.py
│   ├── copy_filtered_directory_structure.py
│   ├── openface_analysis.py
│   ├── organize_and_rename_animated_files.py
│   └── run_pipeline.py
├── services/
│   ├── __init__.py
│   └── unreal/
│       ├── __init__.py
│       └── create_sequences.py
├── utils/
│   ├── __init__.py
│   ├── file_operations.py
│   ├── file_management/
│   │   ├── __init__.py
│   │   ├── rename_dataset_files.py
│   │   └── transfer.py
│   └── video_processing/
│       ├── __init__.py
│       └── filter_and_copy_used_videos.py
```

---

## 🚀 Executando a Pipeline

### 1. ✅ Requisitos:
- Python 3.10+
- Ambiente virtual configurado (`python -m venv .venv`)
- Docker instalado (com container `openface` em execução)
- Audio2Face aberto e configurado para escutar
- Unreal Engine com projeto carregado para leitura dos arquivos `.uasset`

### 2. 🧱 Instalar dependências:
```bash
cd src
pip install -r requirements.txt  # se aplicável
```

### 3. ▶️ Executar a pipeline:
```bash
cd src
python scripts/run_pipeline.py
```

A pipeline executa automaticamente as etapas abaixo:

1. **Análise facial com OpenFace (Docker):**
   - Entrada: `dataset/` → `DockerC/input/`
   - Saída: `DockerC/output/` com `.csv`, frames, etc.

2. **Geração de animação com Audio2Face:**
   - Entrada: arquivos `.wav` do `dataset/`
   - Saída: `.usd` animado na mesma pasta do .wav

3. **Organiza e renomeia arquivos animados:**
   - Entrada: `videos/` com arquivos brutos de animação
   - Saída: arquivos renomeados para `*_animated.mp4` em `dataset/actorXX/`

4. **Análise de emoções por AEPA:**
   - Lê os `.csv` do OpenFace e gera contagem de emoções predominantes
   - Gera gráficos na pasta `graphs/actorXX/`

5. **Comparativo de intensidade de AUs (real vs CG):**
   - Analisa os `.csv` reais e animados
   - Gera gráficos em `graphs/actorXX_au_intensity_comparison/{happy, angry}`

6. **Criação de Level Sequences (Unreal):**
   - Baseado nos `.uasset` do diretório `animation/`
   - Executa via `unreal.EditorAssetLibrary`

---

## ⚙️ Parâmetros e Configurações

Todos os caminhos e limiares estão definidos no arquivo:
```
src/config/constants.py
```

Exemplos:
```python
DATASET_DIR = ROOT_DIR / "dataset"
AEPA_THRESHOLD = 0.7
FPS_DEFAULT = 30
DOCKER_CONTAINER_NAME = "openface"
```

---

## 🧪 Debug: imprimir caminhos configurados
No terminal Python:
```python
from config.constants import print_all_paths
print_all_paths()
```

---

## 📌 Notas importantes
- Certifique-se que os nomes dos arquivos sigam o padrão esperado (com actorXX, etc.)
- Todos os scripts são testados com a estrutura do dataset RAVDESS e MetaHuman.
- Para ajustes, edite diretamente os módulos em `src/core/`, `src/scripts/`, `src/utils/` etc.

---

## 👨‍💻 Autor
**Yuri Garcia Ribeiro**  
Projeto de TCC em Ciências da Computação - Universidade Tiradentes (UNIT)  
Orientador: Prof. Victor Flávio de Andrade Araújo
