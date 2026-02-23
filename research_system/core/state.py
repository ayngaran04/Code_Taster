from typing import TypedDict, List, Dict, Optional, Annotated
import operator

class Fileinfo(TypedDict):
    path:str
    content:str
    extension:str
    size_kb: str

class AgentFinding(TypedDict):
    agent : str
    severity : str
    category : str
    file : str
    line_hint :str
    description : str
    suggestion : str
class ReviewState(TypedDict):
    target_directory: str
    files : List[Fileinfo]

    security_findings : List[AgentFinding]
    architecture_findings : List[AgentFinding]
    code_quality_findings : List[AgentFinding]
    
    final_report : Optional[str]
    errors : Annotated[List[str], operator.add]
