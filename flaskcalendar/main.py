from flask import Flask
from flask import request, render_template, jsonify
import json
import pprint
import datetime

app = Flask(__name__)

import sqlite3
from sqlite3 import Error
class Event:
    

    def __init__(self):
        
        self.sql_create_tasks_table ="""
            CREATE TABLE IF NOT EXISTS `events` (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,             
            `title` varchar(255) NOT NULL,
            `start_event` datetime NOT NULL,
            `end_event` datetime NOT NULL,
            `ressource` varchar(255) NOT NULL
            ) ;"""

        self.lastid = None
        self.conn = self.create_connection("schedule.db")
        # create tables
        if self.conn is not None:
            # create projects table
            self.create_table()            
        else:
            print("conn None")        

    def create_table(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(self.sql_create_tasks_table)
            self.conn.commit()
            self.conn.close()
        except Error as e:
            print(e)

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)

        except Error as e:
            print(e)
        finally:
            return conn

    def executeSql(self, cmd ):
        try:
            self.conn = self.create_connection("schedule.db")
            c = self.conn.cursor()
            c.execute(cmd)
            self.lastid = c.lastrowid
            self.conn.commit()
            self.conn.close()
        except Error as e:
            print(e)
    
    def get_events(self):        
        try:
            self.conn = self.create_connection("schedule.db")
            c = self.conn.cursor()
            c.execute("select * from events")            
            rows = c.fetchall()
            self.conn.close()
            pprint.pprint(rows)
            return rows
        except Error as e:
            print(e)


    def createEvent(self, date, resource, title):
        sqlCommand = "INSERT INTO events (start_event,end_event,ressource,title) values ('%s','%s','%s','%s') " % (date,date,resource,title)
        self.executeSql(sqlCommand)
        return str(self.lastid)


    def editEvent(self,start,id, resource):
        if resource =="null":
            sqlCommand = "UPDATE events SET start_event='%s' WHERE id = %s" % (start,id)
        else:
            sqlCommand = "UPDATE events SET start_event='%s', ressource='%s' WHERE id = %s" % (start,resource,id)
        
        self.executeSql(sqlCommand) 
        return 
        #print(start)
        #print(end)
        #print(id)

    def resizeEvent(self,start,end,id):
        sqlCommand = "UPDATE events SET start_event='%s', end_event='%s' WHERE id = %s" % (start,end,id)
        self.executeSql(sqlCommand)
        #print(start)
        #print(end)
        #print(id)


event = Event()


def parseDate(strdate):
     t = strdate.split("/")
     print(t)
     return datetime.date(int(t[2]),int(t[0]),int(t[1]))

@app.route('/create-event', methods=['POST'])
def createevent():    
    #print(request.values["date"])
    #print(request.values["resource"])
    return event.createEvent(request.values["date"],request.values["resource"], request.values["title"])

@app.route('/edit-event', methods=['POST'])
def editevent():
    event.editEvent(request.values["start"],request.values["id"],request.values["resource"])
    #print(request.values["start"])
    #print(request.values["end"])
    #print(request.values["id"])
    return ""

@app.route('/resize', methods=['POST'])
def resize():
    event.resizeEvent(request.values["start"],request.values["end"],request.values["id"])
    #print(request.values["start"])
    #print(request.values["end"])
    #print(request.values["id"])
    return ""
    

@app.route('/')
def calendar():
    return render_template("resource-event-json.html")


@app.route('/json/<filename>')
def return_json(filename):
    event.get_events()
    with open("flaskcalendar/json/%s" % ( filename ) , "r") as input_data:
        return input_data.read()

@app.route('/events')
def return_events():
    jsonevents = []
    for e in event.get_events():                
        jsonevents.append({"id":e[0],"title":e[1],"start":parseDate(e[2]).isoformat(),"end":parseDate(e[3]).isoformat(),"resourceId":e[4]})        
    return jsonify(jsonevents)    
    

@app.route('/ressources')
def return_ressources():
    with open("flaskcalendar/json/resources.json", "r") as input_data:
        # you should use something else here than just plaintext
        # check out jsonfiy method or the built in json module
        # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
        return input_data.read()

@app.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    # You'd normally use the variables above to limit the data returned
    # you don't want to return ALL events like in this code
    # but since no db or any real storage is implemented I'm just
    # returning data from a text file that contains json elements

    with open("flaskcalendar/json/events-for-resources.json", "r") as input_data:
        # you should use something else here than just plaintext
        # check out jsonfiy method or the built in json module
        # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
        return input_data.read()

if __name__ == '__main__':
    app.debug = True
    app.run()
