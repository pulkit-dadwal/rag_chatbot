from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from qdrant_client.models import PointStruct


class VectorStore:

    def __init__(self, url, api_key):

        self.client = QdrantClient(
            url=url,
            api_key=api_key,
        )

    def create_collection(self, collection_name, vector_size):

        if self.client.collection_exists(collection_name):
            return

        self.client.create_collection(

            collection_name=collection_name,

            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    def upload(self, collection_name, embeddings, chunks):

        points = []

        for idx, (embedding, chunk) in enumerate(zip(embeddings, chunks)):

            points.append(

                PointStruct(

                    id=idx,

                    vector=embedding.tolist(),

                    payload={

                        "text": chunk["text"],
                        "source": chunk["source"]

                    }

                )

            )

        self.client.upsert(

            collection_name=collection_name,

            points=points

        )


    def search(self, collection_name, query_embedding, limit=3):
        results = self.client.query_points(
            collection_name=collection_name,
            query=query_embedding.tolist(),
            limit=limit,
        )

        return results