from db import collection
from models import KnowledgeGraph

from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI(
    title="course-kg API"
)


@app.get("/")
async def root():
    return {"message": "welcome to the knowledge graph API"}


@app.get("/project")
async def get_project() -> List[str]:
    return collection.distinct("project_name")


@app.get("/kg")
async def get_kg(project_name: str) -> KnowledgeGraph:
    result = collection.find_one({"project_name": project_name})

    if not result:
        return HTTPException(status_code=404, detail="Project not found")

    return KnowledgeGraph.model_validate(result)
