#!usr/bin/env python3
"""###################################################
# File: analysisdb.py
# What: Contains the SQL to pull report data
# Author: Howard Nathanson
# Report Functions
# 	most_pop_article3(): returns the 3 most popular
#           articles and the number of views of each.
#	most_pop_authors(): returns the most popular
#           authors and the number of views of each.
#	threshold_err_count(): returns the days when
#           the number of errant requests above a
#           threshold amount occured.
#
# Updated: 05/10/19 - Initial Version
###################################################"""

import psycopg2


def most_pop_articles():
    """ Return the 3 most read articles, most read first."""
    connection = psycopg2.connect("dbname=news")
    cursor = connection.cursor()

    select_stmt = """SELECT ar.title, COUNT(l.path)
                         FROM log l
                         JOIN articles ar ON l.path LIKE '%'||ar.slug
                      GROUP BY ar.title
                      ORDER BY COUNT(l.path) DESC
                      LIMIT 3"""

    cursor.execute(select_stmt)
    record_set = cursor.fetchall()
    connection.close()
    return record_set
# end most_pop_articles


def most_pop_authors():
    """ Return the most popular authors, most popular first."""
    connection = psycopg2.connect("dbname=news")
    cursor = connection.cursor()

    select_stmt = """SELECT au.name, COUNT(l.path) AS total
                         FROM log l
                       JOIN articles ar ON l.path LIKE '%'||ar.slug
                       JOIN authors au ON au.id = ar.author
                      GROUP BY au.name
                      ORDER BY COUNT(l.path) DESC"""
    cursor.execute(select_stmt)
    record_set = cursor.fetchall()
    connection.close()
    return record_set
# end most_pop_authors


def threshold_err_count():
    """ Return the days where over 1% of requests were errant."""
    connection = psycopg2.connect("dbname=news")
    cursor = connection.cursor()

    select_stmt = """WITH totcounts AS (
                              SELECT to_char(time, 'Month DD, YYYY') AS day,
                                      COUNT(*) AS total
                                FROM log
                                GROUP BY day
                              ),
                            errcounts AS (
                               SELECT to_char(time, 'Month DD, YYYY') AS day,
                                      COUNT(*) AS total
                                 FROM log
                                GROUP BY day, status
                               HAVING LEFT(status,3)::INTEGER
                                                   BETWEEN 400 AND 499
                            )
                    SELECT t.day,
                           to_char(e.total::FLOAT * 100 /
                                         t.total::FLOAT, '999D0%')  AS pcterr
                      FROM totcounts t
                      JOIN errcounts e ON t.day = e.day
                     WHERE e.total::FLOAT / t.total::FLOAT > 0.01"""

    cursor.execute(select_stmt)
    record_set = cursor.fetchall()
    connection.close()
    return record_set
# end threshold_err_count
