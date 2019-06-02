#!usr/bin/env python3
"""Playground for testing JSON."""

import json

# test library
a = {
    'name': 'max',
    'age':22,
    'marks' : [90, 50, 80, 40],
    'pass' : True,
    'object': {
        'color' : ('red','blue')
    }
}

# convert python values to json
# takes dictionary and majority of collections and data types, not sets
print(json.dumps(a))
print(json.dumps({"age": 22, "pass": True, "name": "max", "marks": [90, 50, 80, 40]}))
print(json.dumps(["1,","2"]))
print(json.dumps(("tup1","tup2")))
print(json.dumps("text"))
print(json.dumps(100))
print(json.dumps(True))
print(json.dumps(None))

# can indent and replace something with something else.
print(json.dumps("indent by 4, neat", indent=4, separators=(',', '=')))

#can sort by alpha order of key values
print(json.dumps(a))
print(json.dumps(a, sort_keys=True))

#can output to a file
with open ('out.json', 'w') as outf:
    outf.write(json.dumps(a, sort_keys=True))

#read from a file
with open ('out.json', 'r') as inf:
    json_str = inf.read()
    print(type(inf.read()))  #show this is a string value
    # convert string into a json value
    json_value = json.loads(json_str)
    #now a dictionary
    #get the name value
    print(json_value['name'])
