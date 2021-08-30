from __future__ import annotations
from kafka import KafkaConsumer
from dataclasses import dataclass
from datetime import datetime
from service_pb2 import PersonMsg, LocationMsg
import service_pb2
import service_pb2_grpc
import json
import ast
import grpc
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

def create_person(req):
    channel = grpc.insecure_channel('grpc-api:5004')
    stub = service_pb2_grpc.CallServiceStub(channel)
    person = PersonMsg(first_name=req["first_name"] , last_name=req["last_name"], company_name=req["company_name"])
    stub.create_person(person)


def create_location(req):
    channel = grpc.insecure_channel('grpc-api:5004')
    stub = service_pb2_grpc.CallServiceStub(channel)
    location = LocationMsg(person_id=req["person_id"], creation_time=req["creation_time"],latitude=req["latitude"],longitude=req["longitude"])
    stub.create_loc(location)


consumer = KafkaConsumer('test',
     bootstrap_servers=['my-release-kafka.default.svc.cluster.local:9092'],
     value_deserializer=lambda m: json.dumps(m.decode('utf-8')))

for message in consumer:
    resp=eval(json.loads((message.value)))
    if "first_name" in resp:
        create_person(resp)
        logger.warning("Person Created")
    elif "person_id" in resp:
        create_location(resp)
        logger.warning("Location Created")
    else:
      print(resp)
      logger.warning("Nothing created")