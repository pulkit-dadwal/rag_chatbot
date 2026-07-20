from app.config import HF_TOKEN
from huggingface_hub import InferenceClient

class HuggingFaceLLM:
    def __init__(self):
        self.client = InferenceClient(
            api_key = HF_TOKEN
        )

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=512,
        )

        return response.choices[0].message.content