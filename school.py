from flask import Flask,render_template,request,flash,redirect,url_for
import os
import json
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    # return 'Hello World!'
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    data = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_dir = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_dir)
            data = analysis_json(file_dir)
    print("------okok----okok")
    return render_template('index.html',data)

def analysis_json(file_dir):
    location = []
    if file_dir.split('.')[-1] != 'json':
        return location
    with open(file_dir, encoding='utf-8') as f:
        content = json.loads(f.read())
        for key in content.keys():
            location.extend(content[key])
    return location


if __name__ == '__main__':
    app.run()
