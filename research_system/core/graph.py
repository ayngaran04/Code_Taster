from langgraph.graph import StateGraph, END
from research_system.core.state import ReviewState
from research_system.agents.security_agent import run_security_agent
from research_system.agents.architeture_agent import run_architecture_agent
from research_system.agents.code_quality_agent import run_code_quality_agent
from research_system.agents.outputText import run_synthesizer_agent

def build_graph() -> StateGraph:
    graph = StateGraph(ReviewState)


    graph.add_node("security", run_security_agent)
    graph.add_node("architecture", run_architecture_agent)
    graph.add_node("code_quality", run_code_quality_agent)
    graph.add_node("synthesizer", run_synthesizer_agent)

    graph.add_edge("security", "synthesizer") 
    graph.add_edge("architecture", "synthesizer")
    graph.add_edge("code_quality", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()