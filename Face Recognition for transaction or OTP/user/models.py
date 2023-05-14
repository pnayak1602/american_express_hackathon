from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:

  def start_session(self, user):
    del user['cvv']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "card-num": request.form.get('card-num'),
      "card-name": request.form.get('card-name'),
      "exp-date": request.form.get('exp-date'),
      "cvv": request.form.get('cvv')
    }

    # Encrypt the password
    user['cvv'] = pbkdf2_sha256.encrypt(user['cvv'])

    # Check for existing email address
    if db.users.find_one({ "card-num": user['card-num'] }):
      return jsonify({ "error": "Card already added" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Adding card failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.users.find_one({
      "card-num": request.form.get('card-num')
    })

    if user and pbkdf2_sha256.verify(request.form.get('cvv'), user['cvv']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid card credentials" }), 401