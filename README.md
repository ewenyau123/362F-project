# 362f_Project
Create a shopping server for multi-clients access
## Set Up The Enviroment
### Create your Own Database Server
Using the Mac OS, need to use mysql and the phpmyadmin for the database GUI

1.  Installing mysql 
  ~brew install mariadb
  ~mysql.server start
  ~brew services start mariadb
  
2. Login mysql: ~sudo mysql -u root
3. set up the mysql 

###instal phpmyadmin
1.download the file from https://www.phpmyadmin.net/downloads/
2.~unzip phpMyAdmin-5.0.1-all-languages.zip
3.~mv phpMyAdmin-5.0.1-all-languages phpMyAdmin
4.
  ~cd /Library/WebServer/Documents/phpmyadmin/
  ~cp config.sample.inc.php config.inc.php

### Import Data
Import the data in your database server with usingphpmyadmin
1.  press import button on the top bar
2. select the shopping.sql file and import

There will be 3 tables in the schema after the import and refresh your database server

## Configure
1. Go to `database.py` and `owner.py` :
```python
	db = mysql.connector.connect(user='root',password='root',
                              host='127.0.0.1',database='362f')
```
## How to Run
1.  Install python library
```bash
pip install mysql-connector
pip install base64
pip install bottle
pip install selenium
pip install dataclasses
pip install prettytable
pip install re
pip install urllib.parse
```
2. Change to your folder root in cmd 
Example:
```bash
cd C:\Downloads\362f_Project
```
3. Run `app.py`
```bash
python3 app.py
```
You can see below outcome:
> Bottle v0.12.19 server starting up (using PasteServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.
serving on http://127.0.0.1:8080
4. Run http://127.0.0.1:8080 in your browser
![](https://github.com/Lukwok/362f_Project/blob/main/ReadMe_image/login.jpg)
> Login as customer: username= guest/user  
Login as shop owner: username= owner 
Password is no required
5. After login, you can see the main page. Please enjoy different functions by your own
![](https://github.com/Lukwok/362f_Project/blob/main/ReadMe_image/home.jpg)
6. Run `automic_test.py`
```bash
python3 automic_test.py
```
7. Run `automic_test_customer.py`
```bash
python3 automic_test_customer.py
```
