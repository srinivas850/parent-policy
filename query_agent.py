import os
import logging
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the vector store
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    logger.info("Vector store loaded successfully")
except Exception as e:
    logger.error(f"Error loading vector store: {e}")
    raise

# Custom prompt template for parent-focused responses
parent_prompt_template = """
You are a helpful AI assistant designed to help parents understand university policies and resources from their perspective. 
You have access to comprehensive information about university policies, academic calendars, support resources, and other important information for parents.

Use the following pieces of context to answer the question at the end. If you don't know the answer based on the provided context, say so clearly and suggest where the parent might find more information.

Always provide responses that are:
- Clear and easy to understand for parents
- Comprehensive but not overwhelming
- Action-oriented where appropriate
- Empathetic to parental concerns
- Focused on helping parents advocate for or assist their student

Context:
{context}

Question: {question}

Helpful Answer:"""

PROMPT = PromptTemplate(
    template=parent_prompt_template, input_variables=["context", "question"]
)

# Create retrieval QA chain with custom prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp"),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)

def query_knowledge_base(question):
    """
    Query the university knowledge base with parent-focused responses.
    
    Args:
        question (str): The question from the parent
        
    Returns:
        str: The AI-generated answer
    """
    try:
        logger.info(f"Processing question: {question}")
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        sources = result["source_documents"]
        
        # Log sources used
        source_files = [doc.metadata.get('source', 'Unknown') for doc in sources]
        logger.info(f"Sources used: {source_files}")
        
        return answer
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        error_str = str(e)
        if 'insufficient_quota' in error_str:
            return "I'm sorry, but the AI service is currently unavailable due to quota limitations. Please check your Gemini API account billing or try again later. For immediate assistance, contact the university directly."
        else:
            return "I'm sorry, I encountered an error while processing your question. Please try rephrasing or contact the university directly for assistance."

if __name__ == "__main__":
    while True:
        question = input("Ask a question about university policies and resources: ")
        if question.lower() == 'exit':
            break
        answer = query_knowledge_base(question)
        print(f"Answer: {answer}")
