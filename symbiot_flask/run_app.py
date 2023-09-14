from flask import Flask
from injector import Injector

from client_division.client_division import ClientDivision
from client_division.keys_controller import KeysController
from mediator import Mediator
from operation_division.operation_controller import OperationController
from operation_division.operation_division import OperationDivision
from operation_division.operation_entity import db as operation_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:postgres@localhost:5432/symbiot'

operation_db.init_app(app)

if __name__ == '__main__':
    # with app.app_context():
    #     operation_db.drop_all()
    #     operation_db.create_all()

    symbiot = Injector([
        OperationDivision(app, operation_db),
        ClientDivision(app)
    ])

    mediator = Mediator(symbiot)

    symbiot.get(OperationController).listen("/operation")
    symbiot.get(KeysController).listen("/key")

    app.run(debug=True)