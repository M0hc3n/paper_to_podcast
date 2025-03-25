import logging
from typing import List, Dict
from PyPDF2 import PdfReader
from openai import OpenAI
from .templates import PodcastScriptTemplates

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScriptGenerator:
    def __init__(
        self, api_key: str, base_url: str = None, model: str = "gpt-3.5-turbo"
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.templates = PodcastScriptTemplates()

    def _parse_pdf(self, pdf_path: str) -> str:
        try:
            pdf_reader = PdfReader(pdf_path)
            extracted_text = []

            for page in pdf_reader.pages:
                text = page.extract_text()
                extracted_text.append(text)

                # Stop collecting after conclusion
                if "Conclusion" in text:
                    break

            return "\n".join(extracted_text)
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise

    def _generate_completion(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            raise

    def generate_script(self, pdf_path: str) -> str:
        paper_text = self._parse_pdf(pdf_path)

        # Generate script plan
        plan_messages = [
            {"role": "system", "content": "You are an expert podcast script planner."},
            {
                "role": "user",
                "content": self.templates.format_prompt(
                    self.templates.PLAN_PROMPT, paper=paper_text[:5000]
                ),
            },
        ]
        script_plan = self._generate_completion(plan_messages)

        # Generate initial dialogue
        initial_dialogue_messages = [
            {
                "role": "system",
                "content": "You are an expert podcast introduction writer.",
            },
            {
                "role": "user",
                "content": self.templates.format_prompt(
                    self.templates.INITIAL_DIALOGUE_PROMPT, paper_head=paper_text[:1000]
                ),
            },
        ]
        initial_dialogue = self._generate_completion(initial_dialogue_messages)

        # Combine initial dialogue and script plan
        full_script = initial_dialogue + "\n\n" + script_plan

        # Optional: Enhance script
        enhance_messages = [
            {"role": "system", "content": "You are a podcast script enhancer."},
            {
                "role": "user",
                "content": self.templates.format_prompt(
                    self.templates.ENHANCE_PROMPT, draft_script=full_script
                ),
            },
        ]
        enhanced_script = self._generate_completion(enhance_messages)

        return enhanced_script

    def generate_section_dialogue(
        self, section_plan: str, previous_dialogue: str, additional_context: str = ""
    ) -> str:
        dialogue_messages = [
            {"role": "system", "content": "You are an expert podcast dialogue writer."},
            {
                "role": "user",
                "content": self.templates.format_prompt(
                    self.templates.DISCUSS_PROMPT,
                    section_plan=section_plan,
                    previous_dialogue=previous_dialogue,
                    additional_context=additional_context,
                ),
            },
        ]
        return self._generate_completion(dialogue_messages)
