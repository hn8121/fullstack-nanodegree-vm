#!usr/bin/env python
"""File edureka_torial.py."""
######################################################
# File: edureka_tutorial.py
# What: Contains the python code to produce the 
#       FLask test functions
# Author: Howard Nathanson
# Updated: 05/22/19 - Initial Version
######################################################

from flask import Flask, redirect, request, url_for
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def hello_world():
  """Run the main method."""
  return 'Hello World.'

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