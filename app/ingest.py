from config import *
from loaders.pdf_loader import PDFLoader
from chunking.text_splitter import TextChunker
from embeddings.embedding_model import EmbeddingModel
from vectorstore.qdrant_client import VectorStore


loader = PDFLoader(DOCUMENT_PATH)

print("Loading PDFs...")
documents = loader.load_documents()
if not documents:
    print("No PDF files found.")
    exit(1)

chunker = TextChunker(
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

print("Chunking documents...")
chunks = chunker.split_documents(documents)
if not chunks:
    print("No chunks were created.")
    exit(1)

embedding_model = EmbeddingModel(EMBEDDING_MODEL)

print("Generating embeddings...")
embeddings = embedding_model.encode(
    [chunk["text"] for chunk in chunks]
)

vector_store = VectorStore(
    QDRANT_URL,
    QDRANT_API_KEY
)

print("Creating collection...")
if not documents:
    print("No PDF files found.")
    exit(1)

vector_store.create_collection(
    COLLECTION_NAME,
    embeddings.shape[1]
)

print("Uploading vectors...")
vector_store.upload(
    COLLECTION_NAME,
    embeddings,
    chunks
)

print("\nKnowledge base created successfully.\n")
print(f"Documents loaded : {len(documents)}")
print(f"Chunks created   : {len(chunks)}")
print(f"Vectors uploaded : {len(embeddings)}")