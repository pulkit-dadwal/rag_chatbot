from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag import RAG


app = FastAPI()

rag = RAG()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    model: str


@app.post("/chat")
def chat(request: ChatRequest):

    return rag.generate(
        question=request.question,
        model=request.model
    )