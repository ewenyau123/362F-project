# import BaseHTTPRequestHandler
import http.server  
from http import cookies
from socketserver import ThreadingTCPServer, BaseRequestHandler
import threading
from jinja2 import Environment, FileSystemLoader
import magic
import os
import mysql.connector
from urllib.parse import unquote
import json
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
import base64
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin123",
  database="shopping"
)
mycursor = mydb.cursor()

PWD = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def check_cookie(self):
        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        print(cookies)
        try:
            print(cookies)
            return True
        except:
            return False

    def do_GET(self):
        if self.path == '/':
            self.do_login()
        elif self.path == '/listcart':
            self.do_listcart()
        elif self.path == '/done':
            self.do_done()
        elif self.path == '/carderror':
            self.do_carderror()
        elif self.path == '/notenough':
            self.do_notenough()
        elif self.path == '/addstock':
            self.do_addstock()
        else:
            self.staticFile(self.path)

    def staticFile(self, path):
        try:
            filePath = os.path.realpath("./templates" + path)
            with open(filePath, 'rb') as fh:
                mime = magic.Magic(mime=True)
                self.send_response(200)
                self.send_header('Content-Type', mime.from_file(filePath))
                self.end_headers()
                html = fh.read()
                self.wfile.write(html)
        except:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/':
            self.do_authlogin()
        elif self.path == '/listcart':
            self.do_listcart()
        elif self.path == '/checkout':
            self.do_checkout()
        elif self.path == '/addstock':
            self.do_add()

    def do_done(self):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('done.html')
        output = template.render()
        self._set_response()
        self.wfile.write(bytes(output, 'utf-8'))

    def do_carderror(self):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('wrongcard.html')
        output = template.render()
        self._set_response()
        self.wfile.write(bytes(output, 'utf-8'))

    def do_notenough(self):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('notenough.html')
        output = template.render()
        self._set_response()
        self.wfile.write(bytes(output, 'utf-8'))

    def do_login(self):
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('login.html')
        output = template.render()
        self._set_response()
        self.wfile.write(bytes(output, 'utf-8'))
        return

    def do_authlogin(self):
        mycursor.execute("SELECT * FROM customer")
        myresult = mycursor.fetchall()
        clientid = []
        for x in myresult:
            clientid.append(x[0])
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length).decode("utf-8").split("=")
        if int(post_data[1]) in clientid:
            self.do_list(post_data[1])
        else:
            self.do_login()

    def do_list(self,data):
        mycursor.execute("SELECT * FROM product")
        myresult = mycursor.fetchall()
        self.send_response(200)
        self.send_header('Content-type','text/html')
        cookie = http.cookies.SimpleCookie()
        cookie['client_id'] = data
        cookie['client_id']['max-age'] = 60
        for morsel in cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())
        self.end_headers()
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('list.html')
        output = template.render(items=myresult)
        self.wfile.write(bytes(output, 'utf-8'))
    
    def do_listcart(self):
        if self.check_cookie():
            cookie = http.cookies.SimpleCookie()
            content_length = int(self.headers['Content-Length'])
            post_data = unquote(self.rfile.read(content_length).decode("utf-8"))
            cartdata=[]
            total=[]
            cart_sum=0
            if post_data.find("cart")== -1:
                data= post_data.split(";")
                post_data_split=data[0].split("=")
                clientid=post_data_split[2]
                cookie['client_id'] = clientid
                cookie['client_id']['max-age'] = 60
            else:
                data=post_data.split(";")
                post_data_split=data[0].split("=")
                cart_data_split=data[1].split("=")
                clientid=post_data_split[2]
                cartdata=json.loads(cart_data_split[1])
                cookie['client_id'] = clientid
                cookie['client_id']['max-age'] = 60
                cookie['cart'] = cart_data_split[1]
                cookie['cart']['max-age'] = 60
            mycursor.execute("SELECT * FROM product")
            myresult = mycursor.fetchall()
            for x in cartdata:
                subtotal=[]
                for y in myresult:
                    if int(x['productid']) in y:
                        subtotal.append(x['productid'])
                        subtotal.append(y[1])
                        subtotal.append(x['no'])
                        subtotal.append(y[2])
                        subtotal.append(int(x['no'])*y[2])
                        total.append(subtotal)
                        cart_sum+=int(x['no'])*y[2]
            print(total)
            print(cart_sum)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            for morsel in cookie.values():
                self.send_header("Set-Cookie", morsel.OutputString())
            self.end_headers()
            message_bytes = json.dumps(total).encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
            file_loader = FileSystemLoader('templates')
            env = Environment(loader=file_loader)
            template = env.get_template('listcart.html')
            output = template.render(cartdata = base64_message,data=total,clientid=clientid,total_sum=cart_sum)
            self.wfile.write(bytes(output, 'utf-8'))
        else:
            self.send_response(302)
            self.send_header('Location','http://localhost:2222/')
            self.end_headers()

    def do_checkout(self):
        cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        print(cookies)
        assert self.headers['Content-Type'] == 'application/x-www-form-urlencoded'
        length = int(self.headers['content-length'])
        data_lists = parse_qs(
            self.rfile.read(length),
            # Strict options:
            keep_blank_values=True,
            strict_parsing=True,
            errors='strict',
        )
        # Flatten the listed values.
        data_flat = {k.decode("utf-8"): v.decode("utf-8") for (k, [v]) in data_lists.items()}
        cartdata=data_flat.get('cartdetail')
        base64_bytes = cartdata.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = json.loads(message_bytes.decode('ascii'))

        clientid = data_flat.get('clientid')
        creditcard = data_flat.get('number')
        creditdate = data_flat.get('expired').split("-")
        ccv = data_flat.get('cvv')

        mycursor.execute("SELECT * FROM product")
        myresult = mycursor.fetchall()
        nocheck= False
        datecheck=False
        if 12 < len(creditcard) < 17 :
            first2 = creditcard[0:2]
            first4 = creditcard[0:4]

            vendor = None
            if creditcard[0] == "4" :
                vendor = "Visa"
            if creditcard[0] == "5" and "0" < creditcard[1] < "6":
                vendor = "MasterCard"
            if first2 in ("36", "38"):
                vendor = "Diners Club"
            if first4 == "6011" or first2 == "65":
                vendor = "Discover"
            if first2 == "35":
                vendor = "JCB"
            if first2 in ("34", "37"):
                vendor = "American Express"

            if vendor is not None:
                nocheck =True

        now = datetime.datetime.now()
        if int(now.year)<=int(creditdate[0]) and int(now.month)<=int(creditdate[1]):
            datecheck=True
        enoughcheck = False
        if nocheck and datecheck:
            for x in message:
                for y in myresult:
                    if int(x[0]) in y:
                        if x[2]<=y[3]:
                            sql="UPDATE product SET quantity="+str(y[3]-x[2])+" WHERE product_id = "+str(x[0])+";"
                            mycursor.execute(sql)
                            mydb.commit()
                            enoughcheck=True
                        else:
                            enoughcheck=False
            if enoughcheck:
                self.send_response(302)
                for morsel in cookies.values():
                    self.send_header("Set-Cookie", morsel.OutputString())
                self.send_header('Location','http://localhost:2222/done')
                self.end_headers()
            else:
                self.send_response(302)
                self.send_header('Location','http://localhost:2222/notenough')
                self.end_headers()
        else:
            self.send_response(302)
            self.send_header('Location','http://localhost:2222/carderror')
            self.end_headers()

    def do_addstock(self):
        mycursor.execute("SELECT * FROM product")
        myresult = mycursor.fetchall()
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('addstock.html')
        output = template.render(items=myresult)
        self.wfile.write(bytes(output, 'utf-8'))
    
    def do_add(self):
        assert self.headers['Content-Type'] == 'application/x-www-form-urlencoded'
        length = int(self.headers['content-length'])
        data_lists = parse_qs(
            self.rfile.read(length),
            keep_blank_values=True,
            strict_parsing=True,
            errors='strict',
        )
        data_flat = {k.decode("utf-8"): v.decode("utf-8") for (k, [v]) in data_lists.items()}
        print(data_flat)
        productid=data_flat.get('product')
        number = data_flat.get('quantity')
        sql="UPDATE product SET quantity=quantity+"+str(number)+" WHERE product_id = "+str(productid)+";"
        print(sql)
        mycursor.execute(sql)
        print(mycursor.rowcount)
        mydb.commit()
        if mycursor.rowcount !=0:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            file_loader = FileSystemLoader('templates')
            env = Environment(loader=file_loader)
            template = env.get_template('addsuccess.html')
            output = template.render()
            self.wfile.write(bytes(output, 'utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            file_loader = FileSystemLoader('templates')
            env = Environment(loader=file_loader)
            template = env.get_template('addfail.html')
            output = template.render()
            self.wfile.write(bytes(output, 'utf-8'))
    
        

if __name__ == '__main__':
    server = ThreadingTCPServer(("127.0.0.1", 2222), Handler)
    print('Starting server')
    server.serve_forever()
