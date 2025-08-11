"""
Mistral LLM integration for the RAG system
"""

import os
from mistralai import Mistral
from typing import List, Dict, Any, Optional

class MistralLLM:
    def __init__(self, api_key: str = None):
        """
        Initialize Mistral LLM client
        """
        self.api_key = api_key or os.getenv('MISTRAL_API_KEY')
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is required")
        
        self.client = Mistral(api_key=self.api_key)
        self.model = "mistral-large-latest"
    
    def generate_response(self, 
                         query: str, 
                         context: List[Dict[str, Any]]) -> str:
        """
        Generate a response using Mistral Large based on the query and retrieved context
        """
        
        if not context:
            return "I couldn't find any relevant information to answer your question."
        
        try:
            # Build the context from retrieved documents
            context_text = "\n".join([
                result['text']
                for result in context
            ])
            
            # Create the user message with context and query
            user_message = f"""Based on the following context from an Airbnb listing, please answer this question: {query}

Context:
{context_text}

Please provide a short and concise answer, don't be too verbose unless it's explicitly asked.
If you are not very confident in the answer, say 'I don't know'.
"""
            
            # Create chat messages
            messages = [
                {
                    "role": "user",
                    "content": user_message,
                }
            ]
            
            # Generate response from Mistral
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                max_tokens=50,
                temperature=0.2,
                top_p=0.2
            )
            
            response_text = response.choices[0].message.content
            
            return response_text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_enhanced_search(self, 
                                query: str, 
                                context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an enhanced search response with both retrieved documents and LLM-generated answer
        """
        # Get LLM response
        llm_response = self.generate_response(query, context)
        
        return {
            "query": query,
            "llm_response": llm_response,
            "retrieved_documents": context,
            "total_documents": len(context)
        }
