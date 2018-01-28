from ProcessSonar import ProcessSonar
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route("/<string:project>")
def process(project):
    print project
    return ProcessSonar(project).percentage();


if __name__ == '__main__':
    app.run()



