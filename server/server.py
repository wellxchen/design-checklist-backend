from ProcessSonar import ProcessSonar
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import send_from_directory

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route("/api/show")
def process():

    project = request.args.get('project')
    print project
    return ProcessSonar(project).process();

@app.route("/api/statistics") #not finished
def statistics():
    project = request.args.get('project')
    return ProcessSonar(project).statistics();

@app.route("/api/rules") #not finished
def getrules():
    main = request.args.get('main')
    sub = request.args.get('sub')
    project = request.args.get('project')
    return ProcessSonar(project).getrules(main, sub);

@app.route("/api/file/xml")
def uploadxml():
    return send_from_directory(app.config['UPLOAD_FOLDER'], "xml.txt")

@app.route("/api/file/yml")
def uploadyml ():
    return send_from_directory(app.config['UPLOAD_FOLDER'], "yml.txt")

if __name__ == '__main__':
    app.run(threaded=True)



