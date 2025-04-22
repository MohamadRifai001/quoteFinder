import os
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

chroma_client = chromadb.PersistentClient(path="./vector_store")

collection = chroma_client.get_or_create_collection("pdf_chunks")

def scan_and_embed_pdfs(input_folder):
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        reader = PdfReader(os.path.join(input_folder, filename))
        for i, page in enumerate(reader.pages):
            text = (page.extract_text() or "").replace("\n", " ").strip()
            if not text:
                continue

            embedding = embedding_model.encode(text).tolist()
            metadata = {"source_file": filename, "original_page": i + 1}
            chunk_id = f"{filename}_page_{i+1}"

            # Avoid duplicate insert
            try:
                collection.add(
                    documents=[text],
                    embeddings=[embedding],
                    metadatas=[metadata],
                    ids=[chunk_id]
                )
            except chromadb.errors.DuplicateIDError:
                continue  # Already added

def semantic_search(query, top_k=5):
    query_vec = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_vec], n_results=top_k)
    return results
