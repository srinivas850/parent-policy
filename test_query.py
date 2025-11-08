from query_agent import query_knowledge_base

# Test questions that parents might ask
test_questions = [
    "What is the GPA requirement for students?",
    "How can I help my student with financial aid?",
    "What support resources are available for mental health?",
    "When does the fall semester start?",
    "What are the housing options for students?",
    "How do I appeal a financial aid decision?",
    "What tutoring services are available?",
    "What are the academic calendar important dates?",
    "How does the admission process work for transfer students?",
    "What happens if my student fails a class?"
]

print("Testing University Knowledge Base for Parents")
print("=" * 50)

for i, question in enumerate(test_questions, 1):
    print(f"\nTest Question {i}: {question}")
    print("-" * 40)
    try:
        answer = query_knowledge_base(question)
        print(answer)
    except Exception as e:
        print(f"Error: {e}")
    print("\n" + "=" * 50)
