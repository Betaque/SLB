import threading
from flask import Flask, render_template_string
from algorithms import load_balancer

app = Flask(__name__)


def start_load_balancer(listen_port, backend_servers, algorithm='round-robin'):
    request_count = [0]
    connections_count = {server: 0 for server in backend_servers}
    lock = threading.Lock()

    @app.route("/")
    def index():
        selected_server = load_balancer(request_count, "127.0.0.1", connections_count, backend_servers, algorithm, lock)
        return render_template_string(selected_server)

    threading.Thread(target=app.run, kwargs={"port": listen_port}, daemon=True).start()

    print(f"Load Balancer serving on http://127.0.0.1:{listen_port}")