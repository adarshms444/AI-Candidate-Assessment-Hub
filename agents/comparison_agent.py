import math
from components.llm import get_llm

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def comparison_agent(state):
    print("Executing Comparison Agent (Tie-Breaker)...")
    scores = state["scores"]
    if len(scores) < 2: return state

    a_resume, a_score = scores[0]
    b_resume, b_score = scores[1]

    prob = sigmoid(a_score - b_score)
    state["comparison_prob"] = prob

    if 0.45 <= prob <= 0.55:
        llm = get_llm()
        prompt = f"""
        Compare Candidate A and Candidate B for a GenAI Engineer role.
        Candidate A: {a_resume[:800]}
        Candidate B: {b_resume[:800]}
        Who is a better fit? Reply ONLY with 'Candidate A' or 'Candidate B'.
        """
        response = llm.invoke(prompt).content
        if "Candidate B" in response:
            scores[0], scores[1] = scores[1], scores[0]
            state["scores"] = scores

    return state