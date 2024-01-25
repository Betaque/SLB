# Self-Managed Load Balancer (SLB)

This project implements a custom load balancer using Python and Flask. The load balancer distributes incoming requests among specified backend servers based on different load balancing algorithms.

## Getting Started

### Prerequisites

- Python 3.x
- Flask

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/custom-load-balancer.git
   ```

2. Install Dependencies 

   ```bash
   pip3 install flask
   ```

## Configurations

#### Open the backend_servers.py file and specify the backend servers to be used by the load balancer.

   ```bash
   backend_servers = [
    ("localhost", 8081),
    ("localhost", 8082),
    # Add more servers as needed
    ]
   ```

## Usage

### 1. Run the Loadbalancer Server

   ```bash
   python3 src/main.py
   ```

### 2. Select a load balancing algorithm as prompted.

### 3. Access the load balancer at http://127.0.0.1:8080/ to see the load-balanced responses.


## Load Balancing Algorithms

1. Round Robin: Requests are distributed evenly among backend servers.
2. Least Connections: Traffic is directed to the server with the fewest active connections.
3. Weighted Round Robin: Servers are assigned weights, and traffic is distributed based on these weights. (weights can be configured in algorithms.py)
4. IP Hash: Client's IP address is used to determine the target server.
5. Random: Requests are randomly directed to one of the available servers.
