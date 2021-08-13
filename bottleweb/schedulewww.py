from bottle import route, run, request, install, static_file, template, redirect
from bottle_sqlite import SQLitePlugin
from schedule import *

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./bootstrap/js')

@route('/css/<filename>')
def css_static(filename):
    return static_file(filename, root='./bootstrap/css')

@route('/fonts/<filename>')
def fonts_static(filename):
  return static_file(filename, root='./bootstrap/fonts')

@route('/')
def home(db):
  #row = db.execute('SELECT * from schedule').fetchall())
  row = json.loads(get_schedules(db))
  if row:
    return template('home', schedules=row)
  return "Ack! We have encountered an error..."

def toggle(db, column, numid):
  # Toggle a boolean from 0 to 1 or 1 to 0
  #statusquery = db.execute('SELECT finish from schedule where id=?', numid).fetchone()
  statusstr = 'SELECT %s from schedule where id=?' % column
  statusquery = db.execute(statusstr, [numid]).fetchone()
  status = statusquery
  print status
  if status[0] == 0:
    updatestr = 'UPDATE schedule set %s=1 where id=?' % column
  elif status[0] == 1:
    updatestr = 'UPDATE schedule set %s=0 where id=?' % column
  row = db.execute(updatestr, [numid])
  db.commit()
  print updatestr, numid, row
  return

@route('/complete/<idnum>')
def finish(idnum, db):
  # Toggle a schedule's finish/absent status
  toggle(db, "complete", idnum)
  redirurl = "/page/" + str(idnum)
  redirect(redirurl)

@route('/page/done')
def all_done(db):
  schedules_complete = db.execute('SELECT * from schedule where complete=1').fetchall()
  schedules_uncomplete = db.execute('SELECT * from schedule where complete=0').fetchall()
  countquery = db.execute('SELECT count(*) from schedule').fetchone()
  count = countquery[0]
  complete_count = len(schedules_complete)
  uncomplete_count = len(schedules_uncomplete)
  # Calc percent completed
  percentage = float(complete_count) / float(count)
  percentage = percentage * 100
  percentage = int(percentage)
  return template('done', percentage=percentage, complete=complete_count, uncomplete=uncomplete_count)

@route('/page/<idnum>/description', method='POST')
def submit_description(idnum, db):
  description = request.forms.get('description')
  http_method = request.forms.get('http_method')
  if http_method == "PUT":
    put_data(db, idnum, column='description', data=description)
  redirurl = "/page/" + str(idnum)
  redirect(redirurl)

@route('/page/<idnum>')
def scheduleone(idnum, db):
  row = db.execute('SELECT * from schedule where id=?', [idnum]).fetchone()
  # Set previous and next links
  if int(idnum) >= 1:
    prevlink = int(idnum) - 1
  # Need to find number of schedules to find the last link
  countquery = db.execute('SELECT count(*) from schedule').fetchone()
  count = countquery[0]
  if int(idnum) == count:
    nextlink = "done"
  else:
    nextlink = int(idnum) + 1
  if row:
    return template('scheduleitem', schedule=row, prevlink=prevlink, nextlink=nextlink)
  return HTTPError(404, "Page not found")

if __name__ == "__main__":
  sqlite = SQLitePlugin(dbfile='schedule.db')
  install(sqlite)
 
  run(host='192.168.0.21', port=5000)
