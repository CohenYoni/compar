import os
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,BooleanField,SelectField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
import subprocess
from flask import request
from flask import Flask, render_template
from flask_wtf.file import FileField, FileAllowed, FileRequired



app = Flask(__name__)
app.config.from_object(__name__)
WTF_CSRF_ENABLED = False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

DATA = {}
SOURCE_FILE_DIRECTORY = ''


output_log = ""

class singleFileForm(FlaskForm):
    slurm_parameters = TextAreaField('slurm_parameters', validators=[InputRequired()])
    save_combinations = BooleanField('save_combinations')
    compiler = SelectField('compiler', choices=[('icc', 'ICC'), ('gcc', 'GCC')])
    compiler_version = StringField('compiler_version')
    compiler_flags = TextAreaField('compiler_flags')
    source_file_area = TextAreaField('source_file_area')
    upload_file = FileField('upload_file', validators=[FileAllowed(['c'], 'c file only!')])#valiation dont work




def save_source_file(file_path, txt):
    # This function replace the save file option because Changes that can be in the code
    with open(file_path, "w") as f:
        f.write(txt)




@app.route("/")
@app.route("/singlefile", methods=['GET', 'POST'])
def single_file():
    source_file = ''
    form = singleFileForm()
    if request.method == "POST":
        if request.form.get('start_button'):
            #TODO - Open Compar object
            DATA['slurm_parameters'] = form.slurm_parameters.data
            DATA['save_combinations'] = form.save_combinations.data
            DATA['compiler'] = form.compiler.data
            DATA['compiler_version'] = form.compiler_version.data
            DATA['compiler_flags'] = form.compiler_flags.data
            DATA['source_file_text'] = form.source_file_area.data

            if form.source_file_area.data:
                file = form.upload_file.data
                if file:
                    DATA['source_file_name'] = file.filename
                    DATA['source_file_path'] = os.path.join(SOURCE_FILE_DIRECTORY, file.filename)
                else:
                    DATA['source_file_name'] = 'source_file.c'
                    DATA['source_file_path'] = os.path.join(SOURCE_FILE_DIRECTORY, 'source_file.c')
                save_source_file(file_path=DATA['source_file_path'], txt=form.source_file_area.data)

    print(form.slurm_parameters.errors)
    return render_template('single-file-mode.html', form=form)


@app.route('/upload_file')
def upload_file():
    return render_template('multiple-files-mode.html')

@app.route('/multiplefiles')
def multiple_files():
    return render_template('multiple-files-mode.html')

@app.route('/makefile')
def makefile():
    return render_template('makefile-mode.html')


@app.route('/stream_progress')
def stream():
    def generate():
        global output_log
        compar_file = "testt.py"
        proc = subprocess.Popen([f'python3 -u {compar_file}'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            output_log += str(line) + "\n"
            yield line.rstrip() + b'\n'
    return app.response_class(generate(), mimetype='text/plain')


if __name__ == "__main__":
    app.debug = True
    app.run()