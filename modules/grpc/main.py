import time
import grpc
import service_pb2
import service_pb2_grpc
from concurrent import futures

class UdaServicer(service_pb2_grpc.CallServiceServicer):
    def create_person(self, request, context):
        request_value = {
            "id": request.id,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "company_name": request.company_name,
        }
        print(request_value)
        return service_pb2.PersonMsg(**request_value)
    def create_loc(self, request, context):
        request_value = {
            "id": request.id,
            "person_id":request.person_id,
            "latitude":request.latitude,
            "longitude":request.longitude,
            "creation_time":request.creation_time,
        }
        print(request_value)
        return service_pb2.LocationMsg(**request_value)

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