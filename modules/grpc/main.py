import time
from concurrent import futures

from grpc import server
import grpc

import service_pb2
import service_pb2_grpc

class LocationServicer(service_pb2_grpc.GetServiceServicer):
    def Create(self, request, context):
        request_value = {
            "person_id": int(request.person_id),
            "creation_time": request.creation_time,
            "coordinate": request.coordinate,
        }
        print(request_value)
        return service_pb2.LocationMsg(**request_value)
        
class PersonServicer(service_pb2_grpc.GetServiceServicer):
    def Create(self, request, context):
        request_value = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }
        print(request_value)
        return service_pb2.PersonMsg(**request_value)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
service_pb2_grpc.add_GetServiceServicer_to_server(LocationServicer(),server)
service_pb2_grpc.add_GetServiceServicer_to_server(PersonServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
try:
    while True:
        time.sleep(86488)
except KeyboardInterrupt:
    server.stop(0)