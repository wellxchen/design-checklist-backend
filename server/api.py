'''
Flask API for the frontend
'''

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests

# Local imports
from adapter import Adapter

# Load the env variables from .env
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/overview', methods=['POST'])
def overview():
  ''' Returns an overview of the project '''
  project = request.form['project']
  adapter = Adapter(project) 
  return jsonify({
    "data": adapter.percentage()
  })

@app.route('/auth', methods=['POST'])
def route():
  ''' Use user code to get an auth token from the gitlab API '''
  params = {
    "client_id": os.environ.get("CLIENT_ID"),
    "client_secret": os.environ.get("CLIENT_SECRET"),
    "code": request.form["code"],
    "grant_type": "authorization_code",
    "redirect_uri": "http://localhost:3000/login",
  }
  response = requests.post('https://coursework.cs.duke.edu/oauth/token', data=params)
  return jsonify({
    "data": response.json() 
  })