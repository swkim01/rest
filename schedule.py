#from bottle import route, run, request, install, static_file, template, redirect
import json
from bottle import *
#import bottle
from bottle_sqlite import SQLitePlugin

def get_schedules(db):
  row = db.execute('SELECT * from schedule').fetchall()
  if row:
    #return template('home', schedules=row)
    results = []
    for data in row:
        results.append(dict(data))
    return json.dumps(results)
  return null

@route('/schedule', method='GET')
def schedules(db):
    response.content_type = 'application/json'
    return get_schedules(db)

@route('/schedule', method='POST')
def create_schedule(db):
    if not request.json or not 'name' in request.json:
        abort(400)
    row = db.execute('SELECT * from schedule').fetchall()
    if row:
        id = row[-1]['id'] + 1
    else:
        id = 1
    import datetime
    deadline = str(datetime.datetime.now()+datetime.timedelta(days=request.json.get('deadline', 0)))
    schedule = {
        'id': id,
        'name': request.json['name'],
        'deadline': deadline,
        'description': request.json.get('description', ""),
        'complete': 0
    }
    db.execute("INSERT INTO schedule VALUES (?, ?, ?, ?, ?)", (schedule['id'], schedule['name'], schedule['deadline'], schedule['description'], schedule['complete']))
    db.commit()
    return HTTPResponse(status=201, body=json.dumps(schedule))

@route('/schedule/<idnum>', method='GET')
def schedule(idnum, db):
  row = db.execute('SELECT * from schedule where id=?', [idnum]).fetchone()
  if row:
    response.content_type = 'application/json'
    return json.dumps(dict(row))
  return HTTPError(404, "Page not found")

@route('/schedule/<idnum>', method='DELETE')
def delete_schedule(idnum, db):
  delete = db.execute('DELETE from schedule where id=?', [idnum])
  db.commit()
  return ''

def put_data(db, numid, column, data):
  # Put data
  db.text_factory = str
  row = db.execute('SELECT * from schedule where id=?', [numid]).fetchone()
  if row:
    updatestr = 'UPDATE schedule set %s=? where id=?' % column
    print column, data
    update_data = db.execute(updatestr, [data, numid])
    db.commit()
    row = db.execute('SELECT * from schedule where id=?', [numid]).fetchone()
    if row:
      return json.dumps(dict(row))
  return HTTPError(404, "Data not found")

@route('/schedule/<idnum>/name', method='PUT')
def put_name(idnum, db):
  if not request.json or not 'name' in request.json:
      abort(400)
  name = request.json['name']
  response.content_type = 'application/json'
  return put_data(db, idnum, column='name', data=name)

@route('/schedule/<idnum>/description', method='PUT')
def put_description(idnum, db):
  if not request.json or not 'description' in request.json:
      abort(400)
  description = request.json['description']
  response.content_type = 'application/json'
  return put_data(db, idnum, column='description', data=description)

@route('/schedule/<idnum>/deadline', method='PUT')
def put_deadline(idnum, db):
  if not request.json or not 'deadline' in request.json:
      abort(400)
  # deadline format is %d/%m/%y %H:%M
  import datetime
  deadline = datetime.datetime.strptime(request.json.get('deadline', datetime.datetime.now()), "%d/%m/%y %H:%M")
  response.content_type = 'application/json'
  return put_data(db, idnum, column='deadline', data=deadline)

@route('/schedule/<idnum>/complete', method='PUT')
def put_complete(idnum, db):
  row = db.execute('SELECT * from schedule where id=?', [idnum]).fetchone()
  if row:
    complete = row['complete']
    # toggle complete flag
    if complete == 0:
      complete = 1
    else:
      complete = 0
    response.content_type = 'application/json'
    return put_data(db, idnum, column='complete', data=complete)
  return HTTPError(404, "Data not found")

if __name__ == "__main__":
  sqlite = SQLitePlugin(dbfile='schedule.db')
  install(sqlite)
 
  run(host='<HOST IP>', port=<PORT>)
