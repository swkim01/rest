import json
from . import app, db, Schedule, get_schedules
from flask import send_from_directory, render_template, redirect, url_for

@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory('../bootstrap/js', filename)

@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory('../bootstrap/css', filename)

@app.route('/fonts/<path:filename>')
def fonts_static(filename):
    return send_from_directory('../bootstrap/fonts', filename)

@app.route('/')
def home():
  row = json.loads(get_schedules())
  if row:
    return render_template('home.html', schedules=row)
  return "Ack! We have encountered an error..."

def toggle(numid, column):
    # Toggle a boolean from 0 to 1 or 1 to 0
    row = db.session.query(Schedule).filter(Schedule.id==numid).first()
    if row:
        complete = row.complete
        # toggle complete flag
        if complete == 0:
            complete = 1
        else:
            complete = 0
        db.session.query(Schedule).filter(Schedule.id==numid).update({'complete': complete})
        db.session.commit()
    return

@app.route('/complete/<int:idnum>')
def finish(idnum):
  # Toggle a schedule's finish/absent status
  toggle(idnum, "complete")
  return redirect(url_for('scheduleone', idnum=idnum))

@app.route('/page/done')
def all_done():
  schedules_complete = db.session.query(Schedule).filter(Schedule.complete==1).all()
  schedules_uncomplete = db.session.query(Schedule).filter(Schedule.complete==0).all()
  count = db.session.query(Schedule).count()
  complete_count = len(schedules_complete)
  uncomplete_count = len(schedules_uncomplete)
  # Calc percent completed
  percentage = float(complete_count) / float(count)
  percentage = percentage * 100
  percentage = int(percentage)
  return render_template('done.html', percentage=percentage, complete=complete_count, uncomplete=uncomplete_count)

@app.route('/page/<int:idnum>/description', methods=['POST'])
def submit_description(idnum):
  description = request.form.get('description')
  http_method = request.form.get('http_method')
  if http_method == "PUT":
    put_data(idnum, description=description)
  return redirect(url_for('scheduleone', idnum=idnum))

@app.route('/page/<int:idnum>')
def scheduleone(idnum):
  row = db.session.query(Schedule).filter(Schedule.id==idnum).first()
  # Set previous and next links
  if int(idnum) >= 1:
    prevlink = int(idnum) - 1
  # Need to find number of schedules to find the last link
  count = db.session.query(Schedule).count()
  if int(idnum) == count:
    nextlink = "done"
  else:
    nextlink = int(idnum) + 1
  if row:
    return render_template('scheduleitem.html', schedule=row, prevlink=prevlink, nextlink=nextlink)
  return abort(404, "Page not found")

