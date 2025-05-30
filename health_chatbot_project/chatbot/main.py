# This file will contain the main application logic for the chatbot.

import sys
# Assuming main.py is run from 'health_chatbot_project' directory (e.g. /app/health_chatbot_project/)
# Command: python3 chatbot/main.py
# In this case, 'health_chatbot_project' (CWD) is added to sys.path, so 'chatbot' package is found.
from chatbot.knowledge_base import load_knowledge_base
from chatbot.nlp import get_response


def run_chatbot_cli():
    """
    Runs the command-line interface for the Health Information Chatbot.
    """
    kb_filepath = "data/health_info.csv" # Relative to CWD (health_chatbot_project)
    knowledge_base = []

    try:
        knowledge_base = load_knowledge_base(kb_filepath)
        if not knowledge_base and knowledge_base != []: # File existed but was empty or parsing failed
             print(f"Warning: Knowledge base at '{kb_filepath}' is empty or could not be loaded properly.")
        print("Welcome to the Health Information Chatbot! Type 'exit' or 'quit' to leave.")
        if not knowledge_base: # Specifically if list is empty after trying to load
             print("Note: Operating with an empty or problematic knowledge base.")
    except FileNotFoundError:
        print(f"Error: Knowledge base file not found at '{kb_filepath}'. Chatbot cannot operate.")
        sys.exit("Exiting application.")
    except Exception as e:
        print(f"An unexpected error occurred while loading the knowledge base: {e}")
        sys.exit("Exiting application due to knowledge base loading error.")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        
        if not user_input:
            print("Chatbot: Please say something.")
            continue

        response = get_response(user_input, knowledge_base)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    run_chatbot_cli()
