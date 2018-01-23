# SonarQube-Web-plugin

Python server that retrieves analysis data as json from SonarQube hosting on Duke University's server. Processing data in python using SonarQube web api. You can install dependencies using `pip install -r requirements.txt` and run the server with `FLASK_APP=api.py flask run`. The server will be running on `http://localhost:5000`.

## API

# `/overview`

Returns a Json response with schema:

```json
{
  "percentage": {
    "A": "double",
    "B": "double",
    "C": "double"
  },
  "error": {
    "A": {
      "path": "string",
      "rule": "string",
      "message": "string",
      "textRange": {
        "startLine": "int",
        "endLine": "int",
        "startOffset": "int",
        "endOffset": "int"
      }
    },
    "B": {
      "path": "string",
      "rule": "string",
      "message": "string",
      "textRange": {
        "startLine": "int",
        "endLine": "int",
        "startOffset": "int",
        "endOffset": "int"
      }
    },
    "C": {
      "path": "string",
      "rule": "string",
      "message": "string",
      "textRange": {
        "startLine": "int",
        "endLine": "int",
        "startOffset": "int",
        "endOffset": "int"
      }
    }
  }
}
```
