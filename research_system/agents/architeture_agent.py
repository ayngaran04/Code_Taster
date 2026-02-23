from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import HumanMessage
from research_system.core.state import ReviewState
from config import MODEL_NAME,MAX_TOKENS
from research_system.agents.security_agent import format_files_for_prompt, load_prompt, parse_llm_responses

def run_architecture_agent(state:ReviewState)-> ReviewState:
    llm  = ChatGoogleGenerativeAI(model=MODEL_NAME, max_tokens=MAX_TOKENS, temperature=0.5)
    prompt_template =  load_prompt("architecture")
    file_content = format_files_for_prompt(state)
    prompt = prompt_template.replace("{file_contents}", file_content)

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        findings, errors = parse_llm_responses(response.content, "architecture")
    except Exception as e:
        findings = []
        errors = [f"Architecture agent failed: {str(e)}"]

    return {
        "architecture_findings": findings,
        "errors": errors
    }
