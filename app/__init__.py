import os
import random
import uuid
import pandas as pd
import requests
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, request, render_template, g, redirect, Response, flash, session, jsonify
from datetime import datetime, date, time

from .forms.login import LoginForm

from .models.user import Representative, Citizen
from .models.comment import Comment


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config['SECRET_KEY'] = "key"

login_manager = LoginManager()
# login_manager.init_app(app)

DATABASEURI = "postgresql://cfi2103:6814@35.227.79.146/proj1part2"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    print(e)
    pass

@app.route('/')
def index():
  return render_template("index.html", form=LoginForm())

@app.route('/u/<uid>')
def user(uid):
  return 'user'

@app.route('/map')
def map():
  return render_template("map.html")

@app.route('/houseinfo')
def houseinfo():
  if 'uid' in session:
    current_user_uid = session['uid']

    city_q = text("""
      SELECT U.zipcode, Z.city_name, Z.avg_price, H.score, H.value
      FROM Users U, Zipcodes Z, Homes H
      WHERE U.uid = :uid AND Z.zipcode = U.zipcode AND U.hid = H.hid""")
    
    cursor = g.conn.execute(city_q, uid=current_user_uid)
    home_info = {}
    for result in cursor:
      home_info['zipcode'] = result['zipcode']
      home_info['city'] = result['city_name']
      home_info['price'] = result['avg_price']
      home_info['score'] = result['score']
      home_info['value'] = result['value']
       
    return render_template('homeinfo.html', **home_info)
  else:
    return redirect('/')

@app.route('/zipinfo', methods=["POST"])
def zipinfo():
  req = request.get_json()
  zipcode = req['zipcode']

  print(zipcode)

  query = text("""
    SELECT Z.avg_price, AVG(H.score) as score
    FROM Zipcodes Z NATURAL JOIN Homes H
    WHERE Z.zipcode = :zipcode
    GROUP BY Z.avg_price""")
  zipcode_info = {}
  cursor = g.conn.execute(query, zipcode=zipcode)
  for result in cursor:
    zipcode_info['price'] = result['avg_price']
    zipcode_info['score'] = int(result['score'])

  print(zipcode_info)
  
  return jsonify(zipcode_info)


@app.route('/home')
def home():
  print('in home')
  print(session)
  if 'uid' in session:
    print('in SESSIONS')
    return render_template('home.html')
  else:
    print('redirecting back to root')
    return redirect('/')

@app.route('/comments', methods=["POST"])
def comments():
  req = request.get_json()
  zipcode = req['zipcode']
  print(zipcode)

  comments_q = text("""
    SELECT C.comment, C.comment_id, C.uid, C.topic_id, 
      C.sentiment, C.date_posted, T.topic_name, U.username, U.zipcode,
      U.address
    FROM Users U, Comments C, Topics T
    WHERE U.uid = C.uid 
      AND U.zipcode = :zipcode 
      AND T.tid = C.topic_id
    GROUP BY C.comment_id, C.comment, C.uid, C.topic_id, C.uid, C.sentiment, 
      C.date_posted, T.topic_name, U.username, U.zipcode, U.address""")

  cursor = g.conn.execute(comments_q, zipcode=zipcode)
  comments = []

  for result in cursor:
    comment = Comment(comment=result['comment'], uid=result['uid'],
    topic_id=result['topic_id'], comment_id=result['comment_id'], 
    sentiment=result['sentiment'], 
    topic_name=result['topic_name'], username=result['username'], 
    vote_count=1, zipcode=result['zipcode'], address=result['address'])
    comments.append(Comment.toDict(comment))

  print(comments)
  
  return jsonify(comments)

