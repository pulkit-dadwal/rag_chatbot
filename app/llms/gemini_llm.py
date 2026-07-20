from google import genai

from app.config import GEMINI_API_KEY
from app.llms.base_llm import BaseLLM


class GeminiLLM(BaseLLM):

    def __init__(self, model_name="gemini-2.5-flash"):

        self.model_name = model_name

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        return response.text