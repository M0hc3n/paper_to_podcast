import argparse
import os
from dotenv import load_dotenv

from utils.updated.script_generator import ScriptGenerator

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from the environment variables
API_KEY = os.getenv("API_KEY")

# Check if the keys were retrieved successfully
if API_KEY:
    print("API Key retrieved successfully")
else:
    print("API Key not found")

BASE_URL = os.getenv("BASE_URL")

# Check if the keys were retrieved successfully
if BASE_URL:
    print("BASE_URL retrieved successfully")
else:
    print("BASE_URL not found")

MODEL_NAME = os.getenv("MODEL_NAME")

# Check if the keys were retrieved successfully
if MODEL_NAME:
    print("MODEL_NAME retrieved successfully")
else:
    print("MODEL_NAME not found")

print(MODEL_NAME)

script_generator = ScriptGenerator(
    api_key=API_KEY,
    base_url=BASE_URL,
    model="gemini-2.0-flash",
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
    # generate_podcast(script)
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
