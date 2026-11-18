
from vectorstore import search_in_pinecone
from llm import query_llm_with_context

from semantic_cache import (
    get_cached_answer,
    store_cached_answer
)


def process_user_query(query: str):

    print("\n========== SEMANTIC CACHE CHECK ==========")

    # STEP 1: Check Valkey semantic cache
    cached_answer, question_embedding = get_cached_answer(query)

    if cached_answer is not None:

        print("Returning answer from Valkey cache.")

        return cached_answer

    print("Cache miss. Running RAG pipeline...")

    # STEP 2: Retrieve relevant HR policy chunks from Pinecone
    matched_chunks = search_in_pinecone(query)

    print("\n========== RETRIEVED CHUNKS ==========")

    for i, chunk in enumerate(matched_chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)

    context = "\n\n".join(matched_chunks)

    # STEP 3: Generate answer using Gemini
    response = query_llm_with_context(query, context)

    print("\n========== ANSWER ==========")
    print(response)

    # STEP 4: Store the new answer in Valkey
    store_cached_answer(
        query,
        response,
        question_embedding
    )

    return response


if __name__ == "__main__":

    user_query = "what is the cgpa of candidate"

    process_user_query(user_query)
