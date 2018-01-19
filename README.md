# SonarQube-Web-plugin

Node.js server that retrieve json data from SonarQube hosting on Duke University's server. Processing data in python using SonarQube web api.Then returns the filtered json data to node server.

To start the server, run "node server.js", then enter the "localhost:8000/" + <project name you have analzed on sonarqube> in browser. 

It returns a Json file with schema: https://github.com/wellxchen/SonarQube-Web-plugin/blob/master/server/example.json
