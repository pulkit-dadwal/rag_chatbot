from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(self, chunk_size, chunk_overlap):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split_documents(self, documents):

        chunks = []

        for document in documents:

            texts = self.splitter.split_text(document["text"])

            for chunk in texts:

                chunks.append({

                    "text": chunk,
                    "source": document["filename"]

                })

        return chunks