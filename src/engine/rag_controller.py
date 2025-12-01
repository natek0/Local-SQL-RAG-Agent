from typing import Optional
import pandas as pd
from ..llm.ollama_client import OllamaHandler
from ..vector.chroma_store import LocalVectorStore
from ..db.sqlite_handler import SQLiteHandler

class RAGController:
    def __init__(self, db_path: str):
        self.vector_store = LocalVectorStore()
        self.llm = OllamaHandler()
        self.db = SQLiteHandler(db_path)
        
    def index_database(self):
        """
        Reads the DB schema and embeds it into the vector store.
        """
        print("Indexing database schema...")
        full_ddl = self.db.get_schema()
        # Simple splitting by 'CREATE TABLE' for this demo
        tables = full_ddl.split('CREATE TABLE')
        for t in tables:
            if t.strip():
                # Re-add the split keyword and index
                ddl = 'CREATE TABLE' + t
                # Extract table name safely
                try:
                    name = t.split('(')[0].strip().replace('"', '')
                    self.vector_store.add_ddl(ddl, name, "Financial Data Table")
                except:
                    continue

    def _sanitize_sql(self, llm_response: str) -> str:
        """
        Cleans the LLM output to extract just the SQL.
        """
        sql = llm_response.replace('```sql', '').replace('```', '').strip()
        return sql

    def ask(self, question: str, max_retries: int = 3) -> pd.DataFrame:
        """
        The Main Loop: Retrieve -> Generate -> Validate -> Repair
        """
        # 1. Retrieval
        context = self.vector_store.query(question)
        
        # 2. Initial Prompt
        prompt = f"""
        You are an expert SQL Data Analyst.
        Schema Context: {context}
        
        Question: {question}
        
        Return ONLY valid SQL. No explanations.
        """
        
        current_sql = self._sanitize_sql(self.llm.complete(prompt))
        
        # 3. Validation Loop
        for attempt in range(max_retries):
            print(f"Executing Attempt #{attempt+1}: {current_sql}")
            
            df, error = self.db.execute(current_sql)
            
            if error is None:
                return df # Success!
                
            # 4. Self-Correction
            print(f"SQL Failed: {error}. Attempting repair...")
            repair_prompt = f"""
            The following SQL failed:
            {current_sql}
            
            Error Message:
            {error}
            
            Schema Context:
            {context}
            
            Fix the SQL to solve the error. Return ONLY the fixed SQL.
            """
            current_sql = self._sanitize_sql(self.llm.complete(repair_prompt))
            
        raise Exception(f"Failed to generate valid SQL after {max_retries} attempts.")
