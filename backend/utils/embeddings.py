import openai
from pinecone import Pinecone, ServerlessSpec
import uuid
from typing import List
import os

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT") 
INDEX_NAME = os.getenv("INDEX_NAME")

def init_pinecone():
    """Initialize Pinecone connection and return index."""
    try:
        # Initialize Pinecone client
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # List existing indexes
        existing_indexes = pc.list_indexes().names()

        # Ensure the index exists before connecting
        if INDEX_NAME not in existing_indexes:
            print(f"[⚠️] Index '{INDEX_NAME}' does not exist")
            return

        # Connect to the index
        index = pc.Index(INDEX_NAME)
        print(f"[✅] Connected to Pinecone index: {INDEX_NAME}")
        return index

    except Exception as e:
        print(f"[❌] Error initializing Pinecone: {e}")
        return None

def generate_embeddings(text: str) -> List[float]:
    """
    Generates an embedding for the given text using OpenAI.
    
    Args:
        text (str): The input text to embed.
    
    Returns:
        List[float]: A list of floating-point numbers representing the embedding.
    """
    try:
        response = openai.embeddings.create(input=[text], model="text-embedding-3-large")
        embedding = response.data[0].embedding
        print(f"[✅] Successfully generated embedding for: '{text[:30]}...'")
        return embedding
    except Exception as e:
        print(f"[❌] Error generating embedding: {e}")
        return []

def store_embedding(text: str, id: int) -> int:
    """
    Stores an embedding in the Pinecone index with error handling.

    Args:
        text (str): The input text to embed and store.
        id (str): A unique identifier to associate with the embedding.

    Returns:
        int: 1 if success, 0 if failure.
    """
    index = init_pinecone()
    
    if index is None:
        print("[⚠️] Pinecone index not initialized. Skipping storage.")
        return 0

    embedding = generate_embeddings(text)
    
    if not embedding:
        print("[⚠️] Failed to generate embedding. Skipping storage.")
        return 0
    
    unique_id = str(uuid.uuid4())  # Generate a unique ID
    
    try:
        index.upsert(vectors=[(unique_id, embedding, {"text": text, "id": str(id)})])
        print(f"[✅] Stored embedding with ID: {unique_id}")
        return 1
    except Exception as e:
        print(f"[❌] Error storing embedding in Pinecone: {e}")
        return 0
    

def match_embeddings(user_embedding, top_k=3):
    """
    Matches the user_embedding against stored embeddings in Pinecone and returns
    the index of the most similar match.

    Parameters:
    - user_embedding (list): The query embedding.
    - index (pinecone.Index): The Pinecone index to query.
    - top_k (int): Number of top matches to retrieve (default is 1).

    Returns:
    - str: The ID of the highest similarity match.
    """

    index = init_pinecone()
    
    if index is None:
        print("[⚠️] Pinecone index not initialized. Skipping storage.")
        return -1
    
    try:
        # Perform similarity search
        results = index.query(vector=user_embedding, top_k=top_k, include_metadata=True)

        if results and results['matches']:
            top_matches = results['matches']  
            match_ids = [match['metadata']['id'] for match in top_matches]  # Extract IDs

            print(f"[✅] Top {top_k} Matches: {match_ids}")
            return match_ids
        else:
            print("[⚠️] No matches found.")
            return None

    except Exception as e:
        print(f"[❌] Error matching embeddings: {e}")
        return -1

