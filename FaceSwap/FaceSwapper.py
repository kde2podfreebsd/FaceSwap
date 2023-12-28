import os
import cv2
import insightface
from insightface.app import FaceAnalysis
from Telegram.Config import basedir


class NoFaceDetectedError(Exception):
    """Custom exception for no face detected."""

    def __str__(self):
        return "NoFaceDetectedError: FaceAnalysis.model_zoo not found face-mask on image"


class FaceSwapper(object):
    app: FaceAnalysis = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    onnx_path = os.path.join(basedir, 'FaceSwap', 'inswapper_128.onnx')
    swapper: insightface.model_zoo = insightface.model_zoo.get_model(onnx_path, download=True, download_zip=True)

    def __init__(self):
        """Initialize the FaceSwapper."""
        assert insightface.__version__ >= '0.7'

    def detect_faces(self, path_to_image: str):
        """Detect faces in the image.

        Args:
            path_to_image: A string representing the path to the image.

        Returns:
            List of faces detected in the image or raises NoFaceDetectedError.
        """
        img = cv2.imread(path_to_image)
        faces = self.app.get(img)
        faces = sorted(faces, key=lambda x: x.bbox[0])

        if len(faces) > 0:
            return faces
        else:
            raise NoFaceDetectedError("No faces detected in the image.")

    def face_swap(self, path_target_face_image: str, path_replace_face_image: str, user_id: str, output_path: str):
        """Swap faces in the images.

        Args:
            path_target_face_image: A string representing the path to the target face image.
            path_replace_face_image: A string representing the path to the image where faces will be replaced.
            user_id: A string representing the user ID.
            output_path: A string representing the output folder path.
        """
        try:
            img = cv2.imread(path_replace_face_image)
            result_image = img.copy()

            filename = os.path.basename(path_replace_face_image).split(".")[0]
            output_filename = f"{filename}_{user_id}.jpg"

            faces_to_replace = self.detect_faces(path_replace_face_image)
            target_face = self.detect_faces(path_target_face_image)

            for idx, face in enumerate(faces_to_replace):
                result_image = self.swapper.get(result_image, face, target_face[0], paste_back=True)

            cv2.imwrite(os.path.join(output_path, output_filename), result_image)

        except NoFaceDetectedError as e:
            raise NoFaceDetectedError(f"No faces detected on the image for user: {user_id}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_mempack(self, user_id: str, target_face_image_path: str):
        """Create a memory pack with swapped faces.

        Args:
            user_id: A string representing the user ID.
            target_face_image_path: A string representing the path to the target face image.
        """
        output_folder = os.path.join(basedir, 'FaceSwap', 'outputs', str(user_id))

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        else:
            file_list = [os.path.join(output_folder, f) for f in os.listdir(output_folder)]
            for f in file_list:
                os.remove(f)

        templates_folder = os.path.join(basedir, 'FaceSwap', 'templates')
        templates = os.listdir(templates_folder)

        for template in templates:
            template_path = os.path.join(templates_folder, template)
            print(template_path)
            try:
                self.face_swap(target_face_image_path, template_path, user_id, output_folder)
            except NoFaceDetectedError:
                raise NoFaceDetectedError(f"No faces detected on the image for user: {user_id}")

