import cv2
import insightface
import datetime
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis
from .gfpgan_model import gfpgan_gogo
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
inswapper_path = os.path.join(current_dir, '..', 'models', 'inswapper_128.onnx')
result_path = os.path.join(current_dir, '..', 'images', 'result', 'result.jpg')


app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model(inswapper_path, download=False, download_zip=False)


def faceswap(template_img, male_face_img, female_face_img):
    '''
        faceswap(템플릿 이미지, 남자, 여자)
    '''
    # 파일 경로 확인
    print(f"Reading template_img from: {template_img}")
    print(f"Reading male_face_img from: {male_face_img}")
    print(f"Reading female_face_img from: {female_face_img}")

    # 파일 존재 여부 확인
    if os.path.exists(template_img):
        print(f"{template_img} exists.")
    else:
        print(f"{template_img} does not exist.")

    if os.path.exists(male_face_img):
        print(f"{male_face_img} exists.")
    else:
        print(f"{male_face_img} does not exist.")

    if os.path.exists(female_face_img):
        print(f"{female_face_img} exists.")
    else:
        print(f"{female_face_img} does not exist.")


    # 커플 템플릿
    try:
        template_img = cv2.imread(template_img)
    except PermissionError:
        print(f"Permission error while reading {template_img}.")
        return None

    template_faces = app.get(template_img)
    print("detected number of faces: ", len(template_faces))
    dn = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fn = f'fs_{dn}.jpg'


    # 얼굴 이미지
    male_img_read = cv2.imread(male_face_img)
    male_copy_face = app.get(male_img_read)[0]

    female_img_read = cv2.imread(female_face_img)
    female_copy_face = app.get(female_img_read)[0]

    cnt = 0
    for find_face in template_faces:
        if cnt == 0:
            if find_face['gender'] == 0:
                result = swapper.get(template_img, find_face, female_copy_face, paste_back=True)
            else:
                result = swapper.get(template_img, find_face, male_copy_face, paste_back=True)
        else:
            if find_face['gender'] == 0:
                result = swapper.get(result, find_face, female_copy_face, paste_back=True)
            else:
                result = swapper.get(result, find_face, male_copy_face, paste_back=True)
        cnt+=1

    cv2.imwrite(result_path, result)
    gfp_result = np.array(gfpgan_gogo(result_path))
    gfp_result = cv2.cvtColor(gfp_result, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join('images', 'result', fn), gfp_result)
    print(f"saved a file successfully. {fn}")

    return os.path.join(current_dir, '..', 'images', 'result', fn)
