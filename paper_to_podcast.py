import argparse
import os
from templates import enhance_prompt, initial_dialogue_prompt, plan_prompt
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from utils.script import generate_script, parse_script_plan
from utils.free_audio_gen import generate_podcast
from langchain_google_genai import ChatGoogleGenerativeAI

from openai import OpenAI


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
    print("API Key retrieved successfully")
else:
    print("API Key not found")

MODEL_NAME = os.getenv("MODEL_NAME")

# Check if the keys were retrieved successfully
if MODEL_NAME:
    print("API Key retrieved successfully")
else:
    print("API Key not found")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

llm = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[{"role": "system", "content": "You are a helpful assistant."}],
)


# chains
chains = {
    "plan_script_chain": plan_prompt | llm | parse_script_plan,
    "initial_dialogue_chain": initial_dialogue_prompt | llm | StrOutputParser(),
    "enhance_chain": enhance_prompt | llm | StrOutputParser(),
}


def main(pdf_path):
    # Step 1: Generate the podcast script from the PDF
    print("Generating podcast script...")
    script = generate_script(pdf_path, chains, llm)
    print("Podcast script generation complete!")

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
