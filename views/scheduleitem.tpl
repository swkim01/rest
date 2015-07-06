<html>
<head>
<link href="/css/bootstrap.css" rel="stylesheet">
<title>My Schedule</title>
</head>
<body>
<div class="container" style="padding-top:20px;">
<h1 align="center" style="font-size: 70;line-height:110%;">{{ schedule['name'] }}</h1>
<h3 align="center">Day: {{ schedule['deadline'] }}</h3>
% if schedule['complete'] == 0:
%   completestr = "Uncomplete"
% elif schedule['complete'] == 1:
%   completestr = "Complete"
% end
<h4 align="center" style="font-size:40;padding-top:20px;"><a href="/complete/{{ schedule['id'] }}">{{ completestr }}</a></h4>

<h4 align="center" style="padding:20px;">Notes: {{ schedule['description'] }}</td>
<form method="POST" action="/page/{{ schedule['id'] }}/description">
<input name="description" type="text" />
<input name="http_method" type="hidden" value="PUT" />
<input type="submit" value="Submit">
</form>
<a href="/page/{{ prevlink }}">Prev</a> <a href="/"><i class="icon-home"></i></a> <a href="/page/{{ nextlink }}">Next</a>
</div>
</body>
</html>
