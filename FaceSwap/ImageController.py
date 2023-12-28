import os
from FaceSwap.ImagePreparing import ImageResizer
from Telegram.Config import basedir


class ImageController:
    @staticmethod
    def saveImage(user_id, downloaded_file):
        users_images_dir = os.path.join(basedir, 'FaceSwap', 'users_images')
        user_photo_path = os.path.join(users_images_dir, f"{user_id}.jpg")

        if os.path.exists(user_photo_path):
            os.remove(user_photo_path)

        with open(user_photo_path, 'wb') as file:
            file.write(downloaded_file)

    @staticmethod
    def get_output_paths(user_id) -> list[os.path]:
        outputs_dir = os.path.join(basedir, 'FaceSwap', 'outputs', str(user_id))
        if not os.path.exists(outputs_dir):
            return []

        output_files = []
        for filename in os.listdir(outputs_dir):
            file_path = os.path.join(outputs_dir, filename)
            if os.path.isfile(file_path):
                output_files.append(file_path)

        return output_files

    @staticmethod
    def get_target_path(user_id) -> str:
        users_images_dir = os.path.join(basedir, 'FaceSwap', 'users_images')
        user_photo_path = os.path.join(users_images_dir, f"{user_id}.jpg")
        if os.path.exists(user_photo_path):
            return user_photo_path

        user_photo_path = os.path.join(users_images_dir, f"{user_id}.png")
        if os.path.exists(user_photo_path):
            return user_photo_path

        user_photo_path = os.path.join(users_images_dir, f"{user_id}.webp")
        if os.path.exists(user_photo_path):
            return user_photo_path

        return None
