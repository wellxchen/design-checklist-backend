from ProcessSonar import ProcessSonar
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import send_from_directory
import json


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/api/show")
def process():
    project = request.args.get('project')
    return ProcessSonar(project).process(False)

@app.route("/api/statistics")
def statistics():
    project = request.args.get('project')
    return ProcessSonar(project).statistics()

@app.route("/api/rules") #not finished
def getrules():
    main = request.args.get('main')
    sub = request.args.get('sub')
    project = request.args.get('project')
    return ProcessSonar(project).getrules(main, sub)

@app.route("/api/file/xml")
def uploadxml():
    return send_from_directory(app.config['UPLOAD_FOLDER'], "xml.txt")

@app.route("/api/file/yml")
def uploadyml ():
    return send_from_directory(app.config['UPLOAD_FOLDER'], "yml.txt")

@app.route("/api/duplications")
def duplications():
    project = request.args.get('project')
    return ProcessSonar(project).process(True)

@app.route("/api/lmethod")
def lmethod():
    project = request.args.get('project')
    res = {}
    res['method'] = []
    res['method'].extend(ProcessSonar(project).longestmethods())
    return json.dumps(res)

@app.route("/api/commitsonar")
def getcommitsonar ():
    project = request.args.get('project')
    return ProcessSonar(project).getcommitsonar()

@app.route("/api/commit")
def getcommit ():
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(project).getcommit(group, project)

@app.route("/api/commit")
def getalldirectory ():
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(project).getalldirectory(group, project)

if __name__ == '__main__':
    app.run(threaded=True)



