var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('schedule.db');
var path = __dirname + '/views/';
var fs = require('fs');
var handlebars = require('handlebars');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true}));
app.use("/css", express.static('./bootstrap/css'));
app.use("/js", express.static('./bootstrap/js'));
app.use("/fonts", express.static('./bootstrap/fonts'));

handlebars.registerHelper('list', function(context, options) {
  var ret = "";
  for(var i=0, j=context.length; i<j; i++) {
    ret = ret + options.fn(context[i]);
  }
  return ret;
});

handlebars.registerHelper('if', function(complete, options) {
  if (complete) {
    return options.fn(this);
  }
  else {
    return options.inverse(this);
  }
});

app.get('/', function(req,res) {
  db.all('SELECT * from schedule',function(err,rows) {
    var results = new Array();
    rows.forEach(function (row) {
      results.push(row);
    });
    if (results.length == 0)
      res.send("Ack! We have encountered an error...")
    else {
      fs.readFile(path+'home.hbs', 'utf-8', function(err, src) {
        var template = handlebars.compile(src);
        res.send(template({schedules: results}));
      });
    }
  });
});

app.get('/complete/:id', function(req,res) {
  // Toggle a schedule's finish/absent status
  db.get('SELECT complete from schedule where id=?', req.params.id, function(err, row) {
    if (err || !row) {
      res.sendStatus(404);
    }
    else {
      var updatestr;
      if (row.complete == 0)
        updatestr = 'UPDATE schedule set complete=1 where id=?';
      else if (row.complete == 1)
        updatestr = 'UPDATE schedule set complete=0 where id=?';
      db.run(updatestr, req.params.id);
      res.redirect("/page/" + req.params.id);
    }
  });
});

app.get('/page/done', function(req,res) {
  db.serialize(function() {
    var complete_count=0;
    db.all('SELECT * from schedule where complete=1', function(err, rows) {
      if (rows)
        complete_count = rows.length;
    });
    var uncomplete_count=0;
    db.all('SELECT * from schedule where complete=0', function(err, rows) {
      if (rows)
        uncomplete_count = rows.length;
    });
    db.get('SELECT count(*) from schedule', function(err, row) {
      var count=0;
      if (row)
        count = row["count(*)"];
      // Calc percent completed
      var percentage = complete_count / count;
      percentage = parseInt(percentage * 100);
      fs.readFile(path+'done.hbs', 'utf-8', function(err, src) {
        var template = handlebars.compile(src);
        res.send(template({"percentage": percentage, "complete":complete_count, "uncomplete": uncomplete_count}));
      });
    });
  });
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

app.post('/page/:id/description', function(req,res) {
  if (!req.body || !req.body.description) {
    res.sendStatus(400);
  }
  else {
    description = req.body.description;
    put_data(db, req.params.id, 'description', description);
    res.redirect("/page/" + req.params.id);
  }
});

app.get('/page/:id', function(req,res) {
  db.get('SELECT * from schedule where id=?', req.params.id, function(err,row) {
    if (err || !row) {
      res.sendStatus(404);
    }
    else {
      // Set previous and next links
      var prevlink="done";
      if (req.params.id > 1)
        prevlink = parseInt(req.params.id) - 1;
      // Need to find number of schedules to find the last link
      var count=0;
      db.get('SELECT count(*) from schedule', function(err, data) {
        if (data)
          count = data["count(*)"];

        var nextlink;
        if (req.params.id == count)
          nextlink = "done";
        else
          nextlink = parseInt(req.params.id) + 1;

        fs.readFile(path+'scheduleitem.hbs', 'utf-8', function(err, src) {
          var template = handlebars.compile(src);
          res.send(template({"schedule": row, "prevlink":prevlink, "nextlink": nextlink}));
        });
      });
    }
  });
});

app.listen(5000, function() {
  console.log("Live at Port 5000");
});
