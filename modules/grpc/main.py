import time
from types import FunctionType
from flask.wrappers import Response
import grpc
import json
import os
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from sqlalchemy.engine.interfaces import CreateEnginePlugin
from sqlalchemy.sql.expression import false, true
import service_pb2
import service_pb2_grpc
from concurrent import futures
from dataclasses import fields
from geoalchemy2.types import Geometry as GeometryType
from marshmallow import Schema, fields
from marshmallow_sqlalchemy.convert import ModelConverter as BaseModelConverter
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

class Person(base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)

class Location(base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, nullable=False)
    coordinate  = Column(Geometry("POINT"), nullable=False)
    creation_time = Column(String, nullable=False)

class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String(attribute="longitude")
    latitude = fields.String(attribute="latitude")
    creation_time = fields.DateTime()

    class Meta:
        model = Location


class PersonSchema(Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    company_name = fields.String()

    class Meta:
        model = Person

class UdaServicer(service_pb2_grpc.CallServiceServicer):
    def create_person(self, request, context):
        addPerson = Person()
        addPerson.first_name = request.first_name
        addPerson.last_name = request.last_name
        addPerson.company_name = request.company_name
        db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = CreateEnginePlugin(db_string)
        Session = sessionmaker(bind=db)
        session = Session()
        query = session.query(FunctionType.max(addPerson.id).label("max_id"))
        addPerson.id = (query.one().max_id) + 1
        session.add(addPerson)
        session.commit()
        print(addPerson)
        response = service_pb2.Person()
        response.person = true
        return response
    def create_loc(self, request, context):
        addLocation = Location()
        addLocation.person_id = request.person_id
        addLocation.longitude = request.longitude
        addLocation.latitude = request.latitude
        addLocation.creation_time = request.creation_time
        db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        db = CreateEnginePlugin(db_string)
        Session = sessionmaker(bind=db)
        session = Session()
        query = session.query(FunctionType.max(addLocation.id).label("max_id"))
        addLocation.id = (query.one().max_id) + 1
        session.add(addLocation)
        session.commit()
        print(addLocation)
        response = service_pb2.Location()
        response.location = true
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
service_pb2_grpc.add_CallServiceServicer_to_server(UdaServicer(), server)

print("Server starting on port 5004...")
server.add_insecure_port("[::]:5004")
server.start()
try:
    while True:
        time.sleep(86488)
except KeyboardInterrupt:
    server.stop(0)