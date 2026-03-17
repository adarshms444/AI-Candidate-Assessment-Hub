import chromadb
from sentence_transformers import SentenceTransformer
from config import VECTOR_DB_PATH

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = client.get_or_create_collection("resumes")

def index_resumes(resumes):
    # FIX: Delete old data so we don't get duplicate candidates on multiple runs
    existing = collection.get()
    if existing['ids']:
        collection.delete(ids=existing['ids'])

    for r in resumes:
        emb = model.encode(r["text"]).tolist()
        collection.upsert(
            ids=[r["id"]],
            embeddings=[emb],
            documents=[r["text"]],
            metadatas=[r["metadata"]]
        )

def vector_search(query, k, min_exp=0):
    emb = model.encode(query).tolist()
    res = collection.query(
        query_embeddings=[emb], 
        n_results=k,
        where={"experience": {"$gte": min_exp}}
    )
    if not res["documents"] or len(res["documents"][0]) == 0:
        return []
    return list(zip(res["documents"][0], res["distances"][0]))