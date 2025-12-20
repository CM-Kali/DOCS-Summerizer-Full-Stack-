from fastapi import APIRouter, UploadFile, File
from app.services.ai_service import summarize_text
from app.utils.file_reader import extract_text

router = APIRouter(prefix="/summarize", tags=["Summarization"])

@router.post("/")
async def summarize_document(file: UploadFile = File(...)):
    text = extract_text(file)
    summary = summarize_text(text)
    return {"summary": summary}
