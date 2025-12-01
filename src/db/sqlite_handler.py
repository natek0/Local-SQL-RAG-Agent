import sqlite3
import pandas as pd
from typing import Tuple, Optional, Any

class SQLiteHandler:
    """
    Handles database connections and safe query execution.
    Acts as the 'Runtime Environment' for the generated code.
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    def execute(self, sql_query: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Executes a SQL query and returns either the result (as DataFrame) 
        OR the error message.
        
        Returns:
            (DataFrame, None) if success
            (None, ErrorMessage) if failure
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # We use pandas for easy result formatting
                df = pd.read_sql_query(sql_query, conn)
                return df, None
        except Exception as e:
            return None, str(e)
            
    def get_schema(self) -> str:
        """
        Helper to dump the current database schema for indexing.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return "\n\n".join([t[0] for t in tables if t[0] is not None])
