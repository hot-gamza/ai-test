import cv2
import insightface
import datetime
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis
from gfpgan_model import gfpgan_gogo

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model(
    r'../models/inswapper_128.onnx', download=False, download_zip=False)


def faceswap(template_img, face_img):
    '''
        faceswap(템플릿 이미지, 합성 얼굴 이미지)
    '''

    template_img = cv2.imread(template_img)
    template_faces = app.get(template_img)
    print("detected number of faces: ", len(template_faces))
    dn = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fn = f'fs_{dn}.jpg'
    face_img_read = cv2.imread(face_img)
    copy_face = app.get(face_img_read)[0]

    for find_face in template_faces:
        result = swapper.get(template_img, find_face, copy_face)

    gfp_result = np.array(gfpgan_gogo(result))
    cv2.imwrite(f'../images/result/{fn}', gfp_result)
    print(f"saved a file successfully. {fn}")

    return gfp_result


if __name__ == '__main__':
    faceswap(r'../images/st1.jpg',r'../images/karina.jpg')
