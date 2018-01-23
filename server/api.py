'''
Flask API for the frontend
'''

from flask import Flask, request, jsonify
from adapter import Adapter
app = Flask(__name__)

@app.route('/overview', methods=['POST'])
def overview():
  ''' Returns an overview of the project '''
  project = request.form['project']
  adapter = Adapter(project) 
  return jsonify({
    "data": adapter.percentage()
  })