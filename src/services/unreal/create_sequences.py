import os

import unreal


def criar_level_sequence_com_camera(animacao_path):
    """
    Cria um Level Sequence com o nome da animação e adiciona a câmera à sequência.
    """
    # Extrair o nome da animação (sem extensão) para nome do Level Sequence
    animacao_nome = os.path.basename(animacao_path).split(".")[0]
    print(f"Processando Level Sequence: {animacao_nome}")

    # Criar um novo Level Sequence com o nome da animação
    print(f"Criando Level Sequence com o nome da animação: {animacao_nome}")
    level_sequence_factory = unreal.LevelSequenceFactoryNew()
    level_sequence_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        animacao_nome, "/Game/Sequencias", None, level_sequence_factory
    )

    # Verificar se o Level Sequence foi criado com sucesso
    if not level_sequence_asset:
        print(f"Falha ao criar Level Sequence para {animacao_nome}.")
        return

    print(f"Level Sequence {animacao_nome} criado com sucesso.")

    # Abrir o Level Sequence recém-criado
    level_sequence = unreal.LevelSequence.cast(level_sequence_asset)
    if not level_sequence:
        print(f"Falha ao abrir o Level Sequence {animacao_nome}.")
        return

    print(f"Level Sequence {animacao_nome} aberto com sucesso.")

    # Buscar a câmera existente na cena
    cine_camera_actor = obter_actor_na_cena("CineCameraActor_0")

    if cine_camera_actor:
        # Se a câmera foi encontrada na cena, adicioná-la à sequência
        print(f"Adicionando CineCameraActor existente à sequência...")
        cine_camera_binding = level_sequence.add_possessable(cine_camera_actor)
        if cine_camera_binding:
            print(f"CineCameraActor adicionado à sequência.")
        else:
            print(f"Falha ao adicionar CineCameraActor à sequência.")
    else:
        print(
            "Não foi possível encontrar uma câmera existente para adicionar ao Level Sequence."
        )

    # Salvar o Level Sequence
    print(f"Salvando o Level Sequence {animacao_nome}...")
    unreal.EditorAssetLibrary.save_asset(level_sequence.get_path_name())
    print(f"Level Sequence {animacao_nome} criado e salvo com sucesso.")


def obter_actor_na_cena(nome_actor):
    """
    Função para buscar um ator na cena com base no nome fornecido.
    """
    # Usar EditorActorSubsystem para buscar atores (substitui o método depreciado)
    editor_actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    todos_atores = editor_actor_subsystem.get_all_level_actors()
    for ator in todos_atores:
        if ator.get_name() == nome_actor:
            print(f"Ator {nome_actor} encontrado na cena.")
            return ator
    print(f"Ator {nome_actor} não encontrado na cena.")
    return None


def criar_level_sequences_para_animacoes(pasta_animacoes):
    """
    Busca as animações na pasta especificada e cria Level Sequences para cada uma delas.
    """
    print(f"Buscando animações na pasta {pasta_animacoes}...")
    arquivos_animacoes = [
        os.path.join(pasta_animacoes, f)
        for f in os.listdir(pasta_animacoes)
        if f.endswith(".uasset")
    ]
    print(f"{len(arquivos_animacoes)} animações encontradas.")

    # Criar Level Sequences para cada animação
    for animacao in arquivos_animacoes:
        # Transforma o caminho absoluto em um caminho relativo dentro do Unreal
        animacao_relativa = (
            f"/Game/animation/{os.path.basename(animacao).split('.')[0]}"
        )
        print(f"Processando Level Sequence para animação {animacao_relativa}...")
        criar_level_sequence_com_camera(animacao_relativa)


# Caminho para a pasta com as animações (Animation Sequences) - em formato absoluto
pasta_animacoes = (
    r"C:\Users\yurig\Documents\Unreal Projects\MyProject\Content\animation"
)

# Chamar a função para criar Level Sequences para cada animação
print("Iniciando a criação de Level Sequences...")
criar_level_sequences_para_animacoes(pasta_animacoes)
