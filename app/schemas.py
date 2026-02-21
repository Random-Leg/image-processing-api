from pydantic import BaseModel
from typing import Optional, List


class ImageMetadata(BaseModel):
    width: int
    height: int
    format: str
    size_bytes: int


class Thumbnails(BaseModel):
    small: str
    medium: str


class ImageData(BaseModel):
    image_id: str
    original_name: str
    processed_at: str
    metadata: ImageMetadata
    thumbnails: Thumbnails


class ImageResponse(BaseModel):
    status: str
    data: ImageData
    error: Optional[str] = None


from typing import List
ImageListResponse = List[ImageResponse]