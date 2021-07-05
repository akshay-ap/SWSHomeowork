#!/usr/bin/env python3

import sys
import secrets
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    from http import cookies
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')
import sqlite3
from reset_database import reset_database
from cgi import parse_header, parse_multipart
from random import randint
import datetime

DATABASE_FILE = 'website.sqlite3'

form_doc = '''
<!doctype html>
<html><body>
<h1>SEC Intranet</h1>
<form method="post">
    User: <input name="user"> <br>
    Password: <input name="pass" type="password">
<br>
<input type="submit" name="action" value="login">
</form>
</body></html>
'''


authenticated_doc = '''
<!doctype html>
<html><body>
<h1>SEC Intranet</h1>
You are logged in as {username}!
<form method="post">
    <input type="submit" name="action" value="logout">
</form>
<br>
If you are an administrator, you can use the <a href="/admin">admin interface</a>.
</body></html>
'''

success = '''
<!doctype html>
<html><body>
<h1>SEC Intranet</h1>
Welcome, {user}!
</html></body>
'''

fail = '''
<!doctype html>
<html><body style="color:red;">
<h1>SEC Intranet</h1>
{message}
</html></body>
'''

sessions = {}


class MyHandler(BaseHTTPRequestHandler):
    saved_headers = []
    
    def get_or_create_session(self):
        cookie_dict = cookies.SimpleCookie(self.headers['Cookie'])

        if 'sid' in cookie_dict:
            sid = cookie_dict['sid'].value

        if 'sid' not in cookie_dict or sid not in sessions:
            sid = secrets.token_urlsafe()  # generate some random token
            self.saved_headers = [('Set-Cookie', 'sid=' + sid)]
            sessions[sid] = {}  # the session is initially empty

        return sid

    
    def do_GET(self):
        sid = self.get_or_create_session()
        if 'username' in sessions[sid]:
            self.send_response_headers_and_body(authenticated_doc.format(username=sessions[sid]['username']))
        else:
            self.send_response_headers_and_body(form_doc)
            

    def do_POST(self):
        sid = self.get_or_create_session()
        content_length = self.headers['Content-Length']
        body = self.rfile.read(int(content_length))
        post_dict = parse_qs(str(body, 'UTF-8'))

        action = post_dict['action'][0]

        if action == 'login':
                             
            post_user = post_dict['user'][0]
            post_pass = post_dict['pass'][0]

            connection = sqlite3.connect(DATABASE_FILE)  # could also be replaced by a connection to a remote sql server, e.g., a mysql instance
            sql = f"SELECT username FROM users WHERE username = '{post_user}' AND password = '{post_pass}'"
            print (f"Executing SQL: {sql}")
            res = connection.execute(sql)
            entry = res.fetchone()
            if entry is None:
                self.send_response_headers_and_body(fail.format(message="Wrong username or password!"))
                return
            else:
                print ("Successful login!")
                sessions[sid]['username'] = post_user
                self.redirect('/')
                return

        else:
            sessions[sid] = {}
            self.send_response_headers_and_body(form_doc)
            return
                

    def send_response_headers_and_body(self, output):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        for header, value in self.saved_headers:  # we use saved_headers to store headers for this particular response in get_or_create_session
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(bytes(output, 'UTF-8'))

    def redirect(self, target):
        self.send_response(303)
        self.send_header('Location', target)
        self.end_headers()


# We extend the class MyHandler to define an admin interface. The
# extended class overwrites the base class so that we do not have to
# change anything in the surrounding code.
class MyHandler(MyHandler):
    admin_doc = '''
    <!doctype html>
    <html>
    <h1>SEC Intranet - Admin Area</h1>
    <a href='/'>Return to home</a>
    <table>{rows}</table>
    Never store passwords in plain text as we do in this example!
    <form method='post' action="/admin/reset">
    <input type="submit" value="RESET DATABASE" />
    </form>

    <form method='post' action="/admin/add">
    <input type="text" id="user_name" name="user_name" placeholder="name">
    <input type="text"  id="user_password" name="user_password" placeholder="password">
    <input type="submit" value="ADD USER" />
    </form>

    <style>
    table {{ border: 1px solid black; border-collapse: collapse; }}
    th, td {{ border: 1px solid black; padding: 3px; }}
    </style>
    </html>'''
    
    def do_GET(self):
        if self.path != '/admin':
            return super().do_GET()
        
        sid = self.get_or_create_session()

        if not 'username' in sessions[sid]:
            self.send_response_headers_and_body(fail.format(message="Not logged in! <a href='/'>Return to home</a>"))
            return

        username = sessions[sid]['username']
        
        connection = sqlite3.connect(DATABASE_FILE)

        sql = f"SELECT username FROM users WHERE username = '{username}' AND privileges = 'all'"
        print (f"Executing SQL: {sql}")
        res = connection.execute(sql)
        entry = res.fetchone()
        if entry is None:
            self.send_response_headers_and_body(fail.format(message="Not enough privileges! <a href='/'>Return to home</a>"))
            return

        
        res = connection.execute("SELECT id, username, password, signed_up, privileges FROM users");
        rows = '<tr> <th>id</th> <th>username</th> <th>password</th> <th>signed_up</th> <th>privileges</th> </tr>'
        for row in res:
            rows += f'<tr> <td>{row[0]}</td> <td>{row[1]}</td> <td>{row[2]}</td> <td>{row[3]}</td> <td>{row[4]}</td> </tr>'

        self.send_response_headers_and_body(self.admin_doc.format(rows=rows))

    def do_POST(self):
        print("Path:", self.path)
        if self.path == "/admin/add":

            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)

            form_data = { key.decode(): val[0].decode() for key, val in postvars.items() }

            name = form_data.get('user_name')
            password = form_data.get('user_password')

            print(f"New user: {name}/{password}")

            connection = sqlite3.connect(DATABASE_FILE)
            date_str = datetime.datetime.today().strftime('%Y-%m-%d')
            sql = f"INSERT INTO users VALUES ({randint(100,200)}, '{name}', '{password}', '{date_str}', 'user')"
            print (f"Executing SQL: {sql}")
            res = connection.execute(sql)
            connection.commit()
            print("res:", res)
            self.redirect('/admin')

        elif self.path == "/admin/reset":
            print("Reset database")
            reset_database()
            self.redirect('/admin')
        else:
            return super().do_POST()

        

        
if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    print ("Starting web server on http://localhost:8081/")
    print ("Admin interface at http://localhost:8081/admin")
    server.serve_forever()