@app.route('/feedcomments', methods=["POST"])
def feedcomments():
  req = request.get_json()
  print(req)
  filterType = req['filterType']
  filterQuery = req['filterQuery']
  print(filterType)

  # Filter by Zipcode
  if(filterType == 'zipcode'):
    intzip = int(float(filterQuery))

    og_query = text("""
        SELECT C.comment, C.date_posted, C.sentiment, C.topic_id, 
          T.topic_name, C.comment_id, U.uid, U.zipcode, 
          U.username, SUM(V.val) as vote_count
        FROM Users U, Comments C, Topics T, Votes V
        WHERE U.uid = C.uid 
          AND T.tid = C.topic_id
          AND V.comment_id = C.comment_id
          AND C.zipcode LIKE '%:zipcode%'
        GROUP BY C.comment_id, V.val, C.topic_id, T.topic_name, U.username, U.zipcode, U.uid""")

    cursor = g.conn.execute(og_query, zipcode=intzip)
    comments = []
    for result in cursor:
      print(result, '!!!')
      comment = Comment(comment=result['comment'], uid=result['uid'],
      topic_id=result['topic_id'], comment_id=result['comment_id'], 
      sentiment=result['sentiment'], 
      topic_name=result['topic_name'], username=result['username'], 
      vote_count=result['vote_count'], zipcode=result['zipcode'])
      comments.append(Comment.toDict(comment))
    return jsonify(comments)

  # Filter by Date
  elif(filterType == 'date_posted'):
    date_posted = filterQuery

    og_query = text("""
        SELECT C.comment, C.date_posted, C.sentiment, C.topic_id, 
          T.topic_name, C.comment_id, U.uid, U.zipcode, 
          U.username, SUM(V.val) as vote_count
        FROM Users U, Comments C, Topics T, Votes V
        WHERE U.uid = C.uid
        AND V.comment_id = C.comment_id
        AND C.topic_id = T.tid
        AND CAST(C.date_posted AS DATE) = :date_posted
        GROUP BY C.comment_id, C.topic_id, T.topic_name, U.username, U.zipcode, U.uid""")

    cursor = g.conn.execute(og_query, date_posted=date_posted)
    comments = []
    for result in cursor:
      print(result, '!!!')
      comment = Comment(comment=result['comment'], uid=result['uid'],
      topic_id=result['topic_id'], comment_id=result['comment_id'], 
      sentiment=result['sentiment'], 
      topic_name=result['topic_name'], username=result['username'], 
      vote_count=result['vote_count'], zipcode=result['zipcode'])
      comments.append(Comment.toDict(comment))
    return jsonify(comments)

  # Filter by Max Votes 
  elif(filterType == 'maxvotes'):
    maxvotes = int(float(filterQuery))

    og_query = text("""
      SELECT C.comment,  V.val, C.comment_id, C.date_posted, C.sentiment, C.topic_id, T.topic_name, U.uid, U.zipcode, U.username, SUM(V.val) as vote_count
      FROM Users U, Comments C, Topics T, Votes V
      WHERE U.uid = C.uid
      AND V.comment_id = C.comment_id
      AND C.topic_id = T.tid
      AND V.val <= :maxvotes
      GROUP BY C.comment_id,C.topic_id, T.topic_name, U.username, U.zipcode, U.uid, V.val""")

    cursor = g.conn.execute(og_query, maxvotes=maxvotes)
    comments = []
    for result in cursor:
      print(result, '!!!')
      comment = Comment(comment=result['comment'], uid=result['uid'],
      topic_id=result['topic_id'], comment_id=result['comment_id'], 
      sentiment=result['sentiment'], 
      topic_name=result['topic_name'], username=result['username'], 
      vote_count=result['vote_count'], zipcode=result['zipcode'])
      comments.append(Comment.toDict(comment))
    return jsonify(comments)

  # Filter by Min Votes 
  elif(filterType == 'minvotes'):
    minvotes = int(float(filterQuery))

    og_query = text("""
      SELECT C.comment,  V.val, C.comment_id, C.date_posted, C.sentiment, C.topic_id, T.topic_name, U.uid, U.zipcode, U.username, SUM(V.val) as vote_count
      FROM Users U, Comments C, Topics T, Votes V
      WHERE U.uid = C.uid
      AND V.comment_id = C.comment_id
      AND C.topic_id = T.tid
      AND V.val >= :minvotes
      GROUP BY C.comment_id, C.topic_id, T.topic_name, U.username, U.zipcode, U.uid, V.val""")

    cursor = g.conn.execute(og_query, minvotes=minvotes)
    comments = []
    for result in cursor:
      print(result, '!!!')
      comment = Comment(comment=result['comment'], uid=result['uid'],
      topic_id=result['topic_id'], comment_id=result['comment_id'], 
      sentiment=result['sentiment'], 
      topic_name=result['topic_name'], username=result['username'], 
      vote_count=result['vote_count'], zipcode=result['zipcode'])
      comments.append(Comment.toDict(comment))
    return jsonify(comments)

  # Filter by Topic 
  elif(filterType == 'topicfilter'):
    inttid = int(float(filterQuery))

    og_query = text("""
        SELECT C.comment, C.date_posted, C.sentiment, C.topic_id, 
          T.topic_name, C.comment_id, U.uid, U.zipcode, 
          U.username, SUM(V.val) as vote_count
        FROM Users U, Comments C, Topics T, Votes V
        WHERE U.uid = C.uid 
        AND V.comment_id = C.comment_id
        AND C.topic_id LIKE '%:topicfilterid%'
        AND C.topic_id = T.tid
        GROUP BY C.comment_id, T.topic_name, U.username, U.zipcode, 
          U.uid, C.topic_id""")

    cursor = g.conn.execute(og_query, topicfilterid=inttid)
    comments = []
    for result in cursor:
      print(result, '!!!')
      comment = Comment(comment=result['comment'], uid=result['uid'],
      topic_id=result['topic_id'], comment_id=result['comment_id'], 
      sentiment=result['sentiment'], 
      topic_name=result['topic_name'], username=result['username'], 
      vote_count=result['vote_count'], zipcode=result['zipcode'])
      comments.append(Comment.toDict(comment))
    return jsonify(comments)

  else:
    print("yikes")
  
  return redirect('/feed')

