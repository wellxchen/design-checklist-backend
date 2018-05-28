# Design-CheckUp-Web-Backend

Flask server that retrieves analysis data as json from SonarQube hosting on Duke University's server. Processing data in python using SonarQube web api.Then returns the filtered json data to be displayed in frontend. Rule ids and categories are temporarily hardcoded on backend to boost performance. Ultimately, SQL database will be used to store the hardcoded things for better code design.

To start the server, run ```FLASK_APP=__init__.py flask run```, then enter the ```localhost:5000/``` + ```<project name you have analzed on sonarqube>``` in browser. Frontend:https://github.com/zacharyfmarion/sonarqube-web-frontend

Currently hosting on duke's Apache server: http://compsci308.colab.duke.edu

