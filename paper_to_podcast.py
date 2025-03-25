import argparse
from dotenv import load_dotenv

from utils.script_generator import ScriptGenerator
from utils.audio_generator import AudioGenerator
from utils.utils import load_keys

load_dotenv()

API_KEY, BASE_URL, MODEL_NAME = load_keys()

script_generator = ScriptGenerator(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="gemini-2.0-flash",
)

audio_generator = AudioGenerator(
    model_path="./kokoro/kokoro-v1.0.onnx",
    voices_path="./kokoro/voices-v1.0.bin",
)


def main(pdf_path):
    # Step 1: Generate the podcast script from the PDF
    print("Generating podcast script...")
    # script = generate_script(pdf_path, chains, llm)
    script = script_generator.generate_script(pdf_path)
    print("Podcast script generation complete!")

    print(script)
    print("Generating podcast audio files...")
    # # Step 2: Generate the podcast audio files and merge them
    audio_generator.generate_podcast(script)
    print("Podcast generation complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a podcast from a research paper."
    )
    parser.add_argument(
        "pdf_path", type=str, help="Path to the research paper PDF file."
    )

    args = parser.parse_args()
    main(args.pdf_path)