@app.route('/profile')
def profile():
  cursor = g.conn.execute("SELECT * FROM users U")
  row = cursor.first()
  user = Citizen(uid=row.uid, name=row.name, username=row.username, email=row.email, zipcode=row.zipcode, 
        hid=row.hid, address=row.address, party_affiliation=row.party_affiliation)
  cursor.close()

  print(user.name)
  return render_template("profile.html", user=user)

@app.route('/newcomment', methods=["POST"])
def newcomment():
  form = request.form

  comment = form['comment']
  sentiment = form['sentiment']
  topic_id = form['topic']
  date_posted = datetime.now()
  comment_id = uuid.uuid4()
  vote_id = uuid.uuid4()

  print(session)
  if 'uid' in session:
    current_user_uid = session['uid']
    uid = current_user_uid
    print("UID")
    print(uid)

    zq = text("""SELECT U.zipcode FROM Users U WHERE U.uid = :uid;""")
    zcursor = g.conn.execute(zq, uid=uid)
    for zresult in zcursor:
      zipcode = zresult[0]
      print("ZIPCODE" + zipcode)

    aq = text("""SELECT U.address FROM Users U WHERE U.uid = :uid;""")
    acursor = g.conn.execute(aq, uid=uid)
    for aresult in acursor:
      address = aresult[0]
    print(address)
  else:
    print("not a user")

  # Inserting comment
  q = text("""INSERT INTO comments(comment, uid, topic_id, comment_id, sentiment, zipcode,
      date_posted)
    VALUES(:comment, :uid, :topic_id, :comment_id, :sentiment, :zipcode, :date_posted)""")

  print("query")
  g.conn.execute(q, comment=comment, uid=uid, topic_id=topic_id, 
    comment_id=comment_id, sentiment=sentiment, zipcode=zipcode, date_posted=date_posted)

  vq = text("""INSERT INTO votes(vote_id, val, comment_id, uid)
    VALUES(:vote_id, :val, :comment_id, :uid)""") 
  g.conn.execute(vq, vote_id=vote_id, val=1, comment_id=comment_id, uid=uid) 
  return redirect('/feed')

