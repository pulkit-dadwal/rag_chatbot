from query import Retriever
from llms.huggingface_llm import HuggingFaceLLM
from llms.gemini_llm import GeminiLLM


class RAG:

    def __init__(self, qwen=HuggingFaceLLM(), gemini="gemini-2.5-flash"):

        self.retriever = Retriever()
        self.qwen = qwen
        self.gemini= GeminiLLM(model_name=gemini)

    def build_prompt(self, question, retrieved_chunks):
        if not retrieved_chunks:
            return {
                "answer": "I couldn't find any relevant information in the knowledge base.",
                "sources": []
            }

        context = "\n\n".join(
            chunk["text"] for chunk in retrieved_chunks
        )

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the information contained in the provided context.

Do not use outside knowledge.

If the answer cannot be found in the context, reply exactly:

"I couldn't find that information in the provided documents."

Keep the answer concise and accurate.

Context:
{context}

Question:
{question}

Answer:
"""

        return prompt

    def generate(self, question, model="gemini"):

        retrieved_chunks = self.retriever.retrieve(question)

        prompt = self.build_prompt(
            question,
            retrieved_chunks
        )

        if model == "qwen":

            answer = self.qwen.invoke(prompt)

        elif model == "gemini":

            answer= self.gemini.generate(prompt)

        else:

            raise ValueError("Unsupported model")
        

        return {

            "answer": answer,

            "sources": list(
                set(
                    chunk["source"]
                    for chunk in retrieved_chunks
                )
            )

        }