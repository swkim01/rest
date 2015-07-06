<html>
<head>
<link href="/css/bootstrap.css" rel="stylesheet">
<title>Schedule - Status</title>
</head>
<body>
<div class="container">
  <div class="span4">
    <a href="/"><i class="icon-home"></i></a>
  </div>
  <div class="span4">
    <h1>Schedule Status</h1>
    <table class="table table-bordered table-condensed">
    <thead>
    <tr>
      <th>Complete</th>
      <th>Uncomplete</th>
      <th>Percentage Complete</th>
    </tr>
    </thead>
    <tbody>
    <tr>
      <td>{{ complete }}</td>
      <td>{{ uncomplete }}</td>
      <td>{{ percentage }}</td>
    </tr>
    </tbody>
    </table>
  </div>
</div>
</body>
</html>
