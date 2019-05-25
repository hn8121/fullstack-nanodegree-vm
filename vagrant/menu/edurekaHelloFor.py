"""Test file to render an HTML template in Flask."""
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/result')
def result():
    """Render the HTML from the template identified as the first parm."""
    #dict is the dictionary of course,grade tuples
    dict = {'phy':50, 'che':60, 'math':70}
    return render_template('edurekaHelloFor.html', result = dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)