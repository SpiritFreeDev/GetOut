from app import db
from passlib.hash import sha256_crypt
#from app import myapp
from time import time

import jwt

# Helper table for many to many relationship between projects and employees
catsub = db.Table('catsubs',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), nullable=False),
    db.Column('cat_id', db.Integer, db.ForeignKey('categories.cat_id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'cat_id')
    )

class User(db.Model):
    """
    Create the User table
    """
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    user_id         = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(60), index=True, nullable=False)
    last_name       = db.Column(db.String(60), index=True, nullable=False)
    username        = db.Column(db.String(60), index=True, unique=True, nullable=False)
    email           = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password_hash   = db.Column(db.String(128), nullable=False)
    register_date   = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    last_urs_update = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    is_sysadmin     = db.Column(db.Boolean, default=False, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    temporary_pwd   = db.Column(db.Boolean, default=False, nullable=False)
    # Account locked
    is_locked       = db.Column(db.Boolean, default=False, nullable=False)

    # Many-to-many relationship with the Category model
    # Users can select multiple categories, categories can have multiple users
    # NOTE: users is implicitely defined in the categories table
    # ex: Category(cat_name="ABC").users - gives all users assigned to cat ABC
    # ex: User(username="xyz").cats - gives all categories assigned to user xyz
    # ex: Category(cat_name="ABC").users.append(User(username='coutuan3'))  to assign coutuan3 to cat ABC
    cats = db.relationship('Category', secondary=catsub, backref=db.backref('users', lazy='dynamic'))

    # TODO: need to find how to access myapp.config['SECRET_KEY'] as myapp needs models to be
    #       defined and models need myapp to get to the secret key
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.user_id, 'exp': time() + expires_in, 'expcheck': expires_in},
            'myverysecretKEY', algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, 'myverysecretKEY',
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Category(db.Model):
    """
    Create a Category table
      Categories can be assigned to multiple Users and vice versa (Many to Many relationship)
    """
    __tablename__ = 'categories'

    cat_id             = db.Column(db.Integer, primary_key=True)
    cat_name           = db.Column(db.String(60), unique=True)
    subcat_name        = db.Column(db.String(60), unique=True)
    cat_description    = db.Column(db.String(500))
    subcat_description = db.Column(db.String(500))
    catregister_date   = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    last_cat_update    = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    # May want to lock a category from the entire site
    is_locked          = db.Column(db.Boolean, default=False, nullable=False)
    # TO ADD
    #https://en.wikipedia.org/wiki/Squash_(sport)
    #info_link          = db.Column(db.String(200))
    #subcat_img         = db.Column(db.String(50))
    def __repr__(self):
     return "<Category {}>".format(self.cat_name)

#To be added in user profile we will give a default avatar
# avatar          = db.Column(db.String(200), index=True, unique=True, nullable=False)
# Country
# phone number
# address
# Team membership (Core Global Clinical Team, )
# User Picture with default meme
