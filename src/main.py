from lb import start_load_balancer
from handle_client import handle_client
from backend_servers import setup_backend_servers


if __name__ == "__main__":
    algorithm = input("Select load balancing algorithm (round-robin, least-connections, weighted-round-robin, ip-hash, random): ")
    start_load_balancer(8080, setup_backend_servers(), algorithm)

    input("Press Enter to exit...")
