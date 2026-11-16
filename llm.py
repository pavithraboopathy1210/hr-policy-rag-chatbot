
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def query_llm_with_context(query: str, context: str) -> str:
    system_content = """You are a helpful assistant for answering user queries
based on the provided context.

Use the context to provide accurate and relevant answers.
Do not make assumptions beyond the context provided.

If the context does not contain enough information to answer the query,
let the user know that you cannot provide an answer based on the given context.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"""
{system_content}

Query: {query}

Context:
{context}
""",
        config={
            "temperature": 0.4
        }
    )

    return response.text