@app.route('/voting', methods=["POST"])
def voting():
  # form = request.form
  # up = request['up']
  print("VOTED")
  return redirect('/feed')


@app.route('/representativeSignUp', methods=["POST"])
def representativeSignUp():
  data = request.form

  username = data['username']
  password = data['password']
  email = data['email']
  name = data['name']
  address = data['address']
  zipcode = data['zipcode']
  party = data['party']
  value = data['value']
  phone_number = data['phone-num']
  uid = uuid.uuid4()
  home_id = uuid.uuid4()

  g.conn.execute(text("""
  INSERT INTO zipcodes (zipcode, avg_price)
    SELECT :zipcode, 0
    WHERE :zipcode NOT IN (
      SELECT z.zipcode FROM zipcodes z)
  """), zipcode=zipcode)

  g.conn.execute(text("INSERT INTO homes VALUES (:hid, :score, :zipcode, :value)"), 
  hid=home_id, score=10, zipcode=zipcode, value=value)

  g.conn.execute(text("""
  INSERT INTO users VALUES(:uid, :name, :username, 
    :password, :email, :zipcode, :hid, :address, :party)
  """), uid=uid, name=name, username=username, 
  password=password, email=email, zipcode=zipcode, hid=home_id, 
  address=address, party=party)

  g.conn.execute(text("""
    INSERT INTO representatives VALUES(:uid, :phone_number)
  """), uid=uid, phone_number=phone_number)


  session['uid'] = uid 
  session['isRep'] = True
  session['username'] = username

  return redirect('/map')

@app.route('/citizenSignUp', methods=["POST"])
def citizenSignUp():

  data = request.form

  print(data['username'])

  username = data['username']
  password = data['password']
  email = data['email']
  name = data['name']
  address = data['address']
  zipcode = data['zipcode']
  value = int(data['value'])
  party = data['party']
  uid = uuid.uuid4()
  home_id = uuid.uuid4()
  party = "Democrat"

  score = 10

  g.conn.execute(text("""
    INSERT INTO zipcodes (zipcode, avg_price)
      SELECT :zipcode, :avg_price
      WHERE :zipcode NOT IN (
        SELECT z.zipcode FROM zipcodes z)
    """), zipcode=zipcode, avg_price=value)

  g.conn.execute(text("INSERT INTO homes VALUES (:hid, :score, :zipcode, :value)"),
  hid=home_id, score=score, zipcode=zipcode, value=value)

  g.conn.execute(text("""
    INSERT INTO users VALUES(:uid, :name, :username, 
      :password, :email, :zipcode, :hid, :address, :party)
    """), uid=uid, name=name, username=username, 
    password=password, email=email, zipcode=zipcode, hid=home_id, 
    address=address, party=party)

  g.conn.execute(text("INSERT INTO citizens VALUES(:uid)"), uid=uid)

  session['uid'] = uid
  session['isRep'] = False
  session['username'] = username

  return redirect('/home')

@app.route('/login', methods=["POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    username = form['username'].data
    password = form['password'].data

    q = text("SELECT * FROM users U WHERE username = :username AND password = :password")
    cursor = g.conn.execute(q, username=username, password=password)

    row = cursor.first()
    if row:
      user = Citizen(uid=row.uid, name=row.name, username=row.username, email=row.email, zipcode=row.zipcode, 
        hid=row.hid, address=row.address, party_affiliation=row.party_affiliation)

      session['username'] = user.username
      session['uid'] = user.uid
      return redirect('/feed')
    else:
      flash('Username or password incorrect')
      return redirect('/')
  else:
    errs = []
    for error in form.errors.items():
      errs.append("{}: {}".format(error[1][0], error[0]))
    flash(errs)
    return redirect('/')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

@app.route('/feed')
def feed():
  return render_template("feed.html")

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True, threaded=threaded)

  run()