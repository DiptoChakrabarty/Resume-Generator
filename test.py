from flask import Flask,request,jsonify
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo import MongoClient



app =  Flask(__name__)

app.config['SECRET_KEY'] = 'e23739c67eade607c64f90c3ebb479ca' 

'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)'''

client= MongoClient("mongodb://localhost:27017")
db = client.resume
users = db["users"]

bcrypt = Bcrypt(app)



@app.route("/register",methods=['POST'])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    email = data["email"]
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    
    '''new_user = user(username=form.username.data,email=form.email.data,password=hashed)
    db.session.add(new_user)
    db.session.commit()'''
    
    users.insert({
        "username": username,
        "email": email,
        "password": hashed
    })
    ret={
        "status": 200,
        "msg": "user made"
    }
    
    #flash(f'Account Created for {fousername}!','success')
    
    return jsonify(ret)



if __name__ ==  '__main__':
    app.run(debug=True)
