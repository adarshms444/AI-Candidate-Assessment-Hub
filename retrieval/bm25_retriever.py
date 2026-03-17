from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self, resumes):
        self.texts = [r["text"].split() for r in resumes]
        self.raw = [r["text"] for r in resumes]
        if self.texts:
            self.bm25 = BM25Okapi(self.texts)
        else:
            self.bm25 = None

    def search(self, query, k):
        if not self.bm25: return []
        scores = self.bm25.get_scores(query.split())
        ranked = sorted(zip(self.raw, scores), key=lambda x: x[1], reverse=True)
        return ranked[:k]