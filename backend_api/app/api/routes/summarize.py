from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from app.services.ai_service import summarize_text
from app.utils.file_reader import extract_text

router = APIRouter(prefix="/summarize", tags=["Summarization"])

@router.post("/")
async def summarize_document(
    file: UploadFile = File(...),
    length: str = Query("medium", enum=["short", "medium", "long"])
):
    try:
        text = extract_text(file)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Document has no readable text")

        summary = summarize_text(text, length)
        return {
            "status": "success",
            "length": length,
            "word_count": len(summary.split()),
            "summary": summary
        }

    except Exception as e:
        print("ERROR:", str(e))  # <-- YOU WILL SEE REAL ERROR
        raise HTTPException(status_code=500, detail="Summarization failed")



