from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/manifest'
db = SQLAlchemy(app)
CORS(app)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Announcement: {self.description}"
    
    def __init__(self, sender, title, description):
        self.sender = sender
        self.title = title
        self.description = description

def format_announcement(announcement):
    return {
        "sender": announcement.sender,
        "title": announcement.title,
        "description": announcement.description,
        "id": announcement.id,
        "added": announcement.added
    }

@app.route('/')
def hello():
    return 'Hey!'

# Create an announcement
@app.route('/announcement', methods = ['POST'])
def create_announcement():
    sender = request.json['sender']
    title = request.json['title']
    description = request.json['description']
    announcement = Announcement(sender, title, description)
    db.session.add(announcement)
    db.session.commit()
    return format_announcement(announcement)

# Get all announcements
@app.route('/announcements', methods = ['GET'])
def get_announcements():
    time.sleep(1)
    announcements = Announcement.query.order_by(Announcement.id.asc()).all()
    announcement_list = []
    for announcement in announcements:
        announcement_list.append(format_announcement(announcement))

    return {'announcements': announcement_list}

if __name__ == '__main__':
    app.run(port=8000, debug=True)