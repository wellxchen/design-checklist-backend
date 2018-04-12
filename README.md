# Design-CheckUp-Web-Backend

Flask server that retrieves analysis data as json from SonarQube hosting on Duke University's server. Processing data in python using SonarQube web api.Then returns the filtered json data to be displayed in frontend. Frontend:https://github.com/zacharyfmarion/sonarqube-web-frontend

To start the server, run ```FLASK_APP=__init__.py flask run```, then enter the ```localhost:5000/``` + ```<project name you have analzed on sonarqube>``` in browser. 

