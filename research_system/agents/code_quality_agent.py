from research_system.core.state import ReviewState, AgentFinding
from config import MODEL_NAME,MAX_TOKENS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage
from research_system.agents.security_agent import format_files_for_prompt, load_prompt, parse_llm_responses

def run_code_quality_agent(state:ReviewState)-> ReviewState:
    llm  = ChatGoogleGenerativeAI(model=MODEL_NAME, max_tokens=MAX_TOKENS, temperature=0.5)
    prompt_template =  load_prompt("code_quality")
    file_content = format_files_for_prompt(state)
    prompt = prompt_template.replace("{file_contents}", file_content)

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        findings, errors = parse_llm_responses(response.content, "code_quality")
    except Exception as e:
        findings = []
        errors = [f"Code Quality agent failed: {str(e)}"]

    return {
        "code_quality_findings": findings,
        "errors": errors
    }

