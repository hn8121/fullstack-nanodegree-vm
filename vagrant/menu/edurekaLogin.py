"""Test file to run HTML Methods using Flask."""
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success/<name>/')
def success(name):
    """Greet name since login success."""
    return 'welcome %s' % name 

@app.route('/login', methods = ['POST', 'GET'])
def login():
    """Get login name and take action."""
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))
    else:
        # not updating via the form so display the name
        user = request.args.get('nm')
        return redirect(url_for('success', name = user))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)