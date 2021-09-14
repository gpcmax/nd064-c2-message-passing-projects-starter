import grpc
import service_pb2
import service_pb2_grpc
from service_pb2 import PersonMsg, LocationMsg

from datetime import datetime

# open a gRPC channel
channel = grpc.insecure_channel('localhost:5004')

# create a stub (client)
stub = service_pb2_grpc.CallServiceStub(channel)

# create a valid request message
person = PersonMsg(first_name="Bob" , last_name="Stevens", company_name="Tech Comp")
#location = LocationMessage(person_id=5,creation_time="2020-01-05T10:37:06",latitude="20.518730",longitude="22.992470")
#stub.create_location(location)
stub.create_person(person)
print(person)
#print(location)

# make the call
#stub.create_person(person)