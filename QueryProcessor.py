
from vectorstore import search_in_pinecone
from llm import query_llm_with_context


def process_user_query(query: str):

    matched_chunks = search_in_pinecone(query)

    print("\n========== RETRIEVED CHUNKS ==========")

    for i, chunk in enumerate(matched_chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)

    context = "\n\n".join(matched_chunks)

    response = query_llm_with_context(query, context)

    print("\n========== ANSWER ==========")
    print(response)

    return response


if __name__ == "__main__":

    user_query = "what is the cgpa of candidate"

    process_user_query(user_query)
