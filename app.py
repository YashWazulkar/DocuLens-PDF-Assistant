import io
import re
from typing import List

import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="DocuLens — PDF Research Assistant", page_icon="📚", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1100px; padding-top: 2rem;}
.hero {padding: 1.5rem 1.7rem; border-radius: 18px; background: linear-gradient(120deg,#102a43,#243b53); color: white; margin-bottom: 1rem;}
.hero h1 {color: white; margin-bottom: .25rem;}
.small-muted {color: #64748b; font-size: .9rem;}
.source-card {padding: 1rem; border: 1px solid #dbe4ee; border-radius: 12px; margin-bottom: .7rem;}
</style>
<div class="hero">
  <h1>📚 DocuLens</h1>
  <p>Ask questions about your PDFs and inspect the passages that support each result.</p>
</div>
""", unsafe_allow_html=True)

st.caption("Local retrieval-augmented generation (RAG) prototype. It retrieves relevant passages; it does not call an external LLM.")
uploads = st.file_uploader("Upload one or more PDF documents", type=["pdf"], accept_multiple_files=True)

def split_chunks(text: str, chunk_words: int = 180, overlap: int = 35) -> List[str]:
    words = re.findall(r"\S+", text)
    if not words:
        return []
    chunks = []
    step = max(1, chunk_words - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_words])
        if chunk:
            chunks.append(chunk)
        if start + chunk_words >= len(words):
            break
    return chunks

@st.cache_data(show_spinner=False)
def extract_pdf(file_bytes: bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page_no, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            pages.append((page_no, text))
    return pages

documents = []
if uploads:
    with st.spinner("Reading PDFs…"):
        for upload in uploads:
            pages = extract_pdf(upload.getvalue())
            for page_no, page_text in pages:
                for chunk_no, chunk in enumerate(split_chunks(page_text), start=1):
                    documents.append({
                        "filename": upload.name,
                        "page": page_no,
                        "chunk": chunk_no,
                        "text": chunk
                    })

if uploads and not documents:
    st.warning("No selectable text was found. Scanned PDFs may need OCR before they can be searched.")

if documents:
    st.success(f"Indexed {len(documents)} passages from {len(uploads)} PDF(s).")
    question = st.text_input("Ask a question", placeholder="What are the main findings or key dates?")
    top_k = st.slider("Passages to retrieve", min_value=1, max_value=min(8, len(documents)), value=min(4, len(documents)))
    if st.button("Find relevant passages", type="primary", disabled=not question.strip()):
        corpus = [d["text"] for d in documents]
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=30000)
        matrix = vectorizer.fit_transform(corpus + [question])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
        ranked = scores.argsort()[::-1][:top_k]
        if not len(ranked) or max(scores) <= 0:
            st.info("No strong text match was found. Try different wording or check whether the PDF contains searchable text.")
        else:
            st.subheader("Retrieved evidence")
            st.write("These are the most similar passages, ranked by text similarity. Read them before relying on an answer.")
            for rank, idx in enumerate(ranked, start=1):
                item = documents[int(idx)]
                st.markdown(f"""
                <div class="source-card">
                <b>{rank}. {item['filename']}</b> · page {item['page']} · similarity {scores[idx]:.3f}<br><br>
                {item['text'].replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}
                </div>
                """, unsafe_allow_html=True)
                st.caption(f"Source: {item['filename']} — page {item['page']}, passage {item['chunk']}")
            st.info("Prototype limitation: this version retrieves evidence but does not generate a natural-language synthesis. It may miss tables, images, or scanned text.")

with st.expander("How this works"):
    st.markdown("""
    1. Extract selectable text from uploaded PDFs with `pypdf`.
    2. Split text into overlapping passages.
    3. Build TF-IDF vectors and rank passages by cosine similarity to your question.
    4. Show source filenames, page numbers, and similarity scores for inspection.

    Files are processed in this Streamlit session; this app does not intentionally upload PDFs to an external service.
    """)
