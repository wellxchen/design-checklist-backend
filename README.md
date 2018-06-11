# Java code static analysis tool

*Design Checklist* is a tool created for Duke's Compsci308 class in order to help students refactor their code. It analyzes Java projects and reports different code issues tailored to the material covered in the class. Specifically, these issues are broken into 5 main categories:

**Communication**: Is the code easy to read and understand?

**Modularity**: Do your classes have a small, well-defined purpose?

**Flexibility**: Is your program flexibile to change as development goes?

**Code Smells**: Code issues related to general good programming practices, such as: duplications

**Java Notes**: Code issues specific to Java

This repo is the backend server that retrieves analysis data as json from SonarQube hosting on Duke University's server. Processing data in python and shell.Then returns the filtered json data to be displayed in frontend. Rule ids and categories are temporarily hardcoded on backend to boost performance. Ultimately, SQL database will be used to store the hardcoded things for better code design.

To start the server, run ```FLASK_APP=__init__.py flask run```, then enter the ```localhost:5000/``` + ```<project name you have analzed on sonarqube>``` in browser. Frontend:https://github.com/zacharyfmarion/sonarqube-web-frontend
