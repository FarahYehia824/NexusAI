import os
import logging
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# الموديل اللي هيحول النص لأرقام (embeddings)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

DOCUMENTS_DIR = "documents"
VECTOR_STORE_DIR = "vector_store"


def read_pdf_text(filepath: str) -> str:
    """بتقرا كل الـ PDF وترجع النص كله كـ string واحد"""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list:
    """بتقسم النص الطويل لقطع صغيرة (chunks)، مع overlap بسيط عشان منفقدش سياق"""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def build_vector_store():
    """
    بتقرا كل ملفات PDF جوه documents/، تقطعهم، تحولهم لـ embeddings،
    وتخزنهم في FAISS index على الهارد
    """
    all_chunks = []
    all_sources = []

    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            logger.info(f"Reading: {filename}")
            text = read_pdf_text(filepath)
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            all_sources.extend([filename] * len(chunks))

    logger.info(f"Total chunks created: {len(all_chunks)}")

    # تحويل كل الـ chunks لأرقام
    embeddings = embedding_model.encode(all_chunks)
    embeddings = np.array(embeddings).astype('float32')

    # بناء الـ FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # حفظ الـ index والـ chunks على الهارد
    faiss.write_index(index, os.path.join(VECTOR_STORE_DIR, "index.faiss"))
    with open(os.path.join(VECTOR_STORE_DIR, "chunks.pkl"), "wb") as f:
        pickle.dump({"chunks": all_chunks, "sources": all_sources}, f)

    logger.info("Vector store built and saved successfully.")


def search(query: str, top_k: int = 3) -> list:
    """بتاخد سؤال، وترجع أقرب top_k chunks ليه في المعنى"""
    index = faiss.read_index(os.path.join(VECTOR_STORE_DIR, "index.faiss"))
    with open(os.path.join(VECTOR_STORE_DIR, "chunks.pkl"), "rb") as f:
        data = pickle.load(f)

    query_embedding = embedding_model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append({
            "chunk": data["chunks"][idx],
            "source": data["sources"][idx]
        })

    logger.info(f"Search query: '{query}' -> {len(results)} results found")
    return results