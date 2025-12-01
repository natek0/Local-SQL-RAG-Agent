import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict

class LocalVectorStore:
    """
    Manages the storage of database schema metadata using ChromaDB.
    Enables 'Schema Retrieval' - finding the right tables for a query.
    """
    
    def __init__(self, collection_name: str = "sql_schema_metadata"):
        # Persistent storage in the ./data folder
        self.client = chromadb.PersistentClient(path="./data/chroma_db")
        
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_ddl(self, ddl: str, table_name: str, description: str):
        """
        Adds a table's DDL and description to the vector store.
        """
        self.collection.add(
            documents=[f"{table_name}: {description}\n\nDDL:\n{ddl}"],
            metadatas=[{"table_name": table_name, "type": "ddl"}],
            ids=[table_name]
        )
        print(f"Indexed schema for table: {table_name}")

    def query(self, user_question: str, n_results: int = 3) -> List[str]:
        """
        Finds the most relevant table schemas for a given user question.
        """
        results = self.collection.query(
            query_texts=[user_question],
            n_results=n_results
        )
        
        if results['documents']:
            return results['documents'][0]
        return []
