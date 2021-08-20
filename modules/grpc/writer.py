import grpc
import service_pb2
import service_pb2_grpc

from datetime import datetime

print("Sending sameple data...")

channel = grpc.insecure_channel("localhost:5004")
stub = service_pb2_grpc.CallServiceStub(channel)

Person = service_pb2.PersonMsg(id=1, first_name="Steeve", last_name = "Joel", company_name = "Big Tech Comp")
response = stub.create_person(Person)
print(Person)

#Location = service_pb2.LocationMsg(id=1, person_id=1, latitude = "32N", longitude="32E", creation_time = "12am")
#stub.create_loc(Location)
#print(Location)