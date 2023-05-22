from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        messages_serialized = [message.to_dict() for message in messages]

        response = make_response(
            messages_serialized,
            200
        )
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            message_dict,
            201
        )
        return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    
    if request.method == 'PATCH':  
        message = Message.query.filter(Message.id == id).first()
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data.get(attr))

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            message_dict,
            200
        )
        return response

    elif request.method == 'DELETE':
        message = Message.query.filter(Message.id == id).first()

        db.session.delete(message)
        db.session.commit()

        response = make_response(
            "message has been deleted"
        )
        return response

if __name__ == '__main__':
    app.run(port=5555)
