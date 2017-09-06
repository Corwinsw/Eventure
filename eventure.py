from flask import Flask
from flask import request
from flask import jsonify
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(autocommit = True, cursorclass = DictCursor)
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'corwin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kuftence'
app.config['MYSQL_DATABASE_DB'] = 'eventure'
app.config['MYSQL_DATABASE_HOST'] = '146.148.114.227'
mysql.init_app(app)


@app.route('/login', methods=['POST', 'GET'])
def login():

    conn = mysql.connect()
    cur = conn.cursor()

    params = request.get_json(force=True)
    
    fb_id = params["fbId"]
    name = params["name"]

    cur.execute("SELECT usersId FROM users WHERE fbId = %s", (fb_id))

    user_id = 0
    
    if cur.rowcount == 0:
        cur.execute("INSERT INTO users (fbId, name) VALUES (%s, %s)", (fb_id, name)) 
        user_id = cur.lastrowid
    else:
        for r in cur:
            user_id = r["usersId"]
        
    
    cur.execute("SELECT * FROM eventTypes")

    eventTypes = cur.fetchall()
    
    returnJson = {}
    returnJson["usersId"] = user_id
    returnJson["eventTypes"] = eventTypes

    return jsonify(returnJson)


@app.route('/createEvent',  methods=['POST'])
def create_event():
    # expects type, date, location, isGoing

    event = request.get_json()

    conn = mysql.connect()
    cur = conn.cursor()

    cur.execute("INSERT INTO `events` (`eventTypesId`, `date`, `location`) VALUES (%s, %s, %s)", (event["eventTypesId"], event["date"], event["location"]))
    event["eventsId"] = cur.lastrowid
    cur.execute("INSERT INTO `usersEvents` (`usersId`, `eventsId`, `isAnswered`) VALUES (%s, %s, %s)", (event["usersId"], event["eventsId"], event["isAnswered"]))


    return jsonify(event)


    
@app.route('/answerEvent', methods=['POST'])
def answer_event():
    conn = mysql.connect()
    cur = conn.cursor()

    event = request.get_json()

    cur.execute("INSERT INTO `usersEvents` (`usersId`, `eventsId`, `isAnswered`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE isAnswered = %s", (event["usersId"], event["eventsId"], event["isAnswered"], event["isAnswered"]))


    return jsonify(1)



@app.route('/getEvents', methods=['GET'])
def get_events():
    conn = mysql.connect()
    cur = conn.cursor()
   
    user_id = request.args.get('usersId')

    cur.execute("SELECT usersId, e.eventsId as eventsId, isAnswered, eventTypesId, date, location FROM usersEvents ue LEFT JOIN events e ON e.eventsId = ue.eventsId")

    events = cur.fetchall()

    for event in events:
        cur.execute("SELECT u.name, u.usersId, ue.isAnswered from usersEvents ue LEFT JOIN users u ON u.usersId = ue.usersId WHERE ue.eventsId = %s", (event["eventsId"]))

        event["guests"] = cur.fetchall()
    eventsObj = {}
    eventsObj["events"] = events

    return jsonify(eventsObj)

