from flask import Flask
from flask import request, render_template, jsonify
import json


app = Flask(__name__)

import sqlite3
from sqlite3 import Error

sql_create_tasks_table ="""
    CREATE TABLE IF NOT EXISTS `events` (
    `id` int(11) PRIMARY KEY NOT NULL,
    `title` varchar(255) NOT NULL,
    `start_event` datetime NOT NULL,
    `end_event` datetime NOT NULL
    ) ;"""

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

    except Error as e:
        print(e)
    finally:
        return conn

conn = create_connection("schedule.db")
# create tables
if conn is not None:
    # create projects table
    create_table(conn, sql_create_tasks_table)
else:
    print("conn None")


@app.route('/')
def calendar():
    return render_template("resource-event-json.html")

@app.route('/json/<filename>')
def return_json(filename):
    with open("flaskcalendar/json/%s" % ( filename ) , "r") as input_data:
        return input_data.read()

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
