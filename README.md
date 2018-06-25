# Java code static analysis tool

*Design Checklist* is a tool created for Duke's Compsci308 class in order to help students refactor their code. It analyzes Java projects and reports different code issues tailored to the material covered in the class. Specifically, these issues are broken into 5 main categories:

**Communication**: Is the code easy to read and understand?

**Modularity**: Do your classes have a small, well-defined purpose?

**Flexibility**: Is your program flexibile to change as development goes?

**Code Smells**: Code issues related to general good programming practices, such as: duplications

**Java Notes**: Code issues specific to Java

This repo is the backend server that retrieves analysis data as json from SonarQube and processes the data using python and shell. The server currently support 11 endpoints, including: 

```python

"/api/show" #get all issues 

"/api/statistics" #get statistics of the project

"/api/file/xml" #get required xml file to run pipeline on gitlab

"/api/file/yml" #get required yml file to run pipeline on gitlab

"/api/duplications" #get issues regarding duplications

"/api/lmethod" #get longest method in the project

"/api/commit" #get gitlab commit information about a project

"/api/commitstat" #get gitlab commit statistics about a project

"/api/directory" #get issues by directories

"/api/project" #check whether a project has been analyze

"/api/author" #get issues by author
```


To start the server, run ```FLASK_APP=__init__.py flask run```, then enter the ```localhost:5000/``` + ```<project name you have analzed on sonarqube>``` in browser. Frontend:https://github.com/zacharyfmarion/sonarqube-web-frontend
