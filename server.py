import grpc
from concurrent import futures
import requests
from weather_pb2 import WeatherResponse, UpdateWeatherResponse
from weather_pb2_grpc import WeatherServiceServicer, add_WeatherServiceServicer_to_server

class WeatherService(WeatherServiceServicer):
    def GetWeather(self, request, context):
        try:
            # Call the ORM API
            response = requests.get(f'http://localhost:8000/weather/{request.postal_code}')
            data = response.json()
            
            # Create gRPC response with the actual data structure
            return WeatherResponse(
                postcode=data.get('postcode', ''),
                subdiv_name=data.get('subdiv_name', ''),
                feels_like=float(data.get('feels_like', 0.0)),
                rel_hum=int(data.get('rel_hum', 0)),
                temp=float(data.get('temp', 0.0)),
                wind_dir=int(data.get('wind_dir', 0)),
                timestamp=data.get('timestamp', '')
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error: {str(e)}')
            return WeatherResponse()

    def UpdateWeather(self, request, context):
        updated_postcodes = []
        failed_postcodes = []

        try:
            postal_codes = [str(code) for code in request.postal_codes]
            print("\nDebug - Incoming request:")
            print(f"Postal codes to update: {postal_codes}")
            
            # Format request data
            request_data = {"postal_codes": postal_codes}
            
            response = requests.post(
                'http://localhost:8000/weather/update',
                json=request_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Response status: {response.status_code}")
            print(f"Raw response: {response.text}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"Parsed response: {response_data}")
                
                # Handle successful updates
                if isinstance(response_data, dict):
                    if 'updated' in response_data:
                        updated_postcodes = response_data['updated']
                    else:
                        updated_postcodes = postal_codes
                    
                    if 'failed' in response_data:
                        failed_postcodes = response_data['failed']
            else:
                failed_postcodes = postal_codes
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            failed_postcodes = postal_codes

        result = UpdateWeatherResponse(
            updated_postcodes=updated_postcodes,
            failed_postcodes=failed_postcodes,
            message=f"Updated: {len(updated_postcodes)}, Failed: {len(failed_postcodes)}"
        )
        print(f"Sending response: {result}")
        return result

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WeatherServiceServicer_to_server(WeatherService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()