# DocuLens — PDF Research Assistant

**DocuLens** is a lightweight document-retrieval application that helps users find relevant information in PDF files. Upload your documents, ask a question, and inspect the passages most closely related to your query.

## Features

- 📄 Upload multiple PDF documents
- 🔎 Retrieve relevant passages using TF-IDF and cosine similarity
- 📌 Display source filenames and page numbers
- 📊 Show similarity scores for retrieved passages
- 🖥️ Simple, interactive Streamlit interface
- 🔐 Process documents locally without sending them to an external LLM API

## Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **PDF extraction:** pypdf
- **Text retrieval:** scikit-learn
- **Similarity measurement:** Cosine similarity

## How It Works

1. Upload one or more PDF documents.
2. Extract selectable text from each page.
3. Split the text into overlapping passages.
4. Convert passages into TF-IDF vectors.
5. Rank passages according to their cosine similarity to the user's question.
6. Display the most relevant passages with source information.

## Installation

**Prerequisites:** Python 3.10 or newer and pip.

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/DocuLens-PDF-Assistant.git
cd DocuLens-PDF-Assistant
```

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python -m streamlit run app.py
```

Open the local URL printed in your terminal.

## Current Limitations

- Retrieves relevant passages instead of generating natural-language answers.
- Uses lexical similarity rather than semantic embeddings.
- Scanned PDFs without selectable text are not automatically OCR-processed.
- Tables and image-based content may not be extracted accurately.
- Similarity scores indicate textual relevance, not factual correctness.

## Future Improvements

- Add LLM-based answers grounded in retrieved passages.
- Integrate semantic embeddings and vector search.
- Improve retrieval evaluation and citation accuracy.
- Add OCR support for scanned documents.
- Include automated tests and a sample evaluation dataset.

## Privacy

Documents are processed within the running application session. This starter does not intentionally send uploaded PDFs to an external LLM service. Avoid uploading sensitive documents to hosted instances unless their privacy practices are understood.

## Project Status

Learning and development prototype.

## License

Choose and add an appropriate license before redistributing the project. Check the licenses of all dependencies and any third-party materials.

