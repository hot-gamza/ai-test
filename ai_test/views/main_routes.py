from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
import os
from ..utils.faceswap import faceswap
from ..utils.gfpgan_model import gfpgan_gogo

bp = Blueprint('main', __name__, url_prefix='/')

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        male_filenames = []
        female_filenames = []
        male_files = request.files.getlist('male_file')
        female_files = request.files.getlist('female_file')
        # 남자사진 처리
        for file in male_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                male_filenames.append(filepath)
        # 여자사진 처리
        for file in female_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                female_filenames.append(filepath)
        
        template_img = "template_image_path_here"
        result_filenames = faceswap(template_img, male_filenames, female_filenames)
        
        final_result_filenames = []
        for result_file_path in result_filenames:
            result_img = gfpgan_gogo(result_file_path)
            final_result_filename = f"final_results/{result_file_path.split('/')[-1]}"
            result_img.save(f"static/{final_result_filename}")  # PIL Image를 파일로 저장
            final_result_filenames.append(final_result_filename)
            
        return render_template('result.html', filenames=final_result_filenames) 

    return render_template('index.html')