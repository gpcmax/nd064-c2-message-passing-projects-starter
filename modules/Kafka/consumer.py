from kafka import KafkaConsumer
import json
import grpc
import service_pb2
from service_pb2 import PersonMsg, LocationMsg
import service_pb2_grpc

TOPIC_NAME = 'person'

def create_person(reg):
    channel = grpc.insecure_channel("grpc:5005")
    stub = service_pb2_grpc.CallServiceStub(channel)
    person = PersonMsg(
        first_name = reg["first_name"],
        last_name = reg["last_name"],
        company_name = reg["company_name"])
    stub.create_person(person)

def create_loc(reg):
    channel = grpc.insecure_channel("grpc:5005")
    stub = service_pb2_grpc.CallServiceStub(channel)
    location = LocationMsg(
        person_id = reg["person_id"],
        latitude = reg["latitude"],
        longitude = reg["longitude"],
        creation_time = reg["creation_time"])
    stub.create_loc(location)
    

consumer = KafkaConsumer('test',
     bootstrap_servers=['my-release-kafka.default.svc.cluster.local:9092'],
     api_version=(0,10),
     value_deserializer=lambda m: json.dumps(m.decode('utf-8')))

for message in consumer:
    response=eval(json.loads((message.value)))
    if("first_name" in message):
        create_person(response)
    if("person_id" in message):
        create_loc(response)
    print(response)