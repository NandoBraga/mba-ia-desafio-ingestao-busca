import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
PG_VECTOR_COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")

if not all([PDF_PATH, OPENAI_EMBEDDING_MODEL, PG_VECTOR_COLLECTION_NAME, DATABASE_URL]):
    raise ValueError("Certifique-se de que todas as variáveis de ambiente necessárias estão definidas: PDF_PATH, OPENAI_EMBEDDING_MODEL, PG_VECTOR_COLLECTION_NAME, DATABASE_URL")


def ingest_pdf():
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        add_start_index=False).split_documents(docs) 

    if not splits:
        raise SystemExit("Processo de ingestão interrompido devido à ausência de documentos.")

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]    

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = OpenAIEmbeddings(
        model=OPENAI_EMBEDDING_MODEL)

    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)
    print(f"Ingestão concluída. {len(enriched)} documentos foram processados e armazenados.")


if __name__ == "__main__":
    ingest_pdf()