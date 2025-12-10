"""Vector store management using ChromaDB."""

import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings


class VectorStore:
    """Vector store for documentation embeddings."""
    
    def __init__(self, persist_directory: str, collection_name: str = "documentation"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the ChromaDB collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Documentation embeddings"},
        )
    
    def add_chunks(self, chunks: List[Dict]):
        """
        Add chunks with embeddings to the store.
        
        Args:
            chunks: List of chunk dictionaries with 'text', 'metadata', 'embedding'
        """
        ids = []
        embeddings = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            # Generate ID from metadata
            chunk_id = self._generate_id(chunk["metadata"], i)
            ids.append(chunk_id)
            
            embeddings.append(chunk["embedding"])
            documents.append(chunk["text"])
            
            # Prepare metadata (ChromaDB requires string values)
            metadata = {
                "url": str(chunk["metadata"].get("url", "")),
                "title": str(chunk["metadata"].get("title", "")),
                "type": str(chunk["metadata"].get("type", "page")),
                "format": str(chunk["metadata"].get("format", "generic")),
                "chunk_id": str(chunk["metadata"].get("chunk_id", i)),
            }
            metadatas.append(metadata)
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        filter_dict: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Search for similar chunks using an embedding.
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of result dictionaries with 'text', 'metadata', 'distance'
        """
        # Use embedding search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_dict,
        )
        
        # Format results
        formatted_results = []
        if results.get("ids") and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None,
                })
        
        return formatted_results
    
    def search_with_embedding(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        filter_dict: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Search using a pre-computed embedding.
        
        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of result dictionaries
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_dict,
        )
        
        formatted_results = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None,
                })
        
        return formatted_results
    
    def _generate_id(self, metadata: Dict, index: int) -> str:
        """Generate a unique ID for a chunk."""
        import hashlib
        import json
        
        id_string = f"{metadata.get('url', '')}-{metadata.get('chunk_id', index)}"
        return hashlib.md5(id_string.encode()).hexdigest()
    
    def get_collection_info(self) -> Dict:
        """Get information about the collection."""
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
        }

