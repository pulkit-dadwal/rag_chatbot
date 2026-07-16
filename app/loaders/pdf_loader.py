import fitz
from pathlib import Path


class PDFLoader:

    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)

    def load_documents(self):

        documents = []

        for pdf in self.folder_path.glob("*.pdf"):

            doc = fitz.open(pdf)

            text = ""

            for page in doc:
                text += page.get_text()

            documents.append({
                "filename": pdf.name,
                "text": text
            })

        return documents