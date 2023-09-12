from gfpgan import GFPGANer
import torch
import numpy as np
from PIL import Image
import cv2

def gfpgan_gogo2(img):
    '''
        gfp 업스케일링 적용
        gfpgan_gogo(페이스 스왑한 이미지)
    '''
    # img = Image.open(img)
    img = Image.fromarray(img)
    original_img = img.copy()
    np_img = np.array(img)

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = GFPGANer(model_path=r'../models/GFPGANv1.4.pth', upscale=1, arch='clean', channel_multiplier=2, bg_upsampler=None, device=device)
    np_img_bgr = np_img[:, :, ::-1]
    _, _, gfpgan_output_bgr = model.enhance(np_img_bgr, has_aligned=False, only_center_face=False, paste_back=True)
    np_img = gfpgan_output_bgr[:, :, ::-1]

    restored_img = Image.fromarray(np_img)
    result_img = Image.blend(
        original_img, restored_img, 1
    )
    # result_img.show()
    return result_img    

if __name__ == '__main__':
    gfpgan_gogo2('ej2.jpg')