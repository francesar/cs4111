import os
import pandas as pd
import requests
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, request, render_template, g, redirect, Response, flash, session, jsonify

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
  if 'uid' in session:
    print(session)
    return render_template('home.html')
  else:
    return redirect('/')

@app.route('/comments', methods=["POST"])
def comments():
  req = request.get_json()
  zipcode = req['zipcode']

  comments_q = text("""
    SELECT C.comment, C.comment_id, C.uid, C.topic_id, 
      C.sentiment, T.topic_name, U.username, U.zipcode,
      SUM(V.val) as vote_count
    FROM Users U, Comments C, Topics T, Votes V
    WHERE U.uid = C.uid 
      AND U.zipcode = :zipcode 
      AND T.tid = C.topic_id
      AND V.comment_id = C.comment_id
    GROUP BY C.comment_id, C.comment, C.uid, C.topic_id, C.uid, C.sentiment, 
      T.topic_name, U.username, U.zipcode""")

  cursor = g.conn.execute(comments_q, zipcode=zipcode)
  comments = []

  for result in cursor:
    print(result, 'HELLO')
    comment = Comment(comment=result['comment'], uid=result['uid'],
    topic_id=result['topic_id'], comment_id=result['comment_id'], 
    sentiment=result['sentiment'], topic_name=result['topic_name'], 
    username=result['username'], vote_count=result['vote_count'],
    zipcode=zipcode)
    comments.append(Comment.toDict(comment))

  print(comments)
  
  return jsonify(comments)

@app.route('/feedcomments', methods=["POST"])
def feedcomments():
  req = request.get_json()
  zipcode = req['zipcode']
  print(zipcode)

  query = text("SELECT * FROM Comments")
  cursor = g.conn.execute(query)
  comments = []
  for result in cursor:
    comment = Comment(comment=result['comment'], uid=result['uid'], 
    topic_id=result['topic_id'], comment_id=result['comment_id'], 
    sentiment=result['sentiment'])
    comments.append(Comment.toDict(comment))
  
  return jsonify(comments)

@app.route('/profile')
def profile():
  cursor = g.conn.execute("SELECT * FROM users U")
  row = cursor.first()
  user = Citizen(username=row.username, uid=row.uid, name=row.name,
        email=row.email, zipcode=row.zipcode, hid=row.hid)
  cursor.close()

  print(user.name)
  return render_template("profile.html", user=user)

@app.route('/newcomment', methods=["POST"])
def newcomment():
  #form = request.form
  
  comment = "comment" #form['comment']
  uid = 1 
  topic_id = 1
  comment_id = 110
  sentiment = 1 #form['sentiment']

  print(comment)
  q = text("""INSERT INTO comments(comment, uid, topic_id, comment_id, sentiment)
    VALUES(:comment, :uid, :topic_id, :comment_id, :sentiment)""")
  g.conn.execute(q, comment=comment, uid=uid, topic_id=topic_id, 
    comment_id=comment_id, sentiment=sentiment)

  return redirect('/feed')

@app.route('/signup', methods=["POST"])
def signup():
  form = request.form
  
  name = form['name']
  username = form['username']
  password = form['password']
  email = form['email']
  address = form['address']
  zipcode = form['zipcode']
  phonenumber = form['phonenumber']
  party = form['party']

  q = text("""INSERT INTO users(uid, name, username, password, email, zipcode, hid)
    VALUES(:uid, :name, :username, :password, :email, :zipcode, :hid)""")
  g.conn.execute(q, uid=12234, name=name, 
    username=username, password=password, 
    email=email, zipcode=60651, hid=1234456)

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
      user = Citizen(username=row.username, uid=row.uid, name=row.name,
      email=row.email, zipcode=row.zipcode, hid=row.hid)

      session['username'] = user.username
      session['uid'] = user.uid
      return redirect('/home')
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