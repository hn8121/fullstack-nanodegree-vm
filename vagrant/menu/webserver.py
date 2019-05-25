#!/usr/bin/env python
"""Program to emulate web server for menu project."""
import cgi

# from http.server import BaseHTTPRequestHandler, HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import webserver_sql  # contains my queries


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

                # link to create a new restaurant
                output += "<a href='/restaurant/new'>Make a New Restaurant</a>"
                output += "<p>"

                rest_names = webserver_sql.get_restaurants()
                for rest_name in rest_names:

                    # get the id number for each name - part of edit href
                    output += "%s<br>" % rest_name.name
                    output += "<a href='/restaurant/%s/edit'>edit</a><br>" \
                                                             % rest_name.id
                    output += "<a href='/restaurant/%s/delete'>delete</a><br>" \
                                                             % rest_name.id
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

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # get id from URL path
                # split the path. The id is the 2nd part from the right
                startstr, idval, endstr = self.path.rsplit('/', 2)

                # get the restaurant name from the id value
                rname = webserver_sql.get_restaurant_name_from_id(idval)

                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>" % rname.name
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "      action='/restaurant/edit'>"
                output += "   <input name='restaurant_id' type='hidden' "
                output += "       value='%s'>" % idval
                output += "   <input name='restaurant_name' type='text' "
                output += "       placeholder='%s' id='%s'>" \
                                                % (rname.name, idval)
                output += "   <input type='submit' value='Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # get id from URL path
                # split the path. The id is the 2nd part from the right
                startstr, idval, endstr = self.path.rsplit('/', 2)

                # get the restaurant name from the id value
                rname = webserver_sql.get_restaurant_name_from_id(idval)

                output = ""
                output += "<html><body>"
                output += "<h1>Confirm deletion of '%s'</h1>" % rname.name
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "      action='/restaurant/delete'>"
                output += "   <input name='restaurant_id' type='hidden' "
                output += "       value='%s'>" % idval
                output += "   <input type='submit' value='Confirm'>"
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

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    idcontent = fields.get('restaurant_id')

                    # delete the restaurant in the database
                    webserver_sql.del_restaurant(idcontent[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')
                    idcontent = fields.get('restaurant_id')

                    # update the restaurant name in the database
                    webserver_sql.upd_restaurant(idcontent[0], messagecontent[0])
                    #print(mesagecontent[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

            if self.path.endswith("/restaurant/new"):
                ctype, pdict=cgi.parse_header(
                    self.headers.getheader('content-type'))

                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent=fields.get('restaurant_name')

                    webserver_sql.add_restaurant(messagecontent[0])
                    print(messagecontent[0])
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
        port=8080
        server=HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
