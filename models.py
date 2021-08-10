from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#####################
#       USER        #
#####################

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )

    def __init__(self,name, email, id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.name = name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    
    def __repr__(self):
        return f'User {self.email} has been added to the database'

    

#####################
#       HABIT       #
#####################

class Habit(db.Model):
    id = db.Column(db.String, primary_key = True)
    habit_class = db.Column(db.String)
    smart_goal = db.Column(db.String(100))
    habit_date = db.Column(db.DateTime, nullable = False, default = datetime.date)
    habit_steps = db.Column(db.String(300))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, habit_class, smart_goal, habit_date, habit_steps, user_token, id=''):
        self.id = self.set_id()
        self.habit_class = habit_class
        self.smart_goal = smart_goal
        self.habit_date = habit_date
        self.habit_steps = habit_steps
        self.user_token = user_token

    # magic method can be used to print this information
    def __repr__(self):
        return f'Your SMART goal has been updated!'
        # return f'Your SMART goal has been updated!/n{self.smart_goal}'

    # will callback specific habits
    def set_id(self):
        return (secrets.token_urlsafe())


#####################
#       JOURNAL     #
#####################

class JournalEntry(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(1000), nullable = False) 
    entry = db.Column(db.String(1000), nullable = False)
    entry_date = db.Column(db.DateTime, nullable = False, default = datetime.date)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, title, entry, entry_date, user_token, id=''):
        self.id = self.set_id()
        self.title = title
        self.entry = entry
        self.entry_date = entry_date
        self.user_token = user_token

    # magic method can be used to print this information
    def __repr__(self):
        return f'Your entry has been updated!'
        # return f'Your SMART goal has been updated!/n{self.smart_goal}'

    # will callback specific entries
    def set_id(self):
        return (secrets.token_urlsafe())


# Creation of API Schema via the Marshmallow Object
class HabitSchema(ma.Schema):
    class Meta:
        fields = ['habit_class','smart_goal', 'habit_date', 'habit_steps']


habit_schema = HabitSchema()
habits_schema = HabitSchema(many = True)


class JournalEntrySchema(ma.Schema):
    class Meta:
        fields = ['title', 'entry', 'entry_date']

journal_entry_schema = JournalEntrySchema()
journal_entries_schema = JournalEntrySchema(many = True)
