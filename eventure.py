from flask import Flask
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'corwin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kuftence'
app.config['MYSQL_DATABASE_DB'] = 'eventure'
app.config['MYSQL_DATABASE_HOST'] = '146.148.114.227'
mysql.init_app(app)


@app.route('/login', methods=['POST', 'GET'])
def login():
    cur = mysql.get_db().cursor()
    cur.execute('''SELECT name FROM users WHERE fbId = "asdasda"''')
    rv = cur.fetchall()
    return str(rv)

    

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
