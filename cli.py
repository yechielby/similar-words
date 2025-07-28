import requests
import argparse

BASE_URL = "http://localhost:8000"

def get_similar_words(word):
    """Get similar words (anagrams) for a given word"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/similar", params={"word": word})
        if response.status_code == 200:
            data = response.json()
            similar = data.get("similar", [])
            if similar:
                print(f"\n✅ Similar words to '{word}':")
                for i, sim_word in enumerate(similar, 1):
                    print(f"  {i}. {sim_word}")
            else:
                print(f"\n📝 No similar words found for '{word}'")
        else:
            error_data = response.json()
            print(f"\n❌ Error: {error_data.get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Cannot connect to API at {BASE_URL}")
        print("Make sure the API server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def add_word(word):
    """Add a new word to the database"""
    try:
        response = requests.post(f"{BASE_URL}/api/v1/add-word", json={"word": word})
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ {data.get('detail', 'Word added successfully')}")
        else:
            error_data = response.json()
            print(f"\n❌ Error: {error_data.get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Cannot connect to API at {BASE_URL}")
        print("Make sure the API server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def get_stats(from_date=None, to_date=None, endpoint=None):
    """Get API statistics"""
    try:
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if endpoint:
            params["endpoint"] = endpoint
            
        response = requests.get(f"{BASE_URL}/api/v1/stats", params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 API Statistics:")
            print(f"  Total Words: {data.get('totalWords', 0):,}")
            print(f"  Total Requests: {data.get('totalRequests', 0):,}")
            print(f"  Avg Processing Time: {data.get('avgProcessingTimeMs', 0):.2f} microseconds")
            
            if from_date or to_date or endpoint:
                print(f"\n🔍 Filters applied:")
                if from_date:
                    print(f"  From: {from_date}")
                if to_date:
                    print(f"  To: {to_date}")
                if endpoint:
                    print(f"  Endpoint: {endpoint}")
        else:
            error_data = response.json()
            print(f"\n❌ Error: {error_data.get('detail', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Cannot connect to API at {BASE_URL}")
        print("Make sure the API server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

def interactive_mode():
    """Interactive CLI mode"""
    print("🔤 Similar Words API - Interactive Mode")
    print("=" * 40)
    print("Commands:")
    print("  1. find <word>     - Find similar words")
    print("  2. add <word>      - Add new word")
    print("  3. stats           - Show statistics")
    print("  4. help            - Show this help")
    print("  5. quit            - Exit")
    print("=" * 40)
    
    while True:
        try:
            user_input = input("\n> ").strip().lower()
            
            if user_input == "quit" or user_input == "exit":
                print("👋 Goodbye!")
                break
            elif user_input == "help":
                print("\nCommands:")
                print("  find <word>     - Find similar words")
                print("  add <word>      - Add new word")
                print("  stats           - Show statistics")
                print("  help            - Show this help")
                print("  quit            - Exit")
            elif user_input == "stats":
                get_stats()
            elif user_input.startswith("find "):
                word = user_input[5:].strip()
                if word:
                    get_similar_words(word)
                else:
                    print("❌ Please provide a word: find <word>")
            elif user_input.startswith("add "):
                word = user_input[4:].strip()
                if word:
                    add_word(word)
                else:
                    print("❌ Please provide a word: add <word>")
            elif user_input == "":
                continue
            else:
                print("❌ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break

def main():
    parser = argparse.ArgumentParser(description="Similar Words API CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Similar words command
    similar_parser = subparsers.add_parser("find", help="Find similar words (anagrams)")
    similar_parser.add_argument("word", help="Word to find anagrams for")
    
    # Add word command
    add_parser = subparsers.add_parser("add", help="Add a new word to database")
    add_parser.add_argument("word", help="Word to add")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get API statistics")
    stats_parser.add_argument("--from", dest="from_date", help="Start date (ISO 8601 format)")
    stats_parser.add_argument("--to", dest="to_date", help="End date (ISO 8601 format)")
    stats_parser.add_argument("--endpoint", help="Filter by specific endpoint")
    
    # Interactive mode
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive mode")
    
    args = parser.parse_args()
    
    if args.command == "find":
        get_similar_words(args.word)
    elif args.command == "add":
        add_word(args.word)
    elif args.command == "stats":
        get_stats(args.from_date, args.to_date, args.endpoint)
    elif args.command == "interactive":
        interactive_mode()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()