#!usr/bin/env python3
"""###################################################
# File: loganalysis.py
# What: Contains the python code to produce the log
#       analysis reports webpage
# Author: Howard Nathanson
# Updated: 05/10/19 - Initial Version
###################################################"""

from loganalysisdb import (most_pop_articles, most_pop_authors,
                           threshold_err_count)


# most popular articles
article_heading = "Three Most Popular Articles of All Time"
article_report = most_pop_articles()

print(article_heading)
for i in article_report:
    print("\"%s\" - %i views" % (i[0], i[1]))
print("")

# most popular authors
author_heading = "Most Popular Article Authors of All Time"
author_report = most_pop_authors()

print(author_heading)
for i in author_report:
    print("\"%s\" - %i views" % (i[0], i[1]))
print("")

# errant threshold
threshold_heading = "Days With More Than One-Percent Errant Requests"
threshold_report = threshold_err_count()

print(threshold_heading)
for i in threshold_report:
    print("%s - %s errors" % (i[0], i[1]))
print("")

print("END OF REPORTS")
