from fastapi import APIRouter, UploadFile, File
import cloudinary
import cloudinary.uploader
import os

router = APIRouter(
    prefix="/files",
    tags=["files"]
)

# Configure Cloudinary (uses env variables from Render)
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# Upload API
@router.post("/uploadfile")
async def upload_file(upload_file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(upload_file.file)

        return {
            "image_url": result["secure_url"]
        }

    except Exception as e:
        return {
            "error": str(e)
        }