from retrieval.vector_store import vector_search
from retrieval.bm25_retriever import BM25Retriever
from retrieval.ensemble_retriever import ensemble_rank
from config import TOP_K

def retrieval_agent(state):
    print("Executing 3-Stage Hybrid Retrieval...")
    query = state["query"]
    min_exp = state.get("min_experience", 0) 
    resumes = state["resumes"]

    # STAGE 1: Metadata Filtering (Pre-filtering the BM25 Corpus)
    print(f"  -> Stage 1: Metadata Filter (Experience >= {min_exp})")
    filtered_resumes = [r for r in resumes if r["metadata"]["experience"] >= min_exp]

    if not filtered_resumes:
        print("     No candidates passed the experience filter.")
        state["retrieved"] = []
        return state

    # STAGE 2: Dense Retrieval (Vector Search with DB-level Metadata Filter)
    print("  -> Stage 2: Dense Retrieval (Semantic Vector Search)")
    vector_results = vector_search(query, TOP_K, min_exp)

    # STAGE 3: Sparse Retrieval (BM25 on the filtered corpus)
    print("  -> Stage 3: Sparse Retrieval (BM25 Keyword Search)")
    bm25 = BM25Retriever(filtered_resumes)
    sparse_results = bm25.search(query, TOP_K)

    # Combine: Resolve ties and combine results using wRRF
    print("  -> Fusing results with Ensemble Ranker...")
    ranked = ensemble_rank(vector_results, sparse_results)

    state["retrieved"] = ranked
    return state