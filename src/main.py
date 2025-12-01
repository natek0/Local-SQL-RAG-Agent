import sys
import os

# Add src to path so we can import modules easily
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.rag_controller import RAGController
from scripts.setup_data import create_financial_db

def main():
    db_path = "data/finance.db"
    
    if not os.path.exists(db_path):
        print("Initializing Database...")
        create_financial_db(db_path)
        
    agent = RAGController(db_path)
    
    # Check if we need to index (simple check if chroma exists)
    # For this demo, we can just run it safely; Chroma handles duplicates well enough or we skip
    # agent.index_database() # Uncomment if you need to re-index
    
    print("\n--- Local SQL Agent Ready (with Text2Viz) ---")
    print("Ask questions about: AAPL, MSFT, Tech Sector, Stock Prices...")
    print("Try: 'Show me the daily closing prices for Apple'")
    
    while True:
        try:
            q = input("\nQuery: ")
            if q.lower() in ['exit', 'quit']:
                break
                
            df, fig = agent.ask(q)
            
            print("\nResult Data:")
            print(df.head().to_markdown(index=False))
            
            if fig:
                output_file = "latest_chart.html"
                fig.write_html(output_file)
                print(f"\n[Visualization Generated] Saved to {output_file}")
                # Try to open it automatically on Mac
                os.system(f"open {output_file}")
            else:
                print("\n[No Visualization] Data structure did not match visualization rules.")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
