# SonarQube-Web-plugin

Node.js server that retrieve json data from SonarQube hosting on Duke University's server. Processing data in python using SonarQube web api.

To start the server, run "node server.js", then enter the "localhost:8000/" + project name you have analzed on sonarqube. 

It returns a Json file with schema:

{
    "percentage": {
        "A": "double",
        "B": "double",
        "C": "double"
    },
    "error": {
        "A": {
            "path" : "string",
            "rule" : "string",
            "message" : "string",
            "textRange" : {
                "startLine" : "int",
                "endLine" : "int",
                "startOffset" : "int",
                "endOffset" : "int"
            }
        },
        "B": {
            "path" : "string",
            "rule" : "string",
            "message" : "string",
            "textRange" : {
                "startLine" : "int",
                "endLine" : "int",
                "startOffset" : "int",
                "endOffset" : "int"
            }
        },
        "C": {
            "path" : "string",
            "rule" : "string",
            "message" : "string",
            "textRange" : {
                "startLine" : "int",
                "endLine" : "int",
                "startOffset" : "int",
                "endOffset" : "int"
            }
        }
    }
}
