# 362f_Project
Create a shopping server for multi-clients access
## Set Up The Enviroment
### Create your Own Database Server
Using the Mac OS, need to use mysql and the phpmyadmin for the database GUI

1.  Installing mysql 
  - `brew install mariadb`
  - `mysql.server start`
  - `brew services start mariadb`
  
2. Login mysql: - `sudo mysql -u root`
3.  - `set up the mysql`

###instal phpmyadmin
1.download the file from https://www.phpmyadmin.net/downloads/
2.- `unzip phpMyAdmin-5.0.1-all-languages.zip`
3.- `mv phpMyAdmin-5.0.1-all-languages phpMyAdmin`
4.
  - `cd /Library/WebServer/Documents/phpmyadmin/`
  - `cp config.sample.inc.php config.inc.php`

### Import Data
Import the data in your database server with usingphpmyadmin
1.  press import button on the top bar
2. select the shopping.sql file and import

There will be 2 tables in the mysql after the import and refresh your database server

Config in server.py fo connect to the server
In server.py line 17, here is the config of connecting database
Change the config to fit your database
##Next

We need to install the module

1.  Install python library
```
pip install mysql-connector
pip install base64
pip install selenium
pip install http
pip install socketserver
pip install jinja2
pip install magic
pip install os
pip install json
pip install datetime
pip install cgi
pip install urllib.parse
```
2. Change the file direction to your download folder in cmd 
Example:
```
cd /Downloads/362f-project
```
3. Run `server.py`

if it success, it will show the message "Start Server"
if you want to stop the server, Ctrl+C to stop it


4. Run http://localhost:2222 in your browser

Login : username = 10001 

5. Run `test_shopping_customer.py`

6. Run `notenough.py`

7. Run `replenish_test.py`
	

