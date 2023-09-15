import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from buildx.initialize import Initialize
from buildx.build import ImageBuild

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SOURCE_CODES_PATH'] = '/data/codes'


def allowed_sourcecode(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'rar', 'zip', 'tar.gz', 'tar'}


@app.route('/api/v1/buildx', methods=['POST'])
def process_code():
    if 'sourcecode' not in request.files:
        resp = jsonify({'message': 'No sourcecode part in the request'})
        resp.status_code = 400
        return resp
    sourcecode = request.files['sourcecode']
    if sourcecode.sourcecodename == '':
        resp = jsonify({'message': 'No sourcecode selected for uploading'})
        resp.status_code = 400
        return resp
    if sourcecode and allowed_sourcecode(sourcecode.sourcecodename):
        sourcecodename = secure_filename(sourcecode.sourcecodename)
        sourcecode.save(os.path.join(app.config['SOURCE_CODES_PATH'], sourcecodename))
        Initialize.extractSourceCode(sourcecodename.split('.')[0], app.config['SOURCE_CODES_PATH'])
        resp = jsonify({'message': 'sourcecode successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed sourcecode types are rar zip tar.gz tar'})
        resp.status_code = 400
        return resp


@app.route('api/v1/buildx', methods=['GET'])
def build_code():
    if request.args.get('source_code'):
        check_docker_file_exist = ImageBuild.checkDockerfileExist(
            app.config['SOURCE_CODES_PATH'],
            request.args.get('source_code')
        )
        if not check_docker_file_exist:
            ImageBuild.generateDockerfile(
                source_path=app.config['SOURCE_CODES_PATH'],
                source_code=request.args.get('source_code'),
                language=request.args.get('source_language')
            )
        ImageBuild.buildDockerfile(
            source_path=app.config['SOURCE_CODES_PATH'],
            source_code=request.args.get('source_code')
        )

    elif not request.args.get('source_code'):
        resp = jsonify({'message': 'No source code defined'})
        resp.status_code = 400
        return resp
    else:
        resp = jsonify({'message': 'Not Found'})
        resp.status_code = 404
        return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
