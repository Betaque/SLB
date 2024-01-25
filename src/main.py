import hashlib
import random
import socket
import threading
import requests

def round_robin_load_balancer(request_count, servers):
    return servers[request_count % len(servers)]

def least_connections_load_balancer(connections_count, servers):
    return min(servers, key=connections_count.get)

def weighted_round_robin_load_balancer(request_count, servers, weights):
    total_weight = sum(weights)
    cumulative_weights = [sum(weights[:i + 1]) for i in range(len(weights))]
    index = request_count % total_weight
    selected_server = next(server for server, weight in zip(servers, cumulative_weights) if weight > index)
    return selected_server

def ip_hash_load_balancer(client_ip, servers):
    hashed_index = int(hashlib.md5(client_ip.encode()).hexdigest(), 16) % len(servers)
    return servers[hashed_index]

def random_load_balancer(servers):
    return random.choice(servers)

def load_balancer(request_count, client_ip, connections_count, servers, algorithm, lock):
    if algorithm == 'round-robin':
        selected_server = round_robin_load_balancer(request_count[0], servers)
    elif algorithm == 'least-connections':
        selected_server = least_connections_load_balancer(connections_count, servers)
    elif algorithm == 'weighted-round-robin':
        weights = [2, 1, 3]  # Replace with actual weights
        selected_server = weighted_round_robin_load_balancer(request_count[0], servers, weights)
    elif algorithm == 'ip-hash':
        selected_server = ip_hash_load_balancer(client_ip, servers)
    elif algorithm == 'random':
        selected_server = random_load_balancer(servers)
    else:
        raise ValueError("Unsupported load balancing algorithm")

    # Handle HTTP/HTTPS endpoints
    server_address, server_port = selected_server
    if server_address.startswith("http://") or server_address.startswith("https://"):
        response = requests.get(server_address)
        print(f"Request {request_count[0] + 1} directed to {selected_server} with response: {response.text}")
    else:
        with lock:
            connections_count[selected_server] += 1

        print(f"Forwarding request to backend server {selected_server}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect(selected_server)
            data = client_socket.recv(1024)
            server_socket.sendall(data)

            response = server_socket.recv(1024)
            client_socket.sendall(response)

        with lock:
            connections_count[selected_server] -= 1

    return selected_server

def handle_client(client_socket, request_count, connections_count, servers, algorithm, lock):
    client_address = client_socket.getpeername()
    print(f"Accepted connection from {client_address}")

    selected_server = load_balancer(request_count, client_address[0], connections_count, servers, algorithm, lock)

    client_socket.close()

def start_load_balancer(listen_port, backend_servers, algorithm='round-robin'):
    request_count = [0]
    connections_count = {server: 0 for server in backend_servers}
    lock = threading.Lock()

    def listen_for_clients():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lb_socket:
            lb_socket.bind(('0.0.0.0', listen_port))
            lb_socket.listen()

            print(f"Load Balancer listening on port {listen_port} with {algorithm} algorithm")

            while True:
                client_socket, _ = lb_socket.accept()
                threading.Thread(target=handle_client, args=(client_socket, request_count, connections_count, backend_servers, algorithm, lock), daemon=True).start()

    threading.Thread(target=listen_for_clients, daemon=True).start()

if __name__ == "__main__":
    # Replace the backend server information with your actual backend servers
    backend_servers = [("http://google.com", 80), ("http://google.com", 80), ("http://google.com", 80)]
    
    algorithm = input("Select load balancing algorithm (round-robin, least-connections, weighted-round-robin, ip-hash, random): ")
    start_load_balancer(8080, backend_servers, algorithm)

    input("Press Enter to exit...")
