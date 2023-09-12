from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__, url_prefix='/')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     filenames = []
    #     files = request.files.getlist('file')
    #     print(files)
    #     for file in files:
    #         if file and allowed_file(file.filename):
    #             filename = secure_filename(file.filename)
    #             filepath = os.path.join(UPLOAD_FOLDER, filename)
    #             file.save(filepath)
    #             filenames.append(filename)
                
                #TODO logic은 여기에 추가하시오.
        print('asdads')

        # return render_template('result.html', filenames=filenames) 
    # return render_template('index.html')



