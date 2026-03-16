
"""
    1. read the data
    2. create a chunks out of it
    3. make embedding from chunks
    4. store that embedding to vector db e.g chromadb, qudrant, etc
    5. get the relevent embedding based on user prompt and attach it with the user prompt
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings


data = PyPDFLoader(file_path='/Users/dipakkhade/Documents/JOB DOCS/AppointmentLetter_DeepakPermenant.pdf')
docs = data.load()


txt_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=400 
)

document_chunks = txt_splitter.split_documents(documents=docs)

texts = [doc.page_content for doc in document_chunks]

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

embeddings = embeddings_model.embed_documents(texts=texts)
print(f"Generated {len(embeddings)} embeddings.")


chroma_client = chromadb.HttpClient(host='localhost', port=8000)

print(chroma_client.heartbeat())