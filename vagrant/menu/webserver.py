#!/usr/bin/env python
"""Program to emulate web server for menu project."""
import cgi


#from http.server import BaseHTTPRequestHandler, HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import webserver_sql ## contains my queries

class WebServerHandler(BaseHTTPRequestHandler):
    """Class to handle the web requests."""

    def do_GET(self):
        """GET Requests."""
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "      action='/hello'>"
                output += "   <h2>What would you like me to say?</h2>"
                output += "   <input name='message' type='text'>"
                output += "   <input type='submit' value='Submit'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Restuarants</h1>"
                
                ## link to create a new restaurant
                output += "<a href='/restaurant/new'>Make a New Restaurant</a>"
                output += "<p>"

                rest_names = webserver_sql.get_restaurant_names()
                for rest_name in rest_names:
                    output += "%s<br>" % rest_name.name
                    output += "<a href='#'>edit</a><br>"
                    output += "<a href='#'>delete</a><br>"
                    output += "<br>"                    
                
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "      action='/restaurant/new'>"
                output += "   <input name='restaurant_name' type='text' "
                output += "       placeholder='New restaurant name'>"
                output += "   <input type='submit' value='Create'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        """POST Requests."""
        try:
            
            if self.path.endswith("/hello"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
               
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                    output = ""
                    output += "<html><body>"
                    output += "<h2>Okay, how about this: </h2>"
                    output += "<h1>%s</h1>" % messagecontent[0]

                    output += "<form method='POST' enctype='multipart/form-data' "
                    output += "      action='/hello'>"
                    output += "   <h2>What would you like me to say?</h2>"
                    output += "   <input name='message' type='text'>"
                    output += "   <input type='submit' value='Submit'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    
                    print(output)

            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                    
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')

                    webserver_sql.add_restaurant(messagecontent[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
        except:
            print('exception hit')
            pass


def main():
    """Start here."""
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
