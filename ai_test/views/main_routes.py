from flask import Blueprint, request, render_template
from ..utils.upload import handle_upload
from ..utils.faceswap import faceswap
import os
import stat
from io import BytesIO
from PIL import Image

bp = Blueprint('main', __name__, url_prefix='/')

final_results_dir = os.path.join("static", "final_results")
if not os.path.exists(final_results_dir):
    os.makedirs(final_results_dir)
    # 권한설정
    os.chmod(final_results_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

@bp.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        male_files = request.files.getlist('imgFile')[0]
        female_files = request.files.getlist('imgFile')[1]

        print(male_files, female_files)

        male_filenames = handle_upload(male_files)
        female_filenames = handle_upload(female_files)

        template_img = r"D:\project\ai-test\ai_test\images\template\temp.jpg"

        # 이미 faceswap 함수가 모든 처리를 해서 결과 파일을 저장하고, 그 경로를 반환
        result_filenames = faceswap(template_img, male_filenames, female_filenames)
        return result_filenames
