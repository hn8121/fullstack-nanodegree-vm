#!usr/bin/env python3
"""Playground for testing JSON."""

import json
a = [1, 2, 3, 5, 9, 7]

for i in a:
    print(i)
print('======')

 #__iter__()  #get the iterator
 #__next__()  #gets the next iterator

a = [1, 5]
it = iter(a)  #used to get the iterator object, can use to call all alues in collections
b = next(it)  #get first item in list
print(b)
b = next(it)  #get next item in list
print(b)
b = next(it)  #out of iterables, should throw "StopIteration"
print(b)

# can loop over iterations
