from query_agent import query_knowledge_base

# Test the function
question = "What are the admission policies?"
try:
    answer = query_knowledge_base(question)
    print("Test successful!")
    print(f"Answer: {answer[:100]}...")  # Print first 100 chars
except Exception as e:
    print(f"Error: {e}")
