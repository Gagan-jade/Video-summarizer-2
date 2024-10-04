import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

# Fetch environment variables from .env
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Optional print to verify
print("LANGCHAIN_TRACING_V2:", LANGCHAIN_TRACING_V2)
print("LANGCHAIN_ENDPOINT:", LANGCHAIN_ENDPOINT)
print("LANGCHAIN_API_KEY:", LANGCHAIN_API_KEY)
print("LANGCHAIN_PROJECT:", LANGCHAIN_PROJECT)
print("GOOGLE_API_KEY:", GOOGLE_API_KEY)


chat = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.4, google_api_key=GOOGLE_API_KEY, convert_system_message_to_human=True)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=1000):
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        if current_length + len(sentence.split()) > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(sentence)
        current_length += len(sentence.split())
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


def create_faiss_index(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Using a smaller, efficient model
    chunk_embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(chunk_embeddings.shape[1])  # L2 distance for similarity
    index.add(np.array(chunk_embeddings))
    return index, chunk_embeddings

def retrieve_relevant_chunks(query, index, chunks, chunk_embeddings, top_k=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query])
    _, I = index.search(query_embedding, top_k)
    return [chunks[i] for i in I[0]]

def answer_question(chat, retrieved_chunks, user_query):
    # Combine retrieved chunks and user's query
    context = " ".join(retrieved_chunks)
    message = [
        SystemMessage(content=f"Use the following context to answer: {context}"),
        HumanMessage(content=user_query)
    ]
    result = chat.invoke(message)
    return result


pdf_path = r"C:\Users\Arnav\Desktop\msd\attention_is_all_you_need.pdf"

pdf_text = extract_text_from_pdf(pdf_path)

chunks = chunk_text(pdf_text)

index, chunk_embeddings = create_faiss_index(chunks)

user_query = "In brief give me the major important topics being discussed in this pdf"
retrieved_chunks = retrieve_relevant_chunks(user_query, index, chunks, chunk_embeddings)

response = answer_question(chat, retrieved_chunks, user_query)

# Display the response
print(response.content)