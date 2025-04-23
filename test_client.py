import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import update_weather, get_weather
import grpc
from weather_pb2 import WeatherRequest, UpdateWeatherRequest
from weather_pb2_grpc import WeatherServiceStub

def test_update_request():
    print("\nTesting Update Request:")
    channel = grpc.insecure_channel('localhost:50051')
    stub = WeatherServiceStub(channel)
    
    # Test single postal code
    print("\nTesting single postal code:")
    request = UpdateWeatherRequest(postal_codes=['080001'])
    print(f"Sending request: {request}")
    response = stub.UpdateWeather(request)
    print(f"Response received: {response}")
    
    # Test multiple postal codes
    print("\nTesting multiple postal codes:")
    request = UpdateWeatherRequest(postal_codes=['080001', '470001', '130001'])
    print(f"Sending request: {request}")
    response = stub.UpdateWeather(request)
    print(f"Response received: {response}")
    
    channel.close()

def test_get_request():
    print("\nTesting Get Request:")
    channel = grpc.insecure_channel('localhost:50051')
    stub = WeatherServiceStub(channel)
    
    request = WeatherRequest(postal_code='080001')
    print(f"Sending request: {request}")
    response = stub.GetWeather(request)
    print(f"Response received: {response}")
    
    channel.close()

if __name__ == '__main__':
    test_get_request()
    test_update_request()