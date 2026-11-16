from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "Employees are allowed 12 days of casual leave.",
    "Employees can work from home."
]

embeddings = model.encode(sentences)

print(embeddings.shape)
print(embeddings[0])