from typing import TypedDict, List, Dict, Any

class WorkflowState(TypedDict):
    query: str
    min_experience: int # Added for Metadata Filtering
    resumes: List[Dict[str, Any]]
    job_clusters: Dict[str, List[str]]
    retrieved: List[Any]
    scores: List[Any]
    route: str
    comparison_prob: float
    reports: List[str]