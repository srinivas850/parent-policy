# TODO: Change OpenAI API to Gemini API

- [x] Update requirements_new.txt: Replace langchain-openai with langchain-google-genai
- [x] Update query_agent.py: Change import from langchain_openai.OpenAI to langchain_google_genai.GoogleGenerativeAI
- [x] Update query_agent.py: Replace OpenAI() with GoogleGenerativeAI(model="gemini-1.5-flash")
- [x] Update query_agent.py: Change error message from OpenAI to Gemini
- [x] Test the changes by running test_query.py (Note: Requires GOOGLE_API_KEY in .env file for Gemini API) - API key added, test passed successfully
