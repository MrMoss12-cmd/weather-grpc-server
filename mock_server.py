import grpc
from concurrent import futures
import json
from weather_pb2 import WeatherResponse, UpdateWeatherResponse
from weather_pb2_grpc import WeatherServiceServicer, add_WeatherServiceServicer_to_server

class MockWeatherService(WeatherServiceServicer):
    def GetWeather(self, request, context):
        print("\nReceived GetWeather request:")
        print(f"Postal Code: {request.postal_code}")
        return WeatherResponse()

    def UpdateWeather(self, request, context):
        print("\nReceived UpdateWeather request:")
        print("Postal Codes:", list(request.postal_codes))
        print("Request type:", type(request.postal_codes))
        
        # Mock response
        return UpdateWeatherResponse(
            updated_postcodes=list(request.postal_codes),
            failed_postcodes=[],
            message="Test response"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WeatherServiceServicer_to_server(MockWeatherService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Mock Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()