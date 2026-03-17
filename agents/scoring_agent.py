import re
import numpy as np
from sentence_transformers import SentenceTransformer
from config import SKILL_WEIGHTS

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def semantic_match(skill, text, threshold=0.32):
    # FIX: Split by comma, period, newline, semicolon, or pipe to isolate list items
    chunks = [s.strip() for s in re.split(r'[.,\n;|-]', text) if len(s.strip()) > 2]
    
    if not chunks: 
        return False
    
    skill_emb = model.encode(skill)
    chunk_embs = model.encode(chunks)
    
    norms_text = np.linalg.norm(chunk_embs, axis=1)
    norm_skill = np.linalg.norm(skill_emb)
    
    valid = (norms_text > 0) & (norm_skill > 0)
    sims = np.zeros(len(chunks))
    sims[valid] = np.dot(chunk_embs[valid], skill_emb) / (norms_text[valid] * norm_skill)
    
    # Check if the skill matches ANY chunk above the threshold
    return np.max(sims) > threshold

def scoring_agent(state):
    print("Executing Scoring Agent...")
    job = state["job_clusters"]
    results = []

    for resume, _ in state["retrieved"]:
        total = 0
        for cluster, skills in job.items():
            if not skills: continue
            
            # Count how many skills in this cluster match the resume
            matches = sum(semantic_match(s, resume) for s in skills)
            
            # Calculate ratio and apply the cluster weight
            ratio = matches / len(skills)
            total += ratio * SKILL_WEIGHTS[cluster]
            
        results.append((resume, total))

    # Sort descending by score
    state["scores"] = sorted(results, key=lambda x: x[1], reverse=True)
    return state



