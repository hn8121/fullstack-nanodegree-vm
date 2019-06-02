#!usr/bin/env python3
"""Create an exmaple iterator class."""

#must implement __iter__() and __next__()

import json

class ListIterator:

    def __init__(self, list):
        self.__list = list
        self.__index = -1

    ## give iterator
    def __iter__(self):
        return self

    def __next__(self):
        self.__index += 1
        if self.__index >= len(self.__list):
            raise StopIteration
        return(self.__list[self.__index])  #return next item in the list

# create a list for testing
a = [1, 4, 7, 4, 7, 0, 12]

#create a list of ListItertor to show how to iterate over it
myList = ListIterator(a)
it = iter(myList)

# if you next 1 too many times, an "index_out_of_range" will be thrown.
# a StopIteration will be thrown now due to raise in __next__ method
i = 0
while i < len(a):
    print(next(it))
    i += 1
print('done')

myList = ListIterator(a)  #reset the list iterator
it = iter(myList)         #reset the iterator list
# the loop will iterate over the items
for i in it:
    print(i)
    
print ("done")
print(next(it)) # will throw exception
