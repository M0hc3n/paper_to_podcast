import re
import numpy as np
import random
import soundfile as sf
from kokoro_onnx import Kokoro


class AudioGenerator:
    def __init__(
        self,
        model_path: str,
        voices_path: str,
        host="af_sky",
        learner="af_bella",
        expert="am_fenrir",
    ):
        self.kokoro = Kokoro(model_path, voices_path)

        self.SPEAKER_VOICE_MAP = {"Host": host, "Learner": learner, "Expert": expert}

    def parse_script(self, script: str):
        lines = re.findall(
            r"(Host|Learner|Expert):\s*(.*?)(?=(Host|Learner|Expert|$))",
            script,
            re.DOTALL,
        )
        return [
            {"speaker": speaker, "text": text.strip()} for speaker, text, _ in lines
        ]

    def random_pause(self, sample_rate, min_duration=0.5, max_duration=2.0):
        silence_duration = random.uniform(min_duration, max_duration)
        return np.zeros(int(silence_duration * sample_rate))

    def generate_podcast(self, script: str, output_path: str = "./sample_podcasts"):
        parsed_script = self.parse_script(script)
        audio_segments = []

        for segment in parsed_script:
            speaker = segment["speaker"]
            text = segment["text"]
            voice = self.SPEAKER_VOICE_MAP.get(speaker, "af_sarah")

            samples, sample_rate = self.kokoro.create(
                text, voice=voice, speed=1.0, lang="en-us"
            )

            audio_segments.append(samples)
            audio_segments.append(self.random_pause(sample_rate))  # Add silence

        final_audio = np.concatenate(audio_segments)
        output_filename = (
            f"{output_path}/podcast_{int(np.round(np.random.rand() * 1e6))}.wav"
        )
        sf.write(output_filename, final_audio, sample_rate)
        print(f"Podcast saved as {output_filename}")
        return output_filename
