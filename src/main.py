import sys
import os

# Add src to path so we can import modules easily
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.rag_controller.py import RAGController
from scripts.setup_data import create_financial_db

def main():
    db_path = "data/finance.db"
    
    # Ensure DB exists
    if not os.path.exists(db_path):
        print("Initializing Database...")
        create_financial_db(db_path)
        
    agent = RAGController(db_path)
    
    # Index Schema (One time setup)
    agent.index_database()
    
    print("\n--- Local SQL Agent Ready ---")
    print("Ask questions about: AAPL, MSFT, Tech Sector, Stock Prices...")
    
    while True:
        try:
            q = input("\nQuery: ")
            if q.lower() in ['exit', 'quit']:
                break
                
            df = agent.ask(q)
            print("\nResult:")
            print(df.to_markdown(index=False))
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
