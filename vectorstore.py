
from dotenv import load_dotenv
from pinecone import Pinecone, EmbedQuery
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

NAMESPACE = "hr_policy_v2"


def store_in_pinecone(chunks):

    documents = []

    for i, chunk in enumerate(chunks):

        documents.append({
            "_id": f"chunk_{i}",
            "chunk_text": chunk,
            "title": f"Document Chunk {i}"
        })

    print("Uploading documents to Pinecone...")

    # Correct API for your document-schema index
    result = index.documents.batch_upsert(
        namespace=NAMESPACE,
        documents=documents
    )

    if result.errors:

        print("Upload errors:")

        for error in result.errors:
            print(error.error_message)

    else:
        print("All documents uploaded successfully!")

    print("Total documents:", len(documents))


def search_in_pinecone(query, top_k=4):

    results = index.documents.search(
        namespace=NAMESPACE,
        top_k=top_k,
        score_by=[
            EmbedQuery(
                field="chunk_text",
                query=query
            )
        ],
        include_fields=["chunk_text", "title"]
    )

    matched_chunks = []

    for hit in results.matches:

        matched_chunks.append(
            hit.get("chunk_text", "")
        )

    print("Retrieved chunks:", len(matched_chunks))

    return matched_chunks
