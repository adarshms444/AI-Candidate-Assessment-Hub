from config import SEMANTIC_WEIGHT, BM25_WEIGHT

def ensemble_rank(vector_results, bm25_results, k=60):
    rrf_scores = {}
    vector_ranked = sorted(vector_results, key=lambda x: x[1])
    bm25_ranked = sorted(bm25_results, key=lambda x: x[1], reverse=True)

    for rank, (doc, _) in enumerate(vector_ranked):
        rrf_scores[doc] = rrf_scores.get(doc, 0) + (SEMANTIC_WEIGHT * (1 / (k + rank + 1)))

    for rank, (doc, _) in enumerate(bm25_ranked):
        rrf_scores[doc] = rrf_scores.get(doc, 0) + (BM25_WEIGHT * (1 / (k + rank + 1)))

    return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)