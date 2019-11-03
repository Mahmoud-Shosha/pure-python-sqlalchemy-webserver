#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# connect to DB and create a session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list = '<div>'
                for r in restaurants:
                    # if type(r.name)!='str':
                    #     session.delete(r)
                    #     session.commit()
                    list += '<h3>' + r.name + '</h3>'
                    list += "<a href='/restaurants/{}/edit'>Edit</a><br />".format(r.id)
                    list += "<a href='/restaurants/{}/delete'>Delete</a><br /><br />".format(r.id)
                list += '</div>'
                output = "<html><body><h1><a href='/restaurants/new'>Make a New Restaurant Here !</a></h1>"
                output += list
                output += '</body></html>'
                self.wfile.write(output.encode('utf-8'))
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Make a New Restaurant</h2>"
                output += """
                             <form method='POST' action='/restaurants/new'' enctype='multipart/form-data'>
                                <input name='newRestaurantName' type='text'>
                                <input type='submit' value='Create'>
                             </form>
                """
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                return
            if self.path.endswith('/edit'):
                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id=id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>" + restaurant.name + "</h2>"
                output += """
                             <form method='POST' action='/restaurants/{}/edit'' enctype='multipart/form-data'>
                                <input name='restaurantName' value='{}' type='text'>
                                <input type='submit' value='Update'>
                             </form>
                """.format(id, restaurant.name)
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                return
            if self.path.endswith('/delete'):
                id = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id=id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h2>Are you sure you want to delete {} ?</h2>".format(restaurant.name)
                output += """
                             <form method='POST' action='/restaurants/{}/delete'' enctype='multipart/form-data'>
                                <input type='submit' value='Delete'>
                             </form>
                """.format(id)
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                return
        except IOError:
            self.send_error(404, 'File not found {}'.format(self.path))

    def do_POST(self):
        # try:
        if self.path.endswith('/restaurants/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type', ''))
            pdict['boundary'] = pdict['boundary'].encode()
            if ctype=='multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict) # DEALS with bytes
                messagecontent = fields.get('newRestaurantName')[0].decode()
            new_restaurant = Restaurant(name=messagecontent)
            session.add(new_restaurant)
            session.commit()
            self.send_response(301)
            self.send_header('location', '/restaurants')
            self.end_headers()
            return
        if self.path.endswith('/edit'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type', ''))
            pdict['boundary'] = pdict['boundary'].encode()
            if ctype=='multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict) # DEALS with bytes
                messagecontent = fields.get('restaurantName')[0].decode()
            id = self.path.split('/')[2]
            restaurant = session.query(Restaurant).filter_by(id=id).one()
            restaurant.name = messagecontent
            session.add(restaurant)
            session.commit()
            self.send_response(301)
            self.send_header('location', '/restaurants')
            self.end_headers()
            return
        if self.path.endswith('/delete'):
            id = self.path.split('/')[2]
            restaurant = session.query(Restaurant).filter_by(id=id).one()
            session.delete(restaurant)
            session.commit()
            self.send_response(301)
            self.send_header('location', '/restaurants')
            self.end_headers()
            return
        # except:
            # pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("The server is running on port {}".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C entered, stopping the web server ...')
        server.socket.close()


if __name__ == '__main__':
    main()
