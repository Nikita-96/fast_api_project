from fastapi import UploadFile
import shutil

from src.service.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    def upload_image(self, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with open(f"src/static/images/{file.filename}", "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image.delay(image_path)
        # background_tasks.add_task(resize_image, image_path)
