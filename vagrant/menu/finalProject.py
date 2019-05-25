#!usr/bin/env python
"""File finalProject.py."""
######################################################
# File: finalProject.py
# What: Contains the python code to produce the 
#       Rstaurant and Menu website using Flask
# Author: Howard Nathanson
# Updated: 05/22/19 - Initial Version
######################################################

import cgi
import webserver_sql  # contains my queries

# from http.server import BaseHTTPRequestHandler, HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from flask import Flask, redirect, request, url_for, render_template
from itertools import groupby     #group items by a key
from operator import itemgetter   #sot dictionary
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'id':'1'}


@app.route('/', methods=['GET'])
@app.route('/restaurants/', methods=['GET'])
def showRestaurants():
  """Show a list of all restauarants."""
  return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
  """Create a new restaurant method."""
  return render_template('newRestaurant.html')

@app.route('/restaurant/<int:rid>/edit/', methods=['GET','POST'])
def editRestaurant(rid):
  """Edit a restaurant name method."""
  # This page be for editing restaurant <rid>
  return render_template('editRestaurant.html', restaurant = restaurants[rid-1])

@app.route('/restaurant/<int:rid>/delete/', methods=['GET','POST'])
def deleteRestaurant(rid):
  """Delect a restuarant method."""
  # This page will be for deleting restaurant <rid>
  return render_template('deleteRestaurant.html', restaurant = restaurants[rid-1])

@app.route('/restaurant/<int:rid>/', methods=['GET'])
@app.route('/restaurant/<int:rid>/menu/', methods=['GET'])
def showMenu(rid):
  """Display the restuarant menu method."""
  # group items by course
  sort_order = ['Appetizer','Entree','Dessert','Beverage']
  sorted_menu = [i for j in sort_order  
      for i in filter(lambda k: k['course'] == j, items)]
  #print "%s" % str(res) 
  #sorted_menu = sorted(res, key=lambda x: x['course'])
  #items_by_course = groupby(sorted_menu, lambda x: x['course'])
  #for course_name, _ in items_by_course:
  #  print "%s" % (course_name)
  #  for name in names:
  #      print "%s - %s" % (name[1], courses)
  return render_template('menus.html', restaurant = restaurants[rid-1], menu = sorted_menu)

@app.route('/restaurant/<int:rid>/menu/new/', methods=['GET','POST'])
def newMenuItem(rid):
  """Create a new menu item method."""
  return render_template('newMenuItem.html')

@app.route('/restaurant/<int:rid>/menu/<int:mid>/edit/', methods=['GET','POST'])
def editMenuItem(rid, mid):
  """Edit a restuarant menu method."""
  # This page is for editing menu item <mid> for restaurant <rid>
  return render_template('editMenuItem.html', item = item)

@app.route('/restaurant/<int:rid>/menu/<int:mid>/delete/', methods=['GET','POST'])
def deleteMenuItem(rid, mid):
  """Edit a restuarant menu method."""
  # This page is for deleting menu item <mid> for restaurant <rid>
  return render_template('deleteMenuItem.html', item = item)

@app.route('/parm/<float:floatparm>/')
def hello_floatparm(floatparm):
  """Run the function with 1 floating point parameter - floatparm."""
  # the parameter floatparm is the last part of the URL string
  return 'Hello float paramter: %f' % floatparm
  
@app.route('/parm/<int:intparm>/')
def hello_intparm(intparm):
  """Run the function with 1 integer parameter - intparm."""
  # the parameter parm1 is the last part of the URL string
  return 'Hello integer paramter: %i' % intparm
  
@app.route('/parm/<parm1>')
def hello_parm(parm1):
  """Run the function with 1 parameter - parm1."""
  # the parameter parm1 is the last part of the URL string
  return 'Hello paramter: %s' % parm1

### the next set of functions checks the parameter and redirects accordngly
### both functions are run from the same URL; however, the hello_admin
### can only ebe run if the name parameter = 'admin' or the page was 
### already rendered. 
@app.route('/user/<name>/')
def hello_user(name):
  """Check the name for admin or not, redirect accordingly."""
  if name == 'admin':
    # call special hello_admin function
    return redirect(url_for('hello_admin'))
  else:
    # use existing function above to say hello
    return redirect(url_for('hello_parm', parm1 = name))
def hello_admin():
  """Greet the admin user."""
  return ('Hello admin')


  
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)