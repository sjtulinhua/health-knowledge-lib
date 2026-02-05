"""Script to load knowledge base data from JSON files into ChromaDB."""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.services.knowledge_loader import get_knowledge_loader
from app.services.rag import get_rag_service


def main():
    """Load all knowledge data from JSON files."""
    print("=" * 50)
    print("Knowledge Base Loader")
    print("=" * 50)
    
    # Get services
    loader = get_knowledge_loader()
    rag = get_rag_service()
    
    # Check current stats
    stats = rag.get_stats()
    print(f"\nCurrent knowledge base: {stats['total_documents']} documents")
    
    # Load all JSON files
    print("\nLoading knowledge files...")
    results = loader.load_all_json_files()
    
    if results:
        print("\nLoad results:")
        for filename, count in results.items():
            if isinstance(count, int):
                print(f"  ✓ {filename}: {count} items loaded")
            else:
                print(f"  ✗ {filename}: {count}")
    else:
        print("No JSON files found in knowledge_base directory")
    
    # Show final stats
    stats = rag.get_stats()
    print(f"\nTotal documents in knowledge base: {stats['total_documents']}")
    print("\n" + "=" * 50)
    print("Knowledge base loading complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
