import re
import numpy as np
import random
import soundfile as sf
from kokoro_onnx import Kokoro

# the following chcices were taken after several iterations of testing, feel free to check
# other available voices here: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md#american-english
SPEAKER_VOICE_MAP = {"Host": "af_sky", "Learner": "af_bella", "Expert": "am_fenrir"}

# make sure to install those files at the correct location
# use: wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
#      wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
# if the above links aren't working, you can check the repo's README instructions here:
# https://github.com/thewh1teagle/kokoro-onnx/blob/main/README.md
kokoro = Kokoro("./kokoro/kokoro-v1.0.onnx", "./kokoro/voices-v1.0.bin")


def parse_script(script):
    """Extracts speaker-text pairs from the given script."""
    lines = re.findall(
        r"(Host|Learner|Expert):\s*(.*?)(?=(Host|Learner|Expert|$))", script, re.DOTALL
    )
    return [{"speaker": speaker, "text": text.strip()} for speaker, text, _ in lines]


def random_pause(sample_rate, min_duration=0.5, max_duration=2.0):
    """Generates a random silence duration between sentences."""
    silence_duration = random.uniform(min_duration, max_duration)
    silence = np.zeros(int(silence_duration * sample_rate))
    return silence


def generate_podcast(script):
    """Generates and merges audio from the script using Kokoro ONNX."""
    parsed_script = parse_script(script)
    audio_segments = []

    for segment in parsed_script:
        speaker = segment["speaker"]
        text = segment["text"]
        voice = SPEAKER_VOICE_MAP.get(speaker, "af_sarah")

        # print(f"Generating audio for {speaker}: {text}") #? consider this in case of debugging

        samples, sample_rate = kokoro.create(
            text,
            voice=voice,
            speed=1.0,
            lang="en-us",
        )

        audio_segments.append(samples)
        audio_segments.append(
            random_pause(sample_rate=sample_rate)
        )  # adds some silence between sentences

    # Merge all audio parts
    final_audio = np.concatenate(audio_segments)

    # Save the generated podcast
    output_filename = (
        f"./sample_podcasts/podcast_{int(np.round(np.random.rand() * 1e6))}.wav"
    )
    sf.write(output_filename, final_audio, sample_rate)
    print(f"Podcast saved as {output_filename}")
