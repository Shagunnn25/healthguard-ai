from fastapi import APIRouter

router = APIRouter()

@router.post("/ocr")
def ocr():
    return {"message": "OCR module coming soon"}