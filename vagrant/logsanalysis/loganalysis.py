#!usr/bin/env python3
######################################################
# File: analysis.py
# What: Contains the python code to produce the log
#       analysis reports webpage
# Author: Howard Nathanson
# Updated: 05/10/19 - Initial Version
######################################################

from flask import Flask, redirect, request, url_for
from loganalysisdb import (most_pop_articles, most_pop_authors,
                           threshold_err_count)

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis Reports</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>DAILY LOG REPORTS</h1>
    <!-- report content will go here -->
    <div>%s</div>
    
  </body>
</html>
'''

# HTML template for reports
ARTICLERPT = '''\
    <div>"%s" - %s views</div>
'''

AUTHORRPT = '''\
    <div>"%s" - %s views</div>
'''

THRESHOLDRPT = '''\
    <div>%s - %s errors</div>
'''

@app.route('/', methods=['GET'])
def main():
    '''Main page of the log reports.'''
    article_heading = "<strong><u>Three Most Popular Articles of All Time</u></strong>"
    article_report = "".join(ARTICLERPT % (text, int) for text, int in most_pop_articles())
    author_heading = "<strong><u>Most Popular Article Authors of All Time</u></strong>"
    author_report = "".join(AUTHORRPT % (text, int) for text, int in most_pop_authors())
    threshold_heading = "<strong><u>Days With More Than One-Percent Errant Requests</u></strong>"
    threshold_report = "".join(THRESHOLDRPT % (text, float) for text, float in threshold_err_count())
    return_str = HTML_WRAP % article_heading + article_report + "<br>"
    return_str = return_str + author_heading + author_report + "<br>"
    return_str = return_str + threshold_heading + threshold_report
    return return_str

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
