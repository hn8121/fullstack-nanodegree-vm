from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_db_setup import Base, Owner, Team, Player

engine = create_engine('sqlite:///catalog.db')
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


# Create dummy owners
owner1 = Owner(name="Owen Knerr", email="ownerknerr@udacity.com",
               picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(owner1)
session.commit()

owner2 = Owner(name="Hank Nathy", email="hanknathyis@gmail.com",
               picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(owner2)
session.commit()


# Team for Wily Cayotees
team1 = Team(owner_id=1, name="Wily Cayotees", city="Phoenix")

session.add(team1)
session.commit()

player1 = Player(owner_id=1, team_id=1, name="Jimmy Ranger", position="offense",
                 uniform_num="5", salary="$50,000")

session.add(player1)
session.commit()


player2 = Player(owner_id=1, team_id=1, name="Bill Rustle", position="offense",
                 uniform_num="9", salary="$70,000")

session.add(player2)
session.commit()


player3 = Player(owner_id=1, team_id=1, name="Waylan Gitner", position="defense",
                 uniform_num="33", salary="$60,000")

session.add(player3)
session.commit()


player4 = Player(owner_id=1, team_id=1, name="Nilsa Flogla", position="defense",
                 uniform_num="33", salary="$83,000")

session.add(player4)
session.commit()


# Team for Know Nothings
team2 = Team(owner_id=2, name="Know Nothings", city="Shelby")

session.add(team2)
session.commit()

player1 = Player(owner_id=2, team_id=2, name="Stammer Quartler", position="offense",
                 uniform_num="2", salary="$150,000")

session.add(player1)
session.commit()


player2 = Player(owner_id=2, team_id=2, name="Kisplin Qualifin", position="defense",
                 uniform_num="27", salary="$50,000")

session.add(player2)
session.commit()


player3 = Player(owner_id=2, team_id=2, name="Ollie Catalpa", position="defense",
                 uniform_num="33", salary="$65,000")

session.add(player3)
session.commit()


# Team for Rolling Thunder
team3 = Team(owner_id=1, name="Rolling Thunder", city="Lincoln")

session.add(team3)
session.commit()

player1 = Player(owner_id=1, team_id=3, name="Len Place", position="defense",
                 uniform_num="32", salary="$80,000")

session.add(player1)
session.commit()


player2 = Player(owner_id=1, team_id=3, name="Harold Wilson", position="defense",
                 uniform_num="31", salary="$55,000")

session.add(player2)
session.commit()


player3 = Player(owner_id=1, team_id=3, name="Mark Branson", position="defense",
                 uniform_num="34", salary="$65,000")

session.add(player3)
session.commit()


player4 = Player(owner_id=1, team_id=3, name="Grim Plyworld", position="defense",
                 uniform_num="47", salary="$72,000")

session.add(player4)
session.commit()

# Team for Flash Drivers
team4 = Team(owner_id=2, name="Flash Drivers", city="East London")

session.add(team4)
session.commit()

player1 = Player(owner_id=2, team_id=4, name="Carimo Grettle", position="offense",
                 uniform_num="3", salary="$120,000")

session.add(player1)
session.commit()


player2 = Player(owner_id=2, team_id=4, name="Terrence Dill", position="defense",
                 uniform_num="48", salary="$59,000")

session.add(player2)
session.commit()


print("added owners, teams, and players!")
