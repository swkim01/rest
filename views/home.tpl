<!DOCTYPE html>
<html>
<head>
<link href="/css/bootstrap.css" rel="stylesheet">
<title>My Schedule</title>
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
%     completestr = "icon-remove"
%   elif item['complete'] == 1:
%     completestr = "icon-ok"
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
</body>
</html>
