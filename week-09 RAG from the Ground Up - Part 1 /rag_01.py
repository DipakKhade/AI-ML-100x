
"""
    1. read the data
    2. create a chunks out of it
    3. make embedding from chunks
    4. store that embedding to vector db e.g chromadb, qudrant, etc
    5. get the relevent embedding based on user prompt and attach it with the user prompt
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

data = PyPDFLoader(file_path='/Users/dipakkhade/projects/AI-ML-100x/week-09 RAG from the Ground Up - Part 1 /docs/Mahabharata.pdf')
docs = data.load()
print(docs[:10])


txt_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=400 
)

chunks = txt_splitter.split_documents(documents=docs)

