import os
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,BooleanField,SelectField
from flask_bootstrap import Bootstrap
import subprocess
from flask import request
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

DATA = {}
output_log = ""

class singleFileForm(FlaskForm):
    slurm_parameters = TextAreaField('slurm_parameters')
    save_combinations = BooleanField('save_combinations')
    compiler = SelectField('compiler', choices=[('icc', 'ICC'), ('gcc','GCC')])
    compiler_version = StringField('compiler_version')
    compiler_flags = TextAreaField('compiler_flags')



@app.route("/")
@app.route("/singlefile", methods=['GET', 'POST'])
def single_file():
    form = singleFileForm(request.form)

    if request.method == "POST" and form.validate():
        return 'Hello brother'
    return render_template('single-file-mode.html', form=form)

@app.route("/multiplefiles")
def multiple_files():
    return render_template('multiple-files-mode.html')

@app.route("/makefile")
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