from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.userModel import User
from flask_app.models.encounterModel import Encounter


# Encounter Add form
@app.route('/encounter/add/')
def addEncounter():
    thePage = {
        # 'title': 'What did you see?'
    }
    if 'user_id' not in session:
        flash("Please login")
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        return render_template('addEncounter.html', user=theUser, page=thePage)

# Create Encounter
@app.route('/encounter/create/', methods=['post'])
def createEncounter():
    encounter = {
        'category': request.form['category'],
        'location': request.form['location'],
        'encounterReport': request.form['encounterReport'],
        'dateEncounter': request.form['dateEncounter'],
        'user_id': int(session['user_id'])
    }
    newEncounter = Encounter.save(encounter)
    if newEncounter:
        encounterID = newEncounter
        flash("Encounter Added")
        return redirect(f'/encounter/{encounterID}/view/')
    else:
        flash('check information')
        return redirect('/encounter/add/')

# View Encounter
@app.route('/encounter/<int:encounterID>/view/')
def viewEncounter(encounterID):
    if 'user_id' not in session:
        return redirect('/')
    encounterData = {
        'id': encounterID
    }
    theEncounter = Encounter.getOne(encounterData)
    thePage = {
        # 'title': f'{theEncounter.category}'
    }
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    return render_template('viewEncounter.html', page=thePage, user=theUser, encounter=theEncounter)

# Edit Encounter form
@app.route('/encounter/<int:encounterID>/edit/')
def editEncounter(encounterID):
    if 'user_id' not in session:
        return redirect('/')
    encounterData = {
        'id': encounterID
    }
    theEncounter = Encounter.getOne(encounterData)
    thePage = {
        # 'title': f'Edit {theEncounter.category}'
    }
    data = {
        'id': session['user_id']
    }
    theUser = User.getOne(data)
    return render_template('editEncounter.html', page=thePage, user=theUser, encounter=theEncounter)

# Update Encounter
@app.route('/encounter/<int:encounterID>/update/', methods=['post'])
def updateEncounter(encounterID):
    encounterData = {
        'id': encounterID,
        'category': request.form['category'],
        'location': request.form['location'],
        'encounterReport': request.form['encounterReport'],
        'dateEncounter': request.form['dateEncounter']
    }
    Encounter.update(encounterData)
    return redirect(f'/encounter/{encounterID}/view/')

# Delete Encounter
@app.route('/encounter/<int:encounterID>/delete/')
def deleteEncounter(encounterID):
    data = {
        'id': encounterID
    }
    Encounter.delete(data)
    flash('That Encounter has been classified')
    return redirect('/profile/') #maybe I don't need the extra / but see if it works with it if not delete


# @app.route('/like/', methods=['post'])
# def likeFish():
#     theLike = User.userLike(request.form)
#     return redirect('/')