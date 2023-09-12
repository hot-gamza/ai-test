import cv2
import insightface
import datetime
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model(
    r'models\inswapper_128.onnx', download=False, download_zip=False)


def faceswap(face_img):
    '''
        faceswap(합성 얼굴 이미지)
    '''

    img_arr = [
        r'images\st1.jpg'
    ]

    for source_img in img_arr:
        source_img = cv2.imread(source_img)
        faces = app.get(source_img)
        print("detected number of faces: ", len(faces))
        dn = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fn = f'fs_{dn}.jpg'
        face_img_read = cv2.imread(face_img)
        copy_face = app.get(face_img_read)[0]

        for find_face in faces:
            result = swapper.get(source_img, find_face, copy_face)

        cv2.imwrite(f'images/{fn}', result)
        print(f"saved a file successfully. {fn}")

    return None


if __name__ == '__main__':
    faceswap(r'images\3-1000x1500.jpg')
