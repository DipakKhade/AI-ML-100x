
"""
    1. read the data
    2. create a chunks out of it
    3. make embedding from chunks
    4. store that embedding to vector db e.g chromadb, qudrant, etc
    5. get the relevent embedding based on user prompt and attach it with the user prompt
"""

from langchain_community.document_loaders import PyPDFLoader

data = PyPDFLoader(file_path='/Users/dipakkhade/projects/AI-ML-100x/week-09 RAG from the Ground Up - Part 1 /docs/Mahabharata.pdf')
docs = data.load()
print(docs[:10])