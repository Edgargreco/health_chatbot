# This file will manage the chatbot's knowledge base and data retrieval.

import csv
import os # Added import

def load_knowledge_base(filepath: str) -> list[dict]:
    """
    Loads a knowledge base from a CSV file.

    The CSV file should have two columns: "Question" and "Answer".

    Args:
        filepath: The path to the CSV file.

    Returns:
        A list of dictionaries, where each dictionary has "Question"
        and "Answer" keys.

    Raises:
        FileNotFoundError: If the CSV file is not found at the given path.
    """
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            knowledge_base = []
            for row in reader:
                knowledge_base.append({"Question": row["Question"], "Answer": row["Answer"]})
            return knowledge_base
    except FileNotFoundError:
        # Re-raise the exception to be handled by the caller
        raise
    except Exception as e:
        # For other potential errors during CSV parsing
        print(f"An error occurred while loading the knowledge base: {e}")
        return []

if __name__ == '__main__':
    # Example usage for testing (optional)
    # Create a dummy CSV for testing if you don't have one
    # with open("dummy_kb.csv", "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Question", "Answer"])
    #     writer.writerow(["Test Q1?", "Test A1."])
    #     writer.writerow(["Test Q2?", "Test A2."])

    # Test with an existing file
    # Construct path relative to this script's location
    script_dir = os.path.dirname(__file__)
    kb_file = os.path.join(script_dir, "..", "data", "health_info.csv")
    # Normalize the path (e.g., collapses ".." components)
    kb_file = os.path.normpath(kb_file)

    print(f"Attempting to load knowledge base from: {kb_file}")
    try:
        kb = load_knowledge_base(kb_file)
        if kb:
            print("Knowledge base loaded successfully:")
            for item in kb:
                print(f"  Q: {item['Question']} -> A: {item['Answer']}")
        elif not kb and kb != []: # Check if it's an empty list due to an error other than FileNotFoundError
             print("Knowledge base loading resulted in an empty list, but not due to FileNotFoundError.")
        # If FileNotFoundError was raised, this part won't be reached if not caught locally.
    except FileNotFoundError:
        print(f"Error: The file '{kb_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Test with a non-existent file
    non_existent_file = "non_existent_kb.csv"
    print(f"\nAttempting to load knowledge base from non-existent file: {non_existent_file}")
    try:
        kb_non_existent = load_knowledge_base(non_existent_file)
        if not kb_non_existent: # It should raise FileNotFoundError, so this might not be hit as expected
            print("Successfully handled non-existent file (returned empty list or no error). This might indicate an issue if FileNotFoundError was expected.")
    except FileNotFoundError:
        print(f"Successfully caught FileNotFoundError for '{non_existent_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred while testing non-existent file: {e}")
