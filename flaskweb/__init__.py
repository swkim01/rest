import json
from flask import Flask, request, url_for, render_template, abort, jsonify, make_response, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pi/rest/schedule.db'
db = SQLAlchemy(app)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #deadline = db.Column(db.DateTime)
    deadline = db.Column(db.String)
    description = db.Column(db.Text)
    complete = db.Column(db.String)

    def __init__(self, id=1, name=None, deadline=None, description=None, complete=0):
        self.id = id
        self.name = name
        self.deadline = deadline
        self.description = description
        self.complete = complete

    def __repr__(self):
        return '<Schedule %r>' % self.name

def obj_as_dict(obj):
   return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def get_schedules():
    #row = db.session.execute('SELECT * from schedule').fetchall()
    row = db.session.query(Schedule).all()
    if row:
        #return template('home', schedules=row)
        results = []
        for data in row:
            #print(data.__dict__)
            results.append(obj_as_dict(data))
        return json.dumps(results)
        #return jsonify(results)
    return null

@app.route('/schedule', methods=['GET'])
def schedules():
    return jsonify(get_schedules())

@app.route('/schedule', methods=['POST'])
def create_schedule():
    if not request.json or not 'name' in request.json:
        abort(400)
    #row = db.session.execute('SELECT * from schedule').fetchall()
    row = db.session.query(Schedule).all()
    if row:
        #id = row[-1]['id'] + 1
        id = row[-1].id + 1
    else:
        id = 1
    import datetime
    deadline = str(datetime.datetime.now()+datetime.timedelta(days=request.json.get('deadline', 0)))
    schedule = Schedule(id, request.json['name'], deadline, request.json.get('description', ""))
    #db.execute("INSERT INTO schedule VALUES (?, ?, ?, ?, ?)", (schedule['id'], schedule['name'], schedule['deadline'], schedule['description'], schedule['complete']))
    #db.commit()
    db.session.add(schedule)
    return make_response(jsonify(obj_as_dict(schedule)))

@app.route('/schedule/<int:idnum>', methods=['GET'])
def schedule(idnum):
    row = db.session.query(Schedule).filter(Schedule.id==idnum).first()
    if row:
        return jsonify(obj_as_dict(row))
    return abort(404, "Page not found")

@app.route('/schedule/<int:idnum>', methods=['DELETE'])
def delete_schedule(idnum):
    #delete = db.session.execute('DELETE from schedule where id=?', [idnum])
    db.session.query(Schedule).filter(Schedule.id==idnum).delete()
    db.session.commit()
    return ''

def put_data(numid, **kwargs):
    # Put data
    row = db.session.query(Schedule).filter(Schedule.id==numid).update(kwargs)
    db.session.commit()
    if row:
        row = db.session.query(Schedule).filter(Schedule.id==numid).first()
        if row:
            return jsonify(obj_as_dict(row))
    return abort(404, "Data not found")

@app.route('/schedule/<int:idnum>/name', methods=['PUT'])
def put_name(idnum):
    if not request.json or not 'name' in request.json:
        abort(400)
    name = request.json['name']
    return put_data(idnum, name=name)

@app.route('/schedule/<int:idnum>/description', methods=['PUT'])
def put_description(idnum):
    if not request.json or not 'description' in request.json:
        abort(400)
    description = request.json['description']
    return put_data(idnum, description=description)

@app.route('/schedule/<int:idnum>/deadline', methods=['PUT'])
def put_deadline(idnum):
    if not request.json or not 'deadline' in request.json:
        abort(400)
    # deadline format is %d/%m/%y %H:%M
    import datetime
    deadline = datetime.datetime.strptime(request.json.get('deadline', datetime.datetime.now()), "%d/%m/%y %H:%M")
    return put_data(idnum, deadline=deadline)

@app.route('/schedule/<int:idnum>/complete', methods=['PUT'])
def put_complete(idnum):
    row = db.session.query(Schedule).filter(Schedule.id==idnum).first()
    if row:
        complete = row.complete
        # toggle complete flag
        if complete == 0:
            complete = 1
        else:
            complete = 0
        return put_data(idnum, complete=complete)
    return abort(404, "Data not found")

from . import web
