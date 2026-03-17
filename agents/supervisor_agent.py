def supervisor_agent(state):
    print("Executing Supervisor Routing...")
    scores = state["scores"]
    
    if not scores:
        state["route"] = "reject"
        return state

    best_score = scores[0][1]

    # FIX: Update thresholds to match the new realistic math
    if best_score < 0.25:
        state["route"] = "reject"
    elif len(scores) > 1 and best_score < 0.55:
        state["route"] = "compare"
    else:
        state["route"] = "explain"

    return state