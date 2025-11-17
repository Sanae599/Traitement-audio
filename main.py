import os
from pydub import AudioSegment
import yaml

def load_config(path): 
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

def make_noise_same_length(noise, target_ms):
    """
    POur étendre ou couper le bruit des autres audios pour qu'ils aient la même durée que la voix
    """
    result = noise
    while len(result) < target_ms:
        result += noise
    result = result[:target_ms]
    return result


def add_train_noise_to_voice(voice_audio, noise_audio, noise_level_db):
    """
    Afin d'ajouter le bruit de train à la voix intiale
    """
    noise_audio = make_noise_same_length(noise_audio, len(voice_audio))
    noise_audio = noise_audio + noise_level_db
    mixed = voice_audio.overlay(noise_audio)
    return mixed


def main():
    configuration = load_config("configuration.yaml")

    input_voice_path = configuration["input_voice"]
    background_noise_path = configuration["background_noise"]
    output_dir = configuration["output_dir"]
    output_filename = configuration["output_filename"]
    noise_level_db = configuration["noise_level_db"]
    output_formats = configuration["output_formats"]

    voice_audio = AudioSegment.from_file(input_voice_path)
    noise_audio = AudioSegment.from_file(background_noise_path)

    mixed_audio = add_train_noise_to_voice(voice_audio, noise_audio, noise_level_db)
    base_output_path = os.path.join(output_dir, output_filename)

    for fmt in output_formats:
        output_path = f"{base_output_path}.{fmt}"
        mixed_audio.export(output_path, format=fmt)


if __name__ == "__main__":
    main()
