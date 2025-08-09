# Error handling - Robust error management and logging
"""
RAG system implementation using ChromaDB and Mistral LLM
"""

import os
import chromadb
import re
import numpy as np
from typing import List, Dict, Any
from mistralai import Mistral
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from .db import DBConnector
from .llm_handler import MistralLLM

class RAGHandler:
    def __init__(self, chroma_client, mistral_client):
        """
        Initialize the RAG system with ChromaDB and Mistral clients
        """
        self.chroma_client = chroma_client
        self.mistral_client = mistral_client
        
        # Initialize sentence transformer for embeddings
        self.embedding_model = 'mistral-embed'
        # Create or get collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="airbnb_listing",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize Mistral LLM
        self.llm = MistralLLM()

        
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks
        """
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        chunks = text_splitter.split_text(text)
        return chunks
    
    def process_airbnb_listing(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process the Airbnb listing file and return structured data
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean the content
        content = re.sub(r'\n+', '\n', content)
        content = re.sub(r'\s+', ' ', content)
        
        # Split into chunks
        chunks = self.chunk_text(content)

        # Create documents with metadata
        documents = [Document(page_content=chunk) for chunk in chunks]
        return documents

    def get_text_embedding(self, input):
        embeddings_batch_response = self.mistral_client.embeddings.create(
          model="mistral-embed",
            inputs=input
        )
        return embeddings_batch_response.data[0].embedding

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector database
        """
        texts = [doc.page_content for doc in documents]
        ids = [str(i) for i in range(len(documents))]
        embeddings = np.array([self.get_text_embedding(chunk) for chunk in texts])
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids
        )
        

    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant documents
        """
        
        
        query_embedding = np.array([self.get_text_embedding(query)])
            
        # Search in collection
        results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
         
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection
        """
        count = self.collection.count()
        return {
            'collection_name': self.collection.name,
            'document_count': count,
        }
    
    def search_with_llm(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Search for relevant documents and generate LLM response
        """
        
        # Input validation
        if not query or not query.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        
        if n_results <= 0:
            raise ValueError("n_results must be a positive integer")
        
        if n_results > 5:  # Reasonable upper limit
            raise ValueError("n_results cannot exceed 5")
        
        
        # First, search for relevant documents
        search_results = self.search(query, n_results)
            
        # If LLM is available, generate response
        if self.llm:
            try:
                llm_response = self.llm.generate_response(query, search_results)
                    
                return {
                    "query": query,
                    "llm_response": llm_response,
                    "results": search_results
                }
            except Exception as e:                
                return {
                    "query": query,
                    "llm_response": "Sorry, I couldn't generate a response at the moment.",
                    "error": str(e),
                    "results": search_results                    }
        else:
            return {
                    "query": query,
                    "llm_response": "LLM not available. Here are the retrieved documents:",
                    "results": search_results
                }
        
    
    def get_llm_status(self) -> Dict[str, Any]:
        """
        Get the status of the LLM integration
        """
        print(self.llm)
        return {
            "llm_available": self.llm is not None,
            "llm_model": "mistral-large-latest" if self.llm else None,
            "llm_error": None if self.llm else "LLM not initialized"
        }