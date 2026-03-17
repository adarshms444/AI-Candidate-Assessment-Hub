from components.llm import get_llm

llm = get_llm()

def get_fit_label(score):
    if score >= 0.70: return "High"
    elif score >= 0.45: return "Medium"
    else: return "Low"

def explanation_agent(state):
    print("Executing Explanation Agent...")
    reports = []

    passed_candidates = [c for c in state["scores"] if c[1] >= 0.35]

    for rank, (resume, score) in enumerate(passed_candidates):
        fit_level = get_fit_label(score)
        
        # THE FIX: A highly structured, zero-fluff prompt that forces Name, Experience, and Justifications.
        prompt = f"""
        Candidate Resume: {resume}
        Overall Fit: {fit_level}

        Extract the candidate's exact Name and Years of Experience. 
        Then, provide a highly concise, professional evaluation. 
        DO NOT write paragraphs. Use brief, 1-line bullet points only.
        
        Structure EXACTLY like this:
        **Candidate Name:** [Name]
        **Experience:** [X] years
        
        **Strengths:**
        - [1 or 2 short bullets]
        - [1 short bullet]
        
        **Skill Gaps:**
        - [1 or 2 short bullets]
        
        **Fit Justification:** [1 or 2 short sentences explaining exactly why they are fit or unfit based on the JD]
        **Seniority Alignment:** [1  or 2 short sentence evaluating if their experience level realistically meets the role's seniority requirements]
        """
        response = llm.invoke(prompt)
        reports.append(f"### Rank {rank + 1} | Fit: {fit_level} (Score: {score:.2f})\n{response.content}\n")

    state["reports"] = reports
    return state