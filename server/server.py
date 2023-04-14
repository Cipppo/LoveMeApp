from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import json



def start_mysql_connection():
    try:
        connection = mysql.connector.connect(host="localhost", 
                                            database="lovify",
                                            user="root",
                                            password="root")
        if(connection.is_connected()):
            print("LOG ====> Connected to MYSQL Server!")
        return connection
    except Error as e:
        print("Error occured while connecting")
        print(e)

db = start_mysql_connection()



app = Flask(__name__)
CORS(app)

id = 1

def getMessageById():
    global db, id

    cursor = db.cursor()
    query = "SELECT * FROM messaggi WHERE id=%s"
    record = (id,)
    cursor.execute(query, record)
    records = cursor.fetchall()
    return records



#receiver2
#text3

@app.route("/show", methods=['POST'])
def showNext():
    global id 
    messaggio = getMessageById()
    if(messaggio != []):
        data = {
            "Receiver" : messaggio[0][2],
            "Message" : messaggio[0][3],
            "Status" : 1
        }
    else:
        data = {
            "Receiver" : 0,
            "Message" : 0,
            "Status" : 0
        }
    id = id + 1
    return data



app.debug = False
app.run(port=5555)

