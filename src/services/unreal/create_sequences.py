import os

import unreal

from config.constants import ANIMATION_DIR


def criar_level_sequence_com_camera(animacao_path):
    animacao_nome = os.path.basename(animacao_path).split(".")[0]
    print(f"Processando Level Sequence: {animacao_nome}")

    level_sequence_factory = unreal.LevelSequenceFactoryNew()
    level_sequence_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        animacao_nome, "/Game/Sequencias", None, level_sequence_factory
    )

    if not level_sequence_asset:
        print(f"Falha ao criar Level Sequence para {animacao_nome}.")
        return

    print(f"Level Sequence {animacao_nome} criado com sucesso.")
    level_sequence = unreal.LevelSequence.cast(level_sequence_asset)
    if not level_sequence:
        print(f"Falha ao abrir o Level Sequence {animacao_nome}.")
        return

    print(f"Level Sequence {animacao_nome} aberto com sucesso.")
    cine_camera_actor = obter_actor_na_cena("CineCameraActor_0")

    if cine_camera_actor:
        print(f"Adicionando CineCameraActor existente à sequência...")
        cine_camera_binding = level_sequence.add_possessable(cine_camera_actor)
        if cine_camera_binding:
            print(f"CineCameraActor adicionado à sequência.")
        else:
            print(f"Falha ao adicionar CineCameraActor à sequência.")
    else:
        print("Não foi possível encontrar uma câmera existente para adicionar ao Level Sequence.")

    print(f"Salvando o Level Sequence {animacao_nome}...")
    unreal.EditorAssetLibrary.save_asset(level_sequence.get_path_name())
    print(f"Level Sequence {animacao_nome} criado e salvo com sucesso.")


def obter_actor_na_cena(nome_actor):
    editor_actor_subsystem = unreal.get_editor_subsystem(
        unreal.EditorActorSubsystem)
    todos_atores = editor_actor_subsystem.get_all_level_actors()
    for ator in todos_atores:
        if ator.get_name() == nome_actor:
            print(f"Ator {nome_actor} encontrado na cena.")
            return ator
    print(f"Ator {nome_actor} não encontrado na cena.")
    return None


def criar_level_sequences_para_animacoes(pasta_animacoes):
    print(f"Buscando animações na pasta {pasta_animacoes}...")
    arquivos_animacoes = [
        os.path.join(pasta_animacoes, f)
        for f in os.listdir(pasta_animacoes)
        if f.endswith(".uasset")
    ]
    print(f"{len(arquivos_animacoes)} animações encontradas.")

    for animacao in arquivos_animacoes:
        animacao_relativa = f"/Game/animation/{os.path.basename(animacao).split('.')[0]}"
        print(
            f"Processando Level Sequence para animação {animacao_relativa}...")
        criar_level_sequence_com_camera(animacao_relativa)


if __name__ == "__main__":
    print("Iniciando a criação de Level Sequences...")
    criar_level_sequences_para_animacoes(ANIMATION_DIR)
