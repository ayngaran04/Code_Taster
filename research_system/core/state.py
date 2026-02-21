from typing import TypedDict, List, Dict , Optional

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

    secirity_findings : List[AgentFinding]
    architectural_findings : List[AgentFinding]
    code_quality_findings : List[AgentFinding]
    
    final_report : Optional[str]
    errors : List[str]
