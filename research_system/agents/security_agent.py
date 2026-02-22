import json
from langchain_google_genai import GoogleGenerativeAI
from langchain.messages import HumanMessage, SystemMessage
from research_system.core.state import ReviewState, AgentFinding
from config import MODEL_NAME,MAX_TOKENS
from typing import List

def load_prompt(name:str)-> str:
    with open(f'prompts/{name}.text','r') as f:
        return f.read()

def format_files_for_prompt(state:ReviewState)-> str:
    parts = []
    for file in state['files']:
        parts.append(f"File: {file['path']} \n {file['content']}\n")
    return "\n".join(parts)

def parse_llm_responses(response_text:str, agent_name:str)->tuple[List[AgentFinding], List[str]]:
    errors=[]
    cleaned = response_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()

    try:
        raw_findings = json.loads(cleaned)
        findings = []
        for f in raw_findings:
            findings.append(AgentFinding(
                agent=agent_name,
                severity=f.get("severity", "info"),
                category=f.get("category", "Unknown"),
                file=f.get("file", "unknown"),
                line_hint=f.get("line_hint", ""),
                description=f.get("description", ""),
                suggestion=f.get("suggestion", "")
            ))
        return findings, errors
    except json.JSONDecodeError as e:
        errors.append(f"{agent_name}: Failed to parse response — {str(e)}")
        return [], errors

def run_security_agent(state:ReviewState)-> ReviewState:
    llm = GoogleGenerativeAI(model=MODEL_NAME, max_tokens=MAX_TOKENS, temperature=0.5)
    prompt_template =  load_prompt("security")
    file_content = format_files_for_prompt(state)
    prompt = prompt_template.replace("{file_content}", file_content)

    messages = [HumanMessage(content=prompt)]
    try:
        response = llm.invoke(messages)
        findings, errors = parse_llm_responses(response.content, "security")
    except Exception as e:
        findings = []
        errors = [f"Security agent failed: {str(e)}"]

    return {
        **state,  # Preserve all existing state
        "security_findings": findings,
        "errors": state["errors"] + errors
    }
