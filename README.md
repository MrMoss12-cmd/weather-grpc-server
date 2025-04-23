# Weather gRPC Microservice

![Weather Service Architecture](https://i.ibb.co/9HG9P78K/cli.jpg)

A high-performance weather data microservice using gRPC for efficient communication between services.

## Screenshots

![Starter Service](https://i.ibb.co/L4yWwsm/Captura-de-pantalla-2025-04-22-202924.png)
![Requested Service](https://i.ibb.co/1ffCBK4f/Captura-de-pantalla-2025-04-22-202857.png)

## Features

- **Real-time weather data** retrieval by postal code
- **Batch updates** for multiple locations
- **gRPC interface** for high-performance communication
- **REST API integration** with weather data sources
- **Command-line client** for easy interaction

## Technology Stack

- Python 3.9+
- gRPC & Protocol Buffers
- FastAPI (for REST interface)
- SQLAlchemy (ORM)
- MySQL (Database)
- Requests (HTTP client)

## Project Structure

 ```
```plaintext
weather-grpc/
├── weather_grpc_server/       # gRPC server implementation
│   ├── server.py              # Main server logic
│   ├── weather_pb2.py         # Generated protobuf classes
│   ├── weather_pb2_grpc.py    # Generated gRPC service classes
│   └── protos/                # Protocol Buffer definitions
├── weather_orm_service/       # ORM service (if separate)
└── client/                   # Command-line client
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- MySQL (or your preferred database)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/eliashiguera/weather-grpc.git
cd weather-grpc
 ```
```

2. Set up virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
 ```

3. Generate gRPC stubs (if needed):
```bash
python -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/weather.proto
 ```
```

### Running the Services
1. Start the ORM service:
```bash
cd weather_orm_service
uvicorn main:app --reload
 ```

2. Start the gRPC server (in another terminal):
```bash
cd weather_grpc_server
python server.py
 ```

3. Use the client:
```bash
cd client
python client.py get 080001  # Get weather for postal code
python client.py update 080001 470001 130001  # Update multiple locations
 ```
```

## API Documentation
### gRPC Service Methods
- GetWeather(postal_code) - Returns weather data for a single location
- UpdateWeather(postal_codes) - Updates weather data for multiple locations
See protos/weather.proto for full service definition.

## Contributing
1. Fork the project
2. Create your feature branch ( git checkout -b feature/AmazingFeature )
3. Commit your changes ( git commit -m 'Add some AmazingFeature' )
4. Push to the branch ( git push origin feature/AmazingFeature )
5. Open a Pull Request
## License
Distributed under the MIT License. See LICENSE for more information.
