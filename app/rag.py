from torch import chunk

from app.query import Retriever
from app.llms.huggingface_llm import HuggingFaceLLM
from app.llms.gemini_llm import GeminiLLM
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

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

        logger.info("=" * 80)
        logger.info(f"Query: {question}")
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")

        for i, chunk in enumerate(retrieved_chunks, start=1):

            logger.info(
                f"Chunk {i} | "
                f"Score: {chunk['score']:.4f} | "
                f"Source: {chunk['source']}"
            )
            logger.info(f"Text: {chunk['text'][:200]}...")


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
        
        logger.info(f"Model Used: {model}")
        logger.info(f"Answer: {answer}")
        logger.info("=" * 80)
        

        return {

            "answer": answer,

            "sources": list(
                set(
                    chunk["source"]
                    for chunk in retrieved_chunks
                )
            )

        }