# This file will contain unit tests for the chatbot functionalities.

import unittest
import os
import sys

# Ensure the 'chatbot' module can be found by adding the project root to sys.path
# This is often necessary when running tests directly or via some IDEs if the project structure isn't automatically recognized.
# For `python -m unittest discover tests` from the project root, this might not be strictly needed,
# but it adds robustness for other execution methods.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chatbot.knowledge_base import load_knowledge_base
from chatbot.nlp import get_response

class TestChatbotFunctionality(unittest.TestCase):

    def setUp(self):
        """Setup common resources for tests if any (e.g., temp files)."""
        # Path to the real knowledge base file, assuming tests are run from project root
        self.kb_filepath = "data/health_info.csv"
        self.non_existent_filepath = "data/non_existent_kb.csv"

        # Sample knowledge base for testing get_response directly
        self.sample_kb = [
            {"Question": "What is a cold?", "Answer": "A cold is a common illness."},
            {"Question": "How to treat fever?", "Answer": "Rest and fluids."},
            {"Question": "Any advice on headache?", "Answer": "Pain relievers and rest."}
        ]
        self.default_no_answer = "I'm sorry, I don't have an answer to that question right now."

    # --- Tests for knowledge_base.py ---
    def test_load_knowledge_base_success(self):
        """Test loading a valid knowledge base CSV file."""
        kb = load_knowledge_base(self.kb_filepath)
        self.assertIsInstance(kb, list, "Knowledge base should be a list.")
        self.assertTrue(len(kb) > 0, "Knowledge base should not be empty.")
        
        # Check structure of the first item
        if len(kb) > 0:
            first_item = kb[0]
            self.assertIsInstance(first_item, dict, "Each item in KB should be a dictionary.")
            self.assertIn("Question", first_item, "KB item should have a 'Question' key.")
            self.assertIn("Answer", first_item, "KB item should have an 'Answer' key.")

    def test_load_knowledge_base_file_not_found(self):
        """Test loading a non-existent CSV file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError, msg="Should raise FileNotFoundError for non-existent file."):
            load_knowledge_base(self.non_existent_filepath)

    # --- Tests for nlp.py (get_response) ---
    def test_get_response_known_question_exact_match(self):
        """Test get_response with an exact match question."""
        response = get_response("What is a cold?", self.sample_kb)
        self.assertEqual(response, "A cold is a common illness.")

    def test_get_response_known_question_case_insensitive(self):
        """Test get_response with case-insensitive matching."""
        response = get_response("what IS a CoLd?", self.sample_kb)
        self.assertEqual(response, "A cold is a common illness.", "Should match irrespective of case.")

    def test_get_response_partial_match_query_in_kb(self):
        """Test get_response with user query being a substring of a KB question."""
        # Example: "cold" is in "What is a cold?"
        response = get_response("cold", self.sample_kb)
        self.assertEqual(response, "A cold is a common illness.")

    def test_get_response_partial_match_kb_in_query(self):
        """Test get_response with KB question being a substring of user query."""
        # Example: "any advice on headache" (from "Any advice on headache?") in 
        # "Could you give me any advice on headache please?"
        # Note: nlp.py strips trailing '?' from KB questions.
        response = get_response("Could you give me any advice on headache please?", self.sample_kb)
        self.assertEqual(response, "Pain relievers and rest.")
        
    def test_get_response_unknown_question(self):
        """Test get_response with a question not in the knowledge base."""
        response = get_response("What is the meaning of life?", self.sample_kb)
        self.assertEqual(response, self.default_no_answer)

    def test_get_response_empty_query(self):
        """Test get_response with an empty user query."""
        response = get_response("", self.sample_kb)
        self.assertEqual(response, self.default_no_answer)
        
    def test_get_response_empty_query_with_spaces(self):
        """Test get_response with a user query that is only spaces."""
        response = get_response("   ", self.sample_kb)
        self.assertEqual(response, self.default_no_answer, "Query with only spaces should be treated as empty.")

    def test_get_response_no_kb_provided(self):
        """Test get_response with an empty knowledge base list."""
        response = get_response("Any question", [])
        self.assertEqual(response, self.default_no_answer)

    def test_get_response_question_with_punctuation_in_kb(self):
        """Test matching when KB question has punctuation (e.g., '?') that should be stripped."""
        # nlp.py's get_response strips '?.!' from KB questions before matching.
        # sample_kb has "Any advice on headache?"
        response = get_response("advice on headache", self.sample_kb)
        self.assertEqual(response, "Pain relievers and rest.")

if __name__ == '__main__':
    # This allows running the tests directly from this file:
    # python tests/test_chatbot.py
    # However, `python -m unittest discover tests` from project root is standard.
    unittest.main()
