from algorithms import load_balancer

def handle_client(client_socket, request_count, connections_count, servers, algorithm, lock):
    client_address = client_socket.getpeername()
    print(f"Accepted connection from {client_address}")

    response_content = load_balancer(request_count, client_address[0], connections_count, servers, algorithm, lock)

    # Send the response to the client's browser
    client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response_content.encode())

    client_socket.close()
