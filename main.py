import os
from pydub import AudioSegment
from pydub.effects import speedup
import yaml

def load_config(path):
    """Charge le fichier YAML de configuration"""
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config or {}

def make_noise_same_length(noise, target_ms):
    """Pour que le bruit ait la même durée que la voix"""
    result = noise
    while len(result) < target_ms:
        result += noise
    result = result[:target_ms]
    return result

def add_train_noise_to_voice(voice_audio, noise_audio, noise_level_db):
    """Ajoute le bruit de train à la voix initiale"""
    noise_audio = make_noise_same_length(noise_audio, len(voice_audio))
    noise_audio = noise_audio + noise_level_db
    mixed = voice_audio.overlay(noise_audio)
    return mixed

#Appliquer les effets à l'audio
def process_audio(config):
    """effets définis dans notre configuration.yaml
    """
    audio_cfg = config["audio"]
    effects_cfg = config.get("effects", {})

    audio_path = audio_cfg["input"]
    output_path = audio_cfg["output"]
    audio_format = audio_cfg.get("format", "mp3")

    #Charger l'audio avec PyDub
    audio = AudioSegment.from_file(audio_path, format=audio_format)

    #Volume, ici on interprète la valeur comme un gain en dB
    if "volume" in effects_cfg:
        gain_db = effects_cfg["volume"]
        audio = audio + gain_db

    #Fade out
    if "fade_out" in effects_cfg:
        audio = audio.fade_out(effects_cfg["fade_out"])

    #Fade in 
    if "fade_in" in effects_cfg:
        audio = audio.fade_in(effects_cfg["fade_in"])

    #Vitesse
    if "speed" in effects_cfg:
        audio = speedup(audio, playback_speed=effects_cfg["speed"])

    #Exporte du fichier audio avec les effets appliqués
    audio.export(output_path, format=audio_format)

def main():
    configuration = load_config("configuration.yaml")
    #Partie mixage voix + bruit de train
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

    #Partie effets
    process_audio(configuration)

if __name__ == "__main__":
    main()
