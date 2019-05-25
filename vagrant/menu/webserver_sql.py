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


def get_restaurants():
    """Query to list all restaurant ids and names."""
    return session.query(Restaurant.id, Restaurant.name).all()


def get_restaurant_name_from_id(idval):
    """Query to get restaurant name from its id."""
    return session.query(Restaurant).filter_by(id=idval).one()


def add_restaurant(newname):
    """Add a new restaurant to the table."""
    newrec = Restaurant(name=newname)
    session.add(newrec)
    session.commit()

def del_restaurant(idval):
    """Add a new restaurant to the table."""
    delrec = session.query(Restaurant).filter_by(id=idval).one()
    if delrec != []:
        session.delete(delrec)
        session.commit()

def upd_restaurant(idval, updname):
    """Update the restaurant name."""
    print(idval, updname)
    updrec = session.query(Restaurant).filter_by(id=idval).one()
    if updrec != []:
        updrec.name = updname
        session.add(updrec)
        session.commit()
        # print(updrec.name)


def main():
    """Main."""
    #print('start')
    # add_restaurant('AABS')
    rest_name = get_restaurant_name_from_id(3)
    # for rest_name in rest_names:
    print(rest_name.name)
    # session.rollback()


# use filterby to isolate a specific column in the table.
"""veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for vburger in veggieBurgers:
    print(vburger.id, vburger.price, vburger.restaurant.name)
"""
