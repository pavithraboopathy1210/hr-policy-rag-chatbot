
import uuid
import numpy as np

from valkey import Valkey
from sentence_transformers import SentenceTransformer


# VALKEY CONFIGURATION

VALKEY_HOST = "localhost"
VALKEY_PORT = 6379

INDEX_NAME = "hr_semantic_cache_index"
KEY_PREFIX = "semantic_cache:hr_policy_v2:"

CACHE_TTL = 3600

# Maximum allowed cosine distance
MAX_DISTANCE = 0.40

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384


# INITIALIZE VALKEY

valkey_client = Valkey(
    host=VALKEY_HOST,
    port=VALKEY_PORT,
    decode_responses=False
)

embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


# CREATE VECTOR INDEX

def create_cache_index():

    try:
        valkey_client.execute_command(
            "FT.CREATE",
            INDEX_NAME,
            "ON", "HASH",
            "PREFIX", "1", KEY_PREFIX,
            "SCHEMA",
            "question", "TEXT",
            "answer", "TEXT",
            "embedding",
            "VECTOR", "HNSW", "6",
            "TYPE", "FLOAT32",
            "DIM", str(EMBEDDING_DIMENSION),
            "DISTANCE_METRIC", "COSINE"
        )

        print("Semantic cache index created successfully.")

    except Exception as error:

        if "already exists" in str(error).lower():
            print("Semantic cache index already exists.")
        else:
            raise error


# GENERATE EMBEDDING

def generate_embedding(question):

    embedding = embedding_model.encode(
        question,
        normalize_embeddings=True
    )

    return np.asarray(embedding, dtype=np.float32)


# SEARCH SEMANTIC CACHE

def get_cached_answer(question):

    question_embedding = generate_embedding(question)

    query_vector = question_embedding.tobytes()

    try:

        results = valkey_client.execute_command(
            "FT.SEARCH",
            INDEX_NAME,
            "*=>[KNN 1 @embedding $vector AS score]",
            "PARAMS", "2",
            "vector", query_vector,
            "RETURN", "3",
            "answer",
            "question",
            "score",
            "DIALECT", "2"
        )

        print("Raw cache search results:", results)

        if not results or int(results[0]) == 0:

            print("SEMANTIC CACHE: MISS")

            return None, question_embedding

        fields = results[2]

        cached_data = {}

        for i in range(0, len(fields), 2):

            key = fields[i]
            value = fields[i + 1]

            if isinstance(key, bytes):
                key = key.decode("utf-8")

            cached_data[key] = value

        distance = float(cached_data["score"])

        print("Cache similarity distance:", distance)

        if distance <= MAX_DISTANCE:

            answer = cached_data["answer"]

            if isinstance(answer, bytes):
                answer = answer.decode("utf-8")

            print("SEMANTIC CACHE: HIT")

            return answer, question_embedding

        print("SEMANTIC CACHE: MISS")

        return None, question_embedding

    except Exception as error:

        print("Cache search error:", error)

        return None, question_embedding


# STORE ANSWER IN VALKEY

def store_cached_answer(question, answer, question_embedding):

    try:

        cache_key = KEY_PREFIX + str(uuid.uuid4())

        valkey_client.hset(
            cache_key,
            mapping={
                "question": question,
                "answer": answer,
                "embedding": question_embedding.tobytes()
            }
        )

        valkey_client.expire(cache_key, CACHE_TTL)

        print("Answer stored in semantic cache.")

    except Exception as error:

        print("Cache storage error:", error)


# CREATE INDEX

create_cache_index()
