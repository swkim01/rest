<!DOCTYPE html>
<html>
<head>
<title>My Schedule</title>
<link href="/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container">
<p>
<a href="/page/done">Status</a>
</p>
<table class="table table-striped">
<tr>
  <th>Schedule Name</th>
  <th>Deadline</th>
  <th>Description</th>
  <th>Complete?</th>
</tr>
% for item in schedules:
%   if item['complete'] == 0:
%     completestr = "glyphicon-remove"
%   elif item['complete'] == 1:
%     completestr = "glyphicon-ok"
% end
<tr>
  <td><a href="/page/{{ item['id'] }}">{{ item['name'] }}</a></td>
  <td>{{ item['deadline'] }}</td>
  <td>{{ item['description'] }}</td>
  <td><i class="{{ completestr }}"></i></td>
</tr>

%end
</table>
</div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="/js/bootstrap.min.js"></script>
</body>
</html>
