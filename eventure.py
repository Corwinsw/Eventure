from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
    return request.form["fb_id"]
    

@app.route('/createEvent',  methods=['POST', 'GET'])
def create_event():
    event = {}
    event["type"] = request.form["type"] 
    event["date"] = request.form["date"] 
    event["location"] = request.form["location"] 
    event["isGoing"] = request.form["isGoing"] 
    return jsonify(event)
    
@app.route('/answerEvent', methods=['POST', 'GET'])
def answer_event():
    event = {}
    event["eventId"] = request.form["eventId"]
    event["isGoing"] = request.form["isGoing"]
    return jsonify(event)
