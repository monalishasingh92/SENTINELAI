import hashlib
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.rag.document_processor import process_document

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are supported."
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    temp_path = UPLOAD_DIR / f"temp_{uuid4().hex}{extension}"
    saved_path = None
    created_new_file = False

    try:
        file_hash = hashlib.sha256()
        total_size = 0

        with temp_path.open("wb") as buffer:

            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="File size exceeds the 10 MB limit."
                    )

                file_hash.update(chunk)
                buffer.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # Generate a content-based filename
        content_hash = file_hash.hexdigest()
        saved_path = UPLOAD_DIR / f"{content_hash}{extension}"

        # Reuse an existing identical document
        if saved_path.exists():
            temp_path.unlink()
        else:
            temp_path.replace(saved_path)
            created_new_file = True

        # Process and store document
        result = process_document(str(saved_path))

        return {
            "message": "Document uploaded and processed successfully.",
            "duplicate": not created_new_file,
            **result
        }

    except HTTPException:
        raise

    except Exception as error:

        if created_new_file and saved_path and saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}"
        )

    finally:
        if temp_path.exists():
            temp_path.unlink()

        await file.close()
