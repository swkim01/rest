var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var sqlite3 = require('sqlite3').verbose();
var fs = require('fs');
var csv = require('csv');
var router = express.Router();

app.use(bodyParser.json());

fs.stat('schedule.db', function(err, stats) {
  if (err) {
    var db = new sqlite3.Database('schedule.db');
    console.log('schedule.db not found');
    db.serialize(function() {
      db.run("CREATE TABLE schedule ( id INTEGER PRIMARY KEY, name TEXT, deadline TIMESTAMP, description TEXT, complete INTEGER )");
      var csvfile = fs.createReadStream('sample_schedule.csv');
      var index = 0;
      csvfile.pipe(csv.parse())
        .pipe(csv.transform(function(record) {
          index = index + 1;
          var datetime = new Date();
          console.log(record);
          datetime.setDate (datetime.getDate() + index);
          db.run("INSERT INTO schedule VALUES (?, ?, ?, ?, ?)", index, record[0], datetime.toISOString(), record[1], 0);
        }));
    });
  }
});

var db = new sqlite3.Database('schedule.db');

function get_schedules(res) {
  db.all('SELECT * from schedule',function(err,rows) {
    var results = new Array();
    rows.forEach(function (row) {
      results.push(row);
    });
    res.json(results);
  });
};

router.get('/', function(req, res) {
  get_schedules(res);
});

router.post('/', function(req,res) {
  if (!req.body || !req.body.name) {
    res.sendStatus(400);
  }
  else {
    db.all('SELECT * from schedule', function(err, rows) {
      console.log(rows);
      var id = rows[rows.length-1].id+1;
      var datetime = new Date();
      datetime.setDate (datetime.getDate() + req.body.deadline);
      var schedule = {
        'id': id,
        'name': req.body.name,
        'deadline': datetime.toISOString(),
        'description': req.body.description,
        'complete': 0
      };
      db.run("INSERT INTO schedule VALUES (?, ?, ?, ?, ?)", schedule.id, schedule.name, schedule.deadline, schedule.description, schedule.complete);
      res.json(schedule);
    });
  }
});

router.get('/:id', function(req, res) {
  db.get('SELECT * from schedule where id=?', req.params.id, function(err, row) {
    if (err || !row) {
      res.sendStatus(404);
    }
    else {
      res.json(row);
    }
  });
});

router.delete('/:id', function(req, res) {
  db.run('DELETE from schedule where id=?', req.params.id);
  res.send(true);
});

function put_data(db, numid, column, data) {
  // Put data
  var data;
  db.serialize(function() {
    db.get('SELECT * from schedule where id=?', numid, function(err, testrow) {
      if (err || !testrow) {
        data = null;
      }
      else {
        console.log("column="+column+", data="+data+", numid="+numid);
        db.run('UPDATE schedule set '+column+'=? where id=?', data, numid);
        db.get('SELECT * from schedule where id=?', numid, function(err, row) {
          if (err || !row) {
            data = null;
          }
          else {
            data = row;
          }
        });
      }
    });
  });
  return data;
};

router.put('/:id/name', function(req, res) {
  if (!req.body || !req.body.name) {
    res.sendStatus(400);
  }
  else {
    var data = put_data(db, req.params.id, 'name', req.body.name);
    if (data == null)
      res.sendStatus(404);
    else
      res.json(data);
  }
});

router.put('/:id/description', function(req, res) {
  if (!req.body || !req.body.description) {
    res.sendStatus(400);
  }
  else {
    var data = put_data(db, req.params.id, 'description', req.body.description);
    if (data == null)
      res.sendStatus(404);
    else
      res.json(data);
  }
});

router.put('/:id/deadline', function(req, res) {
  if (!req.body || !req.body.deadline) {
    res.sendStatus(400);
  }
  else {
    // deadline format is %d/%m/%y %H:%M
    var datetime = new Date();
    datetime.setDate (datetime.getDate() + req.body.deadline);
    var data = put_data(db, req.params.id, 'deadline', datetime.toISOString());
    if (data == null)
      res.sendStatus(404);
    else
      res.json(data);
  }
});

router.put('/:id/complete', function(req, res) {
  db.get('SELECT * from schedule where id=?', req.params.id, function(err, row) {
    if (err || !row) {
      res.sendStatus(404);
    }
    else {
      // toggle complete flag
      var complete = (row.complete==0)?1:0;
      var data = put_data(db, req.params.id, 'complete', complete);
      if (data == null)
        res.sendStatus(404);
      else
        res.json(data);
    }
  });
});

app.use('/schedule', router);

app.listen(5000, function() {
  console.log("Live at Port 5000");
});
