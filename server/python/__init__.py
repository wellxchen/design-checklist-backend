'''
Server that handles incoming requests and responds with json

:Author:
    Chengkang Xu <cx33@duke.edu>
'''

import json
from ProcessSonar import ProcessSonar
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import send_from_directory



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
CORS(app, resources={r"/api/*": {"origins": "*"}})



@app.route("/api/show")
def process():
    '''
    gets all the issues
    :return: issues
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).process(False, False)

@app.route("/api/statistics")
def statistics():
    '''
    gets statistics
    :return: statistics of projects
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).statistics()


@app.route("/api/file/xml")
def uploadxml():
    '''
    return xml file required to run the project
    :return: xml file
    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'], "xml.txt")

@app.route("/api/file/yml")
def uploadyml ():
    '''
    return yml file required to run the project
    :return: yml file
    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'], "yml.txt")

@app.route("/api/duplications")
def duplications():
    '''
    return duplications
    :return: issues related to duplications
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).process(True, False)

@app.route("/api/lmethod")
def lmethod():
    '''
    return longest methods information
    :return: longest methods
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    res = {}
    res['method'] = []
    res['method'].extend(ProcessSonar(group, project).longestmethods())
    return json.dumps(res)

@app.route("/api/commit")
def getcommit ():
    '''
    return commit info about the project
    :return: commit information
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).getcommit(False)

@app.route("/api/commitstat")
def getcommitstat ():
    '''
    return commit statisctics about the project
    :return: commit statisctics
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).getcommit(True)

@app.route("/api/directory")
def getbydirectory ():
    '''
    return all issues corresponding to directories
    :return: directories and issues in them
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).getbydirectory()

@app.route("/api/project")
def getproject ():
    '''
    if history parameter is set, it will check the history of the project
    if not set, it will check whether a project existed
    :return: whether a project existed or the history
    '''
    project = request.args.get('project')
    group = request.args.get('group')
    history = request.args.get('history')
    if history is None:
        return ProcessSonar(group, project).getproject()
    return ProcessSonar(group, project).gethistory()


@app.route("/api/author")
def getbyauthor():
    """
    return all issues corresponding to authors
    :return: authors and issues they have
    """
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).process(False,True)


@app.route("/api/codemaat")
def getcodemaat():
    """
    return the data gathered from code maat
    :return: data gathered from code maat
    """
    project = request.args.get('project')
    group = request.args.get('group')
    return ProcessSonar(group, project).getcodemaat()


if __name__ == '__main__':
    app.run(threaded=True)



