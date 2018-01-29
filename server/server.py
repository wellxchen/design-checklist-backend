from ProcessSonar import ProcessSonar
from flask import Flask

app = Flask(__name__)

@app.route("/<string:project>")
def process(project):

    return ProcessSonar(project).percentage();


if __name__ == '__main__':
    app.run()



