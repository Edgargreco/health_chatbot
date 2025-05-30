# This file will contain the Natural Language Processing (NLP) functionalities.

def get_response(user_query: str, knowledge_base: list[dict]) -> str:
    """
    Finds a response in the knowledge base for a given user query.

    Args:
        user_query: The user's question.
        knowledge_base: A list of dictionaries with "Question" and "Answer" keys.

    Returns:
        The corresponding answer if a match is found, otherwise a default message.
    """
    user_query_lower = user_query.lower().strip()
    if not user_query_lower: # Handle empty query after stripping
        return "I'm sorry, I don't have an answer to that question right now."

    for item in knowledge_base:
        # Normalize the question from the knowledge base
        # Lowercase and strip common trailing punctuation
        question_lower = item["Question"].lower().strip().rstrip('?.!') 
        
        if not question_lower: # Skip empty questions in KB if any
            continue

        if user_query_lower in question_lower or question_lower in user_query_lower:
            return item["Answer"]

    return "I'm sorry, I don't have an answer to that question right now."

if __name__ == '__main__':
    # Example Usage for testing
    sample_kb = [
        {"Question": "What are the symptoms of a common cold?", "Answer": "Runny nose, sore throat, cough."},
        {"Question": "How to prevent flu?", "Answer": "Get a flu vaccine, wash hands."},
        {"Question": "What is a healthy diet?", "Answer": "Fruits, vegetables, whole grains."}
    ]

    print("Testing NLP response generation:")

    # Test case 1: Exact match (different case)
    query1 = "what are the symptoms of a common cold?"
    response1 = get_response(query1, sample_kb)
    print(f"Query: '{query1}'\nResponse: '{response1}' (Expected: Runny nose, sore throat, cough.)")

    # Test case 2: Partial match (query in KB question)
    query2 = "symptoms of a common cold"
    response2 = get_response(query2, sample_kb)
    print(f"Query: '{query2}'\nResponse: '{response2}' (Expected: Runny nose, sore throat, cough.)")

    # Test case 3: Partial match (KB question in query)
    query3 = "Tell me about how to prevent flu if possible"
    response3 = get_response(query3, sample_kb)
    print(f"Query: '{query3}'\nResponse: '{response3}' (Expected: Get a flu vaccine, wash hands.)")
    
    # Test case 4: No match
    query4 = "What is the capital of France?"
    response4 = get_response(query4, sample_kb)
    print(f"Query: '{query4}'\nResponse: '{response4}' (Expected: I'm sorry, I don't have an answer...)")

    # Test case 5: Empty query
    query5 = ""
    response5 = get_response(query5, sample_kb)
    print(f"Query: '{query5}'\nResponse: '{response5}' (Expected: I'm sorry, I don't have an answer...)")
    
    # Test case 6: Empty knowledge base
    query6 = "Any question"
    response6 = get_response(query6, [])
    print(f"Query: '{query6}' (empty KB)\nResponse: '{response6}' (Expected: I'm sorry, I don't have an answer...)")

    # Test case 7: Query that is a substring of a KB question which has a question mark
    query7 = "common cold"
    response7 = get_response(query7, sample_kb)
    print(f"Query: '{query7}'\nResponse: '{response7}' (Expected: Runny nose, sore throat, cough.)")

    # Test case 8: KB question (without '?') is substring of user query
    query8 = "how to prevent flu today"
    response8 = get_response(query8, sample_kb)
    print(f"Query: '{query8}'\nResponse: '{response8}' (Expected: Get a flu vaccine, wash hands.)")
