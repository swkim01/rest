# rest
REST API of a schedule management example for raspberry pi.

Common files
- bootstrap : Bootstrap is an famous HTML, CSS, and JS framework.

Files for Python
- importcsv.py : creating an SQLite DB from a sample csv file
- schedule.py : REST api for schedule management
- schedulewww.py : web server for schedule management
- views/\*.tpl :

Files for Node.js
- package.json : configuration file for managing npm modules.
- schedule.js : REST api for schedule management
- schedulewww.js : web server for schedule management
- views/\*.hbs : handlebars template files.

#### Installation for Python
1.) You have to install Python Bottle and SQLite3 module.
```shell
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install bottle
sudo pip install bottle-sqlite
```
2.) Clone this repo onto your pi.
```shell
git clone https://github.com/swkim01/rest.git
cd rest
```
3.) Create schedule.db SQLite DB from sample csv file.
```shell
python importcsv.py schedule.csv
```
4.) For testing REST api, execute the server script.
```shell
python schedule.py
```
Then, you can test REST apis by using cURL.
```shell
curl http://<IP address>:<PORT>/schedule
curl http://<IP address>:<PORT>/schedule -H “Content-Type: application/json” -X POST -d ‘{“name”: “Reading”, "description": "Read a novel", "deadline": 10}’
curl http://<IP address>:<PORT>/schedule/schedule/1/description -X PUT -d ‘{”description”: ”Programming python”}’
```

5.) For testing RESTful web service, execute the web server.
```shell
python schedulewww.py
```

#### Installation for Node.js
1.) You have to install Node.js.
```shell
NODE_VERSION=6.3
wget http://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-armv7l.tar.gz
tar xvfz node-v$NODE_VERSION-linux-armv7l.tar.gz
cd node-v$NODE_VERSION-linux-armv7l
sudo cp -r * /usr/local/
```
2.) Clone this repo onto your pi.
```shell
git clone https://github.com/swkim01/rest.git
cd rest
```
3.) Install submodules(express, body-parser, body-parser-json, sqlite3, handlebars) by npm.
```shell
npm install
```
4.) For testing REST api, execute the server script.
```shell
npm start
```
or
```shell
node schedule.js
```
Then, you can test REST apis by using cURL.
```shell
curl http://<IP address>:<PORT>/schedule
curl http://<IP address>:<PORT>/schedule -H “Content-Type: application/json” -X POST -d ‘{“name”: “Reading”, "description": "Read a novel", "deadline": 10}’
curl http://<IP address>:<PORT>/schedule/schedule/1/description -X PUT -d ‘{”description”: ”Programming python”}’
```

5.) For testing RESTful web service, execute the web server.
```shell
node schedulewww.js
```
