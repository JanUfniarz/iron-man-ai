from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import singleton

from symbiot_division import SymbiotDivision
from .operation_endpoint import OperationEndpoint
from .operation_repository import OperationRepository
from .operation_service import OperationService


class OperationDivision(SymbiotDivision):

    def configure(self, binder):
        binder.bind(OperationEndpoint, scope=singleton)
        binder.bind(Flask, to=super().app)
        binder.bind(OperationService, scope=singleton)
        binder.bind(OperationRepository, scope=singleton)
        binder.bind(SQLAlchemy, to=super().db)
