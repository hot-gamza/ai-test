import cv2
import insightface
import datetime
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis
from gfpgan_model import gfpgan_gogo
from gfpgan_model2 import gfpgan_gogo2

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model(
    r'../models/inswapper_128.onnx', download=False, download_zip=False)


def faceswap(template_img, male_face_img, female_face_img):
    '''
        faceswap(템플릿 이미지, 합성 얼굴 이미지)
    '''

    # 커플 템플릿
    template_img = cv2.imread(template_img)
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

    cv2.imwrite(f'../images/result/result.jpg', result)
    gfp_result = np.array(gfpgan_gogo(f'../images/result/result.jpg'))
    gfp_result = cv2.cvtColor(gfp_result, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'../images/result/{fn}', gfp_result)
    print(f"saved a file successfully. {fn}")

    # gfp_result2 = np.array(gfpgan_gogo2(result))
    # cv2.imwrite(f'../images/result/2-{fn}', gfp_result2)

    return gfp_result

if __name__ == '__main__':
    faceswap(r'../images/couple.jpg',r'../images/lake.jpg',r'../images/karina.jpg')
