from app.config import *

from app.embeddings.embedding_model import EmbeddingModel
from app.vectorstore.qdrant_client import VectorStore


class Retriever:

    def __init__(self):

        self.embedding_model = EmbeddingModel(EMBEDDING_MODEL)

        self.vector_store = VectorStore(
            QDRANT_URL,
            QDRANT_API_KEY
        )

    def retrieve(self, question, top_k=10):

        query_embedding = self.embedding_model.encode([question])[0]

        results = self.vector_store.search(
            COLLECTION_NAME,
            query_embedding,
            top_k
        )

        retrieved_chunks = []

        for point in results.points:

            retrieved_chunks.append({

                "text": point.payload["text"],
                "source": point.payload["source"],
                "score": point.score

            })

        return retrieved_chunks