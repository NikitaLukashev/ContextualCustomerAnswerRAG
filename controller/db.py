"""
Database connection module for ChromaDB
"""

import chromadb


class DBConnector:
    def __init__(self, chroma_host: str, chroma_port: int):
        self.chroma_host = chroma_host
        self.chroma_port = chroma_port

    def connect(self):    
        settings = chromadb.config.Settings(
            chroma_api_impl="rest",
            chroma_server_host=self.chroma_host,
            chroma_server_http_port=self.chroma_port
        )
        client = chromadb.HttpClient(settings=settings, host=self.chroma_host, port=self.chroma_port)
        return client
