from google.appengine.ext import db

class Publication(db.Model):
    title = db.StringProperty()
    date = db.DateProperty()

