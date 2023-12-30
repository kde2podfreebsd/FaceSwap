import os
from PIL import Image


class ImageResizer(object):
    def prepare_images(self, folder_path):
        new_folder_path = os.path.join(folder_path, 'prepared_images')
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        image_files = [f for f in os.listdir(folder_path) if
                       os.path.isfile(os.path.join(folder_path, f))]

        for image_file in image_files:
            try:
                img = Image.open(os.path.join(folder_path, image_file))
                img.verify()
                img.close()
            except (IOError, SyntaxError):
                print(f"File {image_file} is not a valid image. Skipping.")
                continue

            try:
                img = Image.open(os.path.join(folder_path, image_file))
                img = img.convert("RGBA")

                if img.size != (512, 512):
                    img = img.resize((512, 512))

                if image_file.lower().endswith('.jpg'):
                    new_file_name = os.path.splitext(image_file)[0] + '.png'
                else:
                    new_file_name = image_file

                img.save(os.path.join(new_folder_path, new_file_name), 'PNG', quality=100)

                file_size = os.path.getsize(os.path.join(new_folder_path, new_file_name)) / 1024
                if file_size > 350:
                    print(f"File {image_file} exceeds size limit. Skipping.")
                    os.remove(os.path.join(new_folder_path, new_file_name))
                    continue

                print(f"Image {image_file} processed and saved as {new_file_name}")

            except Exception as e:
                print(f"Error processing image {image_file}: {e}")
                continue

