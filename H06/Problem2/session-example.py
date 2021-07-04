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

    
login_form_doc = '''
<!doctype html>
<html><body>
{message}
<form method="post" action="/login">
    User: <input name="user">
    <br>
    Password: <input name="pass" type="password">
<br>
<input type="submit" value="go">
</form>
<small>Hint: Username alice, Password bob.
</body></html>
'''

logged_in_doc = '''
<!doctype html>
<html><body>
{message}
<br/>
<form method="post" action="/logout">
<input type="submit" value="Logout">
</form>
</body></html>'''

sessions = {}




class MyHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.close_connection = True

    
    def get_or_create_session(self):
        cookie_dict = cookies.SimpleCookie(self.headers['Cookie'])

        if 'sid' in cookie_dict:
            sid = cookie_dict['sid'].value

        if 'sid' not in cookie_dict or sid not in sessions:
            sid = secrets.token_urlsafe()  # generate some random token
            self.send_header('Set-Cookie', 'sid=' + sid)
            sessions[sid] = {}  # the session is initially empty
        return sid
    
    def do_GET(self):
        self.send_response(200)
        sid = self.get_or_create_session()
        self.send_header('Content-Type', 'text/html;charset=utf-8')
        self.end_headers()
        
        if 'username' in sessions[sid]:
            message = "Welcome! You are logged in as " + sessions[sid]['username']
            output = logged_in_doc.format(message=message)
        else:
            message = 'Not logged in.'
            output = login_form_doc.format(message=message)
            
        
        self.wfile.write(bytes(output, 'UTF-8'))

    def do_POST(self):
        if self.path == "/login":
            content_length = self.headers['Content-Length']
            body = self.rfile.read(int(content_length))
            qs_dict = parse_qs(str(body, 'UTF-8'))

            if qs_dict['user'][0] == 'alice' and qs_dict['pass'][0] == 'bob':
                # login was successful, redirect user to first page.
                self.send_response(303)  # redirection status code "See Other"
                sid = self.get_or_create_session()
                self.send_header('Content-Type', 'text/html;charset=utf-8')
                sessions[sid]['username'] = 'alice'
                self.send_header('Location', '/')
                self.end_headers()
            else:
                # wrong credentials, show form again
                self.send_response(200) 
                self.send_header('Content-Type', 'text/html;charset=utf-8')
                self.end_headers()
                message = 'Wrong credentials.'
                output = login_form_doc.format(message=message)            
                self.wfile.write(bytes(output, 'UTF-8'))

        elif self.path == "/logout":

            cookie_dict = cookies.SimpleCookie(self.headers['Cookie'])
            if 'sid' in cookie_dict:
                sid = cookie_dict['sid'].value
                sessions.pop(sid, None)


            self.send_response(303) 
            sid = self.get_or_create_session()
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.send_header('Location', '/')
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    server.serve_forever()
