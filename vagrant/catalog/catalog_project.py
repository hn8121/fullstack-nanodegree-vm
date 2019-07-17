#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, Owner, Team, Player

# Imports to create a new random session value each time a user logs into the site
from flask import session as login_session
import random
import string

# imports to interact with Google+ authorization and deal with responses
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
# reuses existing Google API application name
APPLICATION_NAME = "Restaurant Menu Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    print("access token received %s " % access_token)

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print("url = %s" % url)
    print("result = %s" % result)

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.3/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0]
    token = token.split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['owner_name'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get owner picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if owner exists
    owner_id = getOwnerID(login_session['email'])
    if not owner_id:
        owner_id = createOwner(login_session)
    login_session['user_id'] = owner_id

    print("FB-state %s" % login_session['state'])
    print("FB-user_id %s" % login_session['user_id'])
    print("FB-owner %s" % login_session['owner_name'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['owner_name']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['owner_name'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out, result %s" % result


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response = make_response(json.dumps(login_session.get('owner_name')),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['provider'] = 'google'

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['owner_name'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # if owner does not exist, create a new owner record
    owner_id = getOwnerID(email=data['email'])
    if not owner_id:
        # insert record into database
        owner_id = createOwner(login_session)
    login_session['user_id'] = owner_id

    #print('In gconnect access token is    %s\n' % login_session['access_token'])
    output = ''
    output += '<h1>Welcome, ' + str(login_session['gplus_id'])
    output += login_session['owner_name']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged as %s" % login_session['owner_name'])
    print("done!")
    return output

# Owner Helper Functions


def createOwner(login_session):
    newOwner = Owner(name=login_session['owner_name'], email=login_session['email'],
                     picture=login_session['picture'])
    session.add(newOwner)
    session.commit()
    owner = session.query(Owner).filter_by(
        email=login_session['email']).one()
    return owner.id


def getOwnerInfo(owner_id):
    owner = session.query(Owner).filter_by(id=owner_id).one()
    return owner


def getOwnerID(email):
    try:
        owner = session.query(Owner).filter_by(email=email).one()
        return owner.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #print('In gdisconnect access token is %s\n' % login_session['access_token'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('gisconnect status = %s' % result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['owner_name']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Team Information
@app.route('/league/owner/JSON')
def onwerJSON():
    owners = session.query(Owner).all()
    return jsonify(Owners=[r.serialize for r in owners])


@app.route('/team/<int:team_id>/player/JSON')
def teamJSON(team_id):
    #team = session.query(Team).filter_by(id=team_id).one()
    players = session.query(Player).filter_by(
        team_id=team_id).all()
    return jsonify(Team=[i.serialize for i in players])


@app.route('/team/<int:team_id>/player/<int:player_id>/JSON')
def teamPlayerJSON(team_id, player_id):
    player = session.query(Player).filter_by(
        id=player_id, team_id=team_id).one()
    return jsonify(Player=player.serialize)


@app.route('/team/JSON')
def teamsJSON():
    teams = session.query(Team).all()
    return jsonify(Teams=[r.serialize for r in teams])


# Show all teams in the leaue
@app.route('/')
@app.route('/league/')
def showLeague():
    teams = session.query(Team).order_by(asc(Team.name))
    if 'owner_name' not in login_session:
        return render_template('publicleague.html', teams=teams)
    else:
        return render_template('league.html', teams=teams)

# Create a new team
@app.route('/team/new/', methods=['GET', 'POST'])
def newTeam():
    if 'owner_name' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        print("here - %s" % login_session['user_id'])
        newTeam = Team(owner_id=login_session['user_id'],
                       name=request.form['name'],
                       city=request.form['city'])
        session.add(newTeam)
        flash('New Team %s %s Successfully Created' %
              (newTeam.city, newTeam.name))
        session.commit()
        return redirect(url_for('showLeague'))
    else:
        return render_template('newTeam.html')

# Edit a team
@app.route('/team/<int:team_id>/edit/', methods=['GET', 'POST'])
def editTeam(team_id):
    if 'owner_name' not in login_session:
        return redirect('/login')
    editedTeam = session.query(
        Team).filter_by(id=team_id).one()

    # do not allow non-owner access to the page
    if editedTeam.owner_id != login_session['user_id']:
        # return "<script>function myFunction() {alert('You are not authorized to edit this team. Please create your own team in order to edit.');}</script><body onload='myFunction()'>"
        return redirect('/league')

    if request.method == 'POST':
        if request.form['name']:
            editedTeam.name = request.form['name']
            editedTeam.city = request.form['city']
            flash('Team Successfully Edited: %s %s' %
                  (editedTeam.city, editedTeam.name))
            return redirect(url_for('showLeague'))
    else:
        return render_template('editTeam.html', team=editedTeam)


# Delete a team
@app.route('/team/<int:team_id>/delete/', methods=['GET', 'POST'])
def deleteTeam(team_id):
    if 'owner_name' not in login_session:
        return redirect('/login')

    teamToDelete = session.query(Team).filter_by(id=team_id).one()

    # do not allow non-owner access to the page
    if teamToDelete.owner_id != login_session['user_id']:
        # return "<script>function myFunction() {alert('You are not authorized to delete this team. Please create your own team in order to delete.');}</script><body onload='myFunction()'>"
        return redirect('/league')

    if request.method == 'POST':
        # delete any team players if exist
        numDel = session.query(Player).filter_by(
            team_id=teamToDelete.id).delete()
        print('Deleted %d players' % numDel)

        # delete team
        session.delete(teamToDelete)

        flash('%s Successfully Deleted' % teamToDelete.name)
        session.commit()
        return redirect(url_for('showLeague'))
    else:
        return render_template('deleteTeam.html', team=teamToDelete)

# Show a team's players
@app.route('/league/<int:team_id>/')
@app.route('/league/<int:team_id>/team/')
def showTeam(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    players = session.query(Player).filter_by(
        team_id=team_id).all()
    owner = getOwnerInfo(team.owner_id)
    print("team owner id: %s" % team.owner_id)
    print("team owner pix: %s" % owner.picture)
    # check if user is owner of the team
    if 'owner_name' not in login_session or owner.id != login_session['user_id']:
        return render_template('publicteam.html', players=players, team=team, owner=owner)
    else:
        return render_template('team.html', players=players, team=team, owner=owner)


# Create a new player
@app.route('/team/<int:team_id>/player/new/', methods=['GET', 'POST'])
def newPlayer(team_id):
    if 'owner_name' not in login_session:
        return redirect('/login')

    team = session.query(Team).filter_by(id=team_id).one()
    # do not allow non-owner access to the page
    if team.owner_id != login_session['user_id']:
        # return "<script>function myFunction() {alert('You are not authorized to add players to this team. Please create your own team in order to add players.');}</script><body onload='myFunction()'>"
        return redirect('/league')

    if request.method == 'POST':
        newPlayer = Player(name=request.form['name'], uniform_num=request.form['uniform_num'],
                           position=request.form['position'], salary=request.form['salary'],
                           team_id=team_id)
        session.add(newPlayer)
        session.commit()
        flash('New Player %s Successfully Created' % (newPlayer.name))
        return redirect(url_for('showTeam', team_id=team_id))
    else:
        return render_template('newPlayer.html', team_id=team_id)

# Edit a player
@app.route('/team/<int:team_id>/player/<int:player_id>/edit', methods=['GET', 'POST'])
def editPlayer(team_id, player_id):
    if 'owner_name' not in login_session:
        return redirect('/login')
    editedPlayer = session.query(Player).filter_by(id=player_id).one()
    team = session.query(Team).filter_by(id=team_id).one()

    # do not allow non-owner access to the page
    if team.owner_id != login_session['user_id']:
        # return "<script>function myFunction() {alert('You are not authorized to edit players on this team. Please create your own team in order to edit players.');}</script><body onload='myFunction()'>"
        return redirect('/league')

    if request.method == 'POST':
        if request.form['name']:
            editedPlayer.name = request.form['name']
        if request.form['uniform_num']:
            editedPlayer.uniform_num = request.form['uniform_num']
        if request.form['position']:
            editedPlayer.position = request.form['position']
        if request.form['salary']:
            editedPlayer.salary = request.form['salary']

        session.add(editedPlayer)
        session.commit()
        flash('Player Successfully Edited')
        return redirect(url_for('showTeam', team_id=team_id))
    else:
        return render_template('editPlayer.html', team_id=team_id, player_id=player_id, player=editedPlayer)


# Delete a player
@app.route('/team/<int:team_id>/player/<int:player_id>/delete', methods=['GET', 'POST'])
def deletePlayer(team_id, player_id):
    if 'owner_name' not in login_session:
        return redirect('/login')
    team = session.query(Team).filter_by(id=team_id).one()

    # do not allow non-owner access to the page
    if team.owner_id != login_session['user_id']:
        # return "<script>function myFunction() {alert('You are not authorized to delete players on this team. Please create your own team in order to delete players.');}</script><body onload='myFunction()'>"
        return redirect('/league')

    playerToDelete = session.query(Player).filter_by(id=player_id).one()
    if request.method == 'POST':
        session.delete(playerToDelete)
        session.commit()
        flash('Player Successfully Deleted')
        return redirect(url_for('showTeam', team_id=team_id))
    else:
        return render_template('deletePlayer.html', team_id=team_id, player=playerToDelete)

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    print("disconnect-state %s" % login_session['state'])
    print("disconnect-user_id %s" % login_session['user_id'])
    print("disconnect-owner %s" % login_session['owner_name'])
    print("disconnect-provider %s" % login_session['provider'])
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            del login_session['owner_name']
            del login_session['email']
            del login_session['picture']
            del login_session['user_id']
            del login_session['provider']
        flash("You have successfully been logged out.")
    else:
        flash("You were not logged in")
    return redirect(url_for('showLeague'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=8000, threaded=False)
