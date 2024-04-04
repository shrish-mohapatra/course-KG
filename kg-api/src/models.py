from pydantic import BaseModel, Field
from typing import List


class Node(BaseModel):
    id: str = Field(description="Name of node")
    sources: List[str] = Field(description="List of files node appears in")


class Edge(BaseModel):
    source: str = Field(description="Starting Node ID")
    target: str = Field(description="Destination Node ID")


class KnowledgeGraph(BaseModel):
    project_name: str = Field(description="Name of project KG was created for")
    nodes: List[Node]
    edges: List[Edge]
