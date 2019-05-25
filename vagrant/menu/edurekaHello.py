"""Test file to render an HTML template in Flask."""
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/hello/<user>')
def hello_name(user):
    """Render the HTML from the template identified as the first parm."""
    return render_template('edurekaHello.html', name = user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)