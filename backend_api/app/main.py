from fastapi import FastAPI
from app.api.routes.summarize import router as summarize_router

app = FastAPI(
    title="AI Document Summarizer",
    description="Backend API for document summarization",
    version="1.0.0"
)

app.include_router(summarize_router)

@app.get("/")
def root():
    return {"message": "AI Document Summarizer API is running"}
