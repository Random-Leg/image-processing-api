from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from datetime import datetime
import uuid
import os
from fastapi.responses import FileResponse
from .database import engine
from .models import Base, ImageRecord
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import ImageResponse, ImageListResponse


app = FastAPI()
Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

THUMBNAIL_DIR = "thumbnails"
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Image Processing API is running"}


@app.post(
    "/api/images",
    response_model=ImageResponse,
    summary="Upload an image",
    responses={
        200: {
            "description": "Image successfully processed",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "data": {
                            "image_id": "123e4567-e89b-12d3-a456-426614174000",
                            "original_name": "example.jpg",
                            "processed_at": "2026-02-21T18:58:33.308271",
                            "metadata": {
                                "width": 1920,
                                "height": 1080,
                                "format": "jpg",
                                "size_bytes": 204800
                            },
                            "thumbnails": {
                                "small": "http://127.0.0.1:8000/api/images/123/thumbnails/small",
                                "medium": "http://127.0.0.1:8000/api/images/123/thumbnails/medium"
                            }
                        },
                        "error": None
                    }
                }
            }
        }
    }
)
async def upload_image(file: UploadFile = File(...)):

    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only JPG and PNG are supported."
        )

    image_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{image_id}_{file.filename}")

    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract metadata
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            format = img.format.lower()
            if format in ['jpeg', 'mpo']:
                format = 'jpg'
            small_img = img.copy()
            small_img.thumbnail((128,128))
            small_path = os.path.join(THUMBNAIL_DIR, f"{image_id}_small.jpg")
            small_img.save(small_path)

            medium_img = img.copy()
            medium_img.thumbnail((512,512))
            medium_path = os.path.join(THUMBNAIL_DIR, f"{image_id}_medium.jpg")
            medium_img.save(medium_path)

        size_bytes = os.path.getsize(file_path)

    except Exception:
        raise HTTPException(status_code=400, detail="Corrupted image")
    
    db = SessionLocal()

    db_image = ImageRecord(
        id=image_id,
        original_name=file.filename,
        status="success",
        width=width,
        height=height,
        format=format,
        size_bytes=size_bytes,
        processed_at=datetime.utcnow().isoformat(),
        error=None
    )

    db.add(db_image)
    db.commit()
    db.close()

    return {
        "status": "success",
        "data": {
            "image_id": image_id,
            "original_name": file.filename,
            "processed_at": datetime.utcnow().isoformat(),
            "metadata": {
                "width": width,
                "height": height,
                "format": format,
                "size_bytes": size_bytes
            },
            "thumbnails": {
                "small": f"http://127.0.0.1:8000/api/images/{image_id}/thumbnails/small",
                "medium": f"http://127.0.0.1:8000/api/images/{image_id}/thumbnails/medium"
            }
        },
        "error": None
    }

@app.get("/api/images/{image_id}/thumbnails/{size}")
def get_thumbnail(image_id: str, size: str):

    if size not in ["small", "medium"]:
        raise HTTPException(status_code=400, detail="Invalid thumbnail size")

    file_path = os.path.join(THUMBNAIL_DIR, f"{image_id}_{size}.jpg")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Thumbnail not found")

    return FileResponse(file_path)


@app.get(
    "/api/images",
    response_model=ImageListResponse,
    summary="List all processed images"
)
def list_images():

    db = SessionLocal()
    images = db.query(ImageRecord).all()
    db.close()

    result = []

    for img in images:
        result.append({
            "status": img.status,
            "data": {
                "image_id": img.id,
                "original_name": img.original_name,
                "processed_at": img.processed_at,
                "metadata": {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "size_bytes": img.size_bytes
                },
                "thumbnails": {
                    "small": f"http://127.0.0.1:8000/api/images/{img.id}/thumbnails/small",
                    "medium": f"http://127.0.0.1:8000/api/images/{img.id}/thumbnails/medium"
                }
            },
            "error": img.error
        })

    return result