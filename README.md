# SonarQube-Plugin-Backend

Flask server that retrieves analysis data as json from SonarQube hosting on Duke University's server. Processing data in python using SonarQube web api.Then returns the filtered json data to be displayed in frontend.

To start the server, run ```FLASK_APP=server.py flask run```, then enter the ```localhost:5000/``` + ```<project name you have analzed on sonarqube>``` in browser. 

It returns a Json file with schema: 
```json
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
```
