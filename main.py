from langgraph.graph import StateGraph, END
from state import WorkflowState

from agents.retrieval_agent import retrieval_agent
from agents.scoring_agent import scoring_agent
from agents.supervisor_agent import supervisor_agent
from agents.comparison_agent import comparison_agent
from agents.explanation_agent import explanation_agent

from ingestion.resume_loader import load_resumes
from ingestion.job_parser import parse_job_description
from retrieval.vector_store import index_resumes
import os


def build_graph():
    """
    Constructs the LangGraph state machine, defining nodes (agents) 
    and the edges (routing logic) that connect them.
    """
    graph = StateGraph(WorkflowState)

    # 1. Add all agents as discrete nodes
    graph.add_node("retrieve", retrieval_agent)
    graph.add_node("score", scoring_agent)
    graph.add_node("supervisor", supervisor_agent)
    graph.add_node("compare", comparison_agent)
    graph.add_node("explain", explanation_agent)

    # 2. Define the linear start of the pipeline
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "score")
    graph.add_edge("score", "supervisor")

    # 3. Define the Supervisor's dynamic routing logic
    graph.add_conditional_edges(
        "supervisor",
        lambda s: s["route"],
        {
            "compare": "compare",
            "explain": "explain",
            "reject": END
        }
    )

    # 4. Connect the remaining nodes to the end
    graph.add_edge("compare", "explain")
    graph.add_edge("explain", END)

    return graph.compile()


def main():
    print("--- Loading Data & Initializing AI Recruiter ---")
    # Auto-create directories if they don't exist to prevent FileNotFoundError
    os.makedirs("data/resumes", exist_ok=True)
    
    # 1. Load Data
    resumes = load_resumes("data/resumes")
    job_clusters = parse_job_description("data/job_description.txt")
    
    print(f"Loaded {len(resumes)} resumes.")
    
    # 2. Index to ChromaDB (Upsert logic handles duplicates safely)
    index_resumes(resumes)

    # 3. Build the LangGraph Application
    app = build_graph()

    # 4. Initialize the State (Injecting the Metadata Requirement)
    initial_state = {
        "query": "GenAI engineer LangChain RAG vector database custom LLM",
        "min_experience": 2,  # Stage 1: Hard requirement for Metadata Filter
        "resumes": resumes,
        "job_clusters": job_clusters,
        "retrieved": [],
        "scores": [],
        "route": "",
        "comparison_prob": 0.0,
        "reports": []
    }

    print("--- Invoking Multi-Agent Graph ---")
    
    # Execute the graph
    final_state = app.invoke(initial_state)

    # 5. Output the Final Reports
    print("\n" + "=" * 50)
    print("FINAL MATCH REPORTS")
    print("=" * 50)
    
    reports = final_state.get("reports", [])
    if not reports:
        print("No candidates passed the required thresholds.")
    else:
        for report in reports:
            print(report)
            print("-" * 50)


if __name__ == "__main__":
    main()