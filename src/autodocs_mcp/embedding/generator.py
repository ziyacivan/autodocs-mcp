"""Embedding generation for documentation chunks."""

from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """Generate embeddings for documentation content."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        """
        Initialize the embedding generator.

        Args:
            model_name: Name of the sentence transformer model
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _load_model(self):
        """Lazy load the model."""
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)

    def chunk_text(self, text: str, metadata: Dict) -> List[Dict[str, str]]:
        """
        Split text into chunks with metadata.

        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk

        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []

        # Simple chunking by character count
        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for i in range(end, max(start, end - 100), -1):
                    if text[i] in ".!?\n":
                        end = i + 1
                        break

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_metadata = {
                    **metadata,
                    "chunk_id": chunk_id,
                    "chunk_start": start,
                    "chunk_end": end,
                }
                chunks.append(
                    {
                        "text": chunk_text,
                        "metadata": chunk_metadata,
                    }
                )
                chunk_id += 1

            # Move start position with overlap
            start = end - self.chunk_overlap

        return chunks

    def generate_embeddings(self, chunks: List[Dict[str, str]]) -> List[Dict]:
        """
        Generate embeddings for text chunks.

        Args:
            chunks: List of chunk dictionaries with 'text' and 'metadata'

        Returns:
            List of dictionaries with 'text', 'metadata', and 'embedding'
        """
        self._load_model()

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=False)

        results = []
        for i, chunk in enumerate(chunks):
            results.append(
                {
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "embedding": embeddings[i].tolist(),
                }
            )

        return results

    def process_pages(self, pages: List[Dict[str, str]]) -> List[Dict]:
        """
        Process pages into chunks and generate embeddings.

        Args:
            pages: List of page dictionaries with 'content', 'url', 'title', etc.

        Returns:
            List of chunk dictionaries with embeddings
        """
        all_chunks = []

        for page in pages:
            content = page.get("content", "")
            if not content:
                continue

            # Create metadata for chunks
            metadata = {
                "url": page.get("url", ""),
                "title": page.get("title", ""),
                "type": page.get("type", "page"),
                "format": page.get("format", "generic"),
            }

            # Chunk the content
            chunks = self.chunk_text(content, metadata)

            # Generate embeddings
            embedded_chunks = self.generate_embeddings(chunks)
            all_chunks.extend(embedded_chunks)

        return all_chunks
