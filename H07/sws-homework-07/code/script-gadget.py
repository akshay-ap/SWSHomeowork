#!/usr/bin/env python3

import sys
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    from html import escape
except ImportError:
    sys.exit('ERROR: It seems like you are not running Python 3. '
             'This script only works with Python 3!')


main_doc = '''
<!doctype html>
<html>
<head>

<script type="text/javascript" src="https://knockoutjs.com/downloads/knockout-3.4.2.js"></script>

</head>
<body>
<h1>SEC Air Travel</h1>
<p>
<a href="?data=classes">Classes</a> <a href="?data=routes">Routes</a>
</p>
<p>
    Choose:
    <select data-bind="options: d{data}, 
                       optionsCaption: 'Choose...',
                       optionsText: 'name',
                       value: chosenTicket"></select>
                       
    <button data-bind="enable: chosenTicket, 
                       click: resetTicket">Clear</button>
    </p>                   
    <p data-bind="with: chosenTicket">
        You have chosen <b data-bind="text: name"></b>
        ($<span data-bind="text: price"></span>)    
    </p>
    
    <script type="text/javascript">
        function TicketsViewModel() {{
            this.dclasses = [
                {{ name: "Economy", price: 199.95 }},
                {{ name: "Business", price: 449.22 }},
                {{ name: "First Class", price: 1199.99 }}
            ];
            this.droutes = [
                {{ name: "STR-LAX", price: 599.95 }},
                {{ name: "STR-FRA", price: 99.23 }},
                {{ name: "STR-LUX", price: 103.05 }}
            ];
            this.chosenTicket = ko.observable();
            this.resetTicket = function() {{ this.chosenTicket(null) }}
        }}
        ko.applyBindings(new TicketsViewModel(), document.getElementById("liveExample"));
    </script>	
</body></html>
'''




class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_dict = urlparse(self.path)  # parse URL string into dictionary
        get_dict = parse_qs(url_dict.query)  # select query string from URL dictionary

        self.send_response(200)
        self.send_header('Content-Type', 'text/html;charset=utf-8')

        self.end_headers()

        if 'data' in get_dict:
            data = get_dict['data'][0]
        else:
            data = 'classes'
            
        print("data", data)
        print("escaped", escape(data))
        output = main_doc.format(data=escape(data))
        self.wfile.write(bytes(output, 'UTF-8'))


if __name__ == '__main__':
    server = HTTPServer(('', 8081), MyHandler)
    print("Starting web server on http://localhost:8081/")
    server.serve_forever()
