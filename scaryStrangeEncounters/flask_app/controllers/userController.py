from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.userModel import User
from flask_app.models.encounterModel import Encounter

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    thePage = {
        # 'title': 'Scary Strange Encounters'
    }
    if 'user_id' not in session:
        return render_template('logReg.html', page=thePage)
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        theEncounters = Encounter.getAll()
        theUsers = User.getAll()
        return render_template('index.html', user=theUser, page=thePage, encounters=theEncounters, users=theUsers)
    
@app.route('/logout/')
def logout():
    session.clear()
    flash("We Will be in contact...")
    return redirect('/')

@app.route('/reg/', methods=['post'])
def registration():
    is_valid = User.validate(request.form)
    if not is_valid:
        return redirect('/')
    else:
        new_user = {
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        id = User.save(new_user)
        if not id:
            flash("Please make sure information entered is correct.")
            return redirect('/')
        else:
            session['user_id'] = id
            flash("Welcome, encryption activated!")
            return redirect('/')
        
@app.route('/login/', methods=['post'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data)
    if not user:
        flash("Email not found, please register.")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password")
        return redirect('/')
    else:
        session['user_id'] = user.id
        flash("They are watching you <> <>")
        return redirect('/')
    
# Profile
@app.route('/profile/')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    else:
        thePage = {
            # 'title': 'Scary Strange Encounters'
        }
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        theUserEncounters = User.userEncounters(data)
        return render_template('profile.html', page=thePage, user=theUser, userEncounters=theUserEncounters)