#!usr/bin/env python
"""Contains all sqls for menu program."""

from sqlalchemy import create_engine, inspect, func
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



def get_restaurant_names():
    """Query to list all restaurant names."""
    return session.query(Restaurant).distinct(Restaurant.name).all()
    
def add_restaurant(newname):
    """Add a new restaurant to the table."""
    newrec = Restaurant(name=newname)
    session.add(newrec)
    session.commit()
    #print(newrec.name) 

def main():
    """Main."""
    #print('start')
    #add_restaurant('AABS')
    #rest_names = get_restaurant_names()
    #for rest_name in rest_names:
    #    print(rest_name.name)
    #session.rollback()
    

### use filterby to isolate a specific column in the table.
"""veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for vburger in veggieBurgers:
    print(vburger.id, vburger.price, vburger.restaurant.name)
"""
