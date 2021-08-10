from flask import Blueprint, request, jsonify
from helpers import token_required
from models import JournalEntry, db,User,Habit,JournalEntry,habit_schema,habits_schema, journal_entry_schema, journal_entries_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value'}


# CREATE HABIT ENDPOINT

@api.route('/habits', methods = ['POST'])
@token_required
def create_habit(current_user_token):
    habit_class = request.json['habit_class']
    smart_goal = request.json['smart_goal']
    habit_date = request.json['habit_date']
    habit_steps = request.json['habit_steps']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    habit = Habit( habit_class,smart_goal,habit_date, habit_steps, user_token = user_token )

    db.session.add(habit)
    db.session.commit()

    response = habit_schema.dump(habit)
    return jsonify(response)




# RETRIEVE ALL HABITS ENDPOINT
@api.route('/habits', methods = ['GET'])
@token_required
def get_habits(current_user_token):
    owner = current_user_token.token
    habits = Habit.query.filter_by(user_token = owner).all()
    response = habits_schema.dump(habits)
    return jsonify(response)


# RETRIEVE ONE HABIT ENDPOINT
@api.route('/habits/<id>', methods = ['GET'])
@token_required
def get_habit(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        habit = Habit.query.get(id)
        response = habit_schema.dump(habit)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



# UPDATE HABIT ENDPOINT
@api.route('/habits/<id>', methods = ['PUT'])
@token_required
def update_habit(current_user_token,id):
    habit = Habit.query.get(id) # getting instance of habit

    habit.habit_class = request.json['habit_class']
    habit.smart_goal = request.json['smart_goal']
    habit.habit_date = request.json['habit_date']
    habit.habit_steps = request.json['habit_steps']
    habit.user_token = current_user_token.token

    db.session.commit()
    response = habit_schema.dump(habit)
    return jsonify(response)


# DELETE HABIT ENDPOINT
@api.route('/habits/<id>', methods = ['DELETE'])
@token_required
def delete_habit(current_user_token, id):
    habit = Habit.query.get(id)
    db.session.delete(habit)
    db.session.commit()
    response = habit_schema.dump(habit)
    return jsonify(response)


################################
#         JOURNAL ENTRIES      #
################################

# CREATE JOURNAL ENTRY ENDPOINT





@api.route('/journal', methods = ['POST'])
@token_required
def create_entry(current_user_token):
    title = request.json['title']
    entry = request.json['entry']
    entry_date = request.json['entry_date']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    entry = JournalEntry( title, entry, entry_date, user_token = user_token )

    db.session.add(entry)
    db.session.commit()

    response = journal_entry_schema.dump(entry)
    return jsonify(response)




# RETRIEVE ALL ENTRIES ENDPOINT
@api.route('/journal', methods = ['GET'])
@token_required
def get_entries(current_user_token):
    owner = current_user_token.token
    entries = JournalEntry.query.filter_by(user_token = owner).all()
    response = habits_schema.dump(entries)
    return jsonify(response)


# RETRIEVE ONE JOURNAL ENTRY ENDPOINT
@api.route('/journal/entry/<id>', methods = ['GET'])
@token_required
def get_entry(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        entry = JournalEntry.query.get(id)
        response = journal_entry_schema.dump(entry)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



# UPDATE Entry ENDPOINT
@api.route('/journal/entry/<id>', methods = ['POST','PUT'])
@token_required
def update_entry(current_user_token,id):
    entry = JournalEntry.query.get(id) # getting instance of journal entry

    title, user_id, entry, entry_date, id=''
    
    entry.title = request.json['title']
    entry.entry = request.json['entry']
    entry.entry_date = request.json['entry_date']
    entry.user_token = current_user_token.token

    db.session.commit()
    response = journal_entry_schema.dump(entry)
    return jsonify(response)


# DELETE ENTRY ENDPOINT
@api.route('/journal/entry/<id>', methods = ['DELETE'])
@token_required
def delete_entry(current_user_token, id):
    entry = JournalEntry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    response = journal_entry_schema.dump(entry)
    return jsonify(response)