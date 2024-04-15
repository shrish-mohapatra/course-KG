from pydantic import BaseModel, Field
from typing import List, Optional


class Node(BaseModel):
    id: str = Field(description="Name of node")
    notes: Optional[str] = None
    sources: List[str] = Field(description="List of files node appears in")


class Edge(BaseModel):
    source: str = Field(description="Starting Node ID")
    target: str = Field(description="Destination Node ID")
    relationship: str = Field(description="Relationship between nodes")


class KnowledgeGraph(BaseModel):
    project_name: str = Field(description="Name of project KG was created for")
    contributors: dict = Field(description="Contributors involved in KG generation")
    nodes: List[Node]
    edges: List[Edge]
