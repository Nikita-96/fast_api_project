from fastapi import APIRouter, UploadFile  # , BackgroundTasks

from src.service.images import ImageService


router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
def upload_image(file: UploadFile):
    ImageService().upload_image(file=file)
