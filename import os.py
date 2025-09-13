import os
import pandas as pd
import numpy as np
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Initialize OpenAI client with API key
client = OpenAI(api_key="Openai_api_key")

EMBED_MODEL = 'all-MiniLM-L6-v2'
embedder = SentenceTransformer(EMBED_MODEL)

@st.cache_resource
def load_data_and_index():
    # Load dataset directly from GitHub raw URL
    url = "https://raw.githubusercontent.com/HariSoftwaredeveloper/dataset_Q-A/master/train.csv"
    df = pd.read_csv(url)
    
    questions = df["Question"].astype(str).tolist()
    answers = df["Answer"].astype(str).tolist()
    embeddings = embedder.encode(questions, show_progress_bar=True)
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings).astype('float32'))
    return df, index, embeddings

df, index, embeddings = load_data_and_index()

def get_top_k(query, k=3):
    q_emb = embedder.encode([query])
    _, idxs = index.search(np.array(q_emb).astype('float32'), k)
    context = []
    for i in idxs[0]:
        context.append(f"Q: {df.iloc[i]['Question']} A: {df.iloc[i]['Answer']}")
    return "\n".join(context)

def generate_answer(user_query):
    context = get_top_k(user_query, k=3)
    prompt = (
        f"Given the following medical FAQ context, answer the user's question naturally and clearly."
        f"\n\nContext:\n{context}\n\nUser question: {user_query}\nAnswer:"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Act as a helpful medical FAQ assistant. Respond using the provided context only. Do not make up answers."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

st.title("Medical FAQ Chatbot (RAG-Based)")
st.write("Ask any medical question related to our FAQ knowledge base. Example: 'Can children take paracetamol?'")

user_input = st.text_input("Enter your question here:")

if user_input:
    with st.spinner("Retrieving answer..."):
        result = generate_answer(user_input)
    st.success(result)
