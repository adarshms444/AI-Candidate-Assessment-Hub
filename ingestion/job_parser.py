import json
from components.llm import get_llm

def parse_job_description(path):
    # 1. Read the raw, unstructured text
    with open(path, "r", encoding="utf-8") as f:
        job_text = f.read()

    # 2. Prompt the LLM to act as the parser
    prompt = f"""
    You are an expert AI technical recruiter. Analyze the following Job Description.
    Extract the skills and group them strictly into these four categories:
    
    1. "must_have": Explicitly required or mandatory skills.
    2. "important": Highly desired or core responsibilities.
    3. "nice_to_have": Bonus, optional, or "plus" skills.
    4. "implicit": Foundational skills NOT explicitly written in the text, but absolutely necessary to execute the 'must_have' skills.
    
    Job Description:
    {job_text}
    
    Respond ONLY with a valid JSON object. Do not include markdown blocks like ```json.
    Format exactly like this:
    {{
        "must_have": ["skill1", "skill2"],
        "important": ["skill3"],
        "nice_to_have": [],
        "implicit": ["skill4", "skill5"]
    }}
    """
    
    llm = get_llm()
    
    print("Agent: Parsing Job Description and inferring implicit skills...")
    try:
        response = llm.invoke(prompt).content
        
        # Clean the output in case the LLM disobeys and adds markdown
        cleaned_response = response.replace("```json", "").replace("```", "").strip()
        
        # Convert the string to a Python dictionary
        clusters = json.loads(cleaned_response)
        
        # Ensure all keys exist even if the LLM misses one
        for key in ["must_have", "important", "nice_to_have", "implicit"]:
            if key not in clusters:
                clusters[key] = []
                
        return clusters

    except Exception as e:
        print(f"Error parsing JD: {e}. Falling back to empty clusters.")
        return {
            "must_have": [],
            "important": [],
            "nice_to_have": [],
            "implicit": []
        }