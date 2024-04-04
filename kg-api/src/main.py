from fastapi import FastAPI

app = FastAPI(
    title="course-kg API"
)


@app.get("/")
async def root():
    return {"message": "welcome to the knowledge graph API"}
