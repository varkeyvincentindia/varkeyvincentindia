from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user # import these functions
from .models import Note
from . import db # import db object (sqlalchemy obj) from __init__.py
import json
 

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required # you cannot get to the homepage without logging in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category= 'error')
        else:
            new_note=Note(data=note, user_id= current_user.id) #'note' from line 11 added to the data attribute in Note object
            db.session.add(new_note)

            db.session.commit()
            flash('Note added', category= 'success')
    return render_template("home.html", user= current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # string passed from index.js converted to dictionary
    noteId = note['noteId'] # key value passed from index.js is 'noteId'
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({}) # flask function