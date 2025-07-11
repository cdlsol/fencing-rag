from fastapi import FastAPI
from api.routes import user_prompt

app = FastAPI()

app.include_router(user_prompt.router)

@app.get("/health")
def read_root():
    return {"message": "Fencing RAG API running all good :)"}