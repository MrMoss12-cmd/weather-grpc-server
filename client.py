import grpc
import argparse
from weather_pb2 import WeatherRequest, UpdateWeatherRequest
from weather_pb2_grpc import WeatherServiceStub

def get_weather(stub, postal_code):
    try:
        request = WeatherRequest(postal_code=postal_code)
        response = stub.GetWeather(request)
        print(f"\nWeather information for postal code {response.postcode}:")
        print(f"Location: {response.subdiv_name}")
        print(f"Temperature: {response.temp}°C")
        print(f"Feels like: {response.feels_like}°C")
        print(f"Relative Humidity: {response.rel_hum}%")
        print(f"Wind Direction: {response.wind_dir}°")
        print(f"Timestamp: {response.timestamp}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")

def update_weather(stub, postal_codes):
    try:
        # Convert the first postal code to string if multiple are provided
        postal_code = str(postal_codes[0])
        request = UpdateWeatherRequest(postal_codes=[postal_code])
        response = stub.UpdateWeather(request)
        if response.updated_postcodes:
            print("\nSuccessfully updated postcode:")
            print(f"- {response.updated_postcodes[0]}")
            print(f": {response.message}")
        if response.failed_postcodes:
            print("\nFailed to update postcode:")
            print(f"- {response.failed_postcodes[0]}")
            print(f"Error: {response.message}")
    except grpc.RpcError as e:
        print(f"Error: {e.details()}")

def main():
    parser = argparse.ArgumentParser(description='Weather Service Client')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Get weather command
    get_parser = subparsers.add_parser('get', help='Get weather information')
    get_parser.add_argument('postal_code', help='Postal code to get weather information')

    # Update weather command
    update_parser = subparsers.add_parser('update', help='Update weather information')
    update_parser.add_argument('postal_codes', nargs='+', help='One or more postal codes to update')

    args = parser.parse_args()

    channel = grpc.insecure_channel('localhost:50051')
    stub = WeatherServiceStub(channel)

    try:
        if args.command == 'get':
            get_weather(stub, args.postal_code)
        elif args.command == 'update':
            update_weather(stub, args.postal_codes)
        else:
            parser.print_help()
    finally:
        channel.close()

if __name__ == '__main__':
    main()