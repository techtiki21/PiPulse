import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import psutil

class agent(BaseHTTPRequestHandler):
    def do_GET(self):  # overrides BaseHTTPRequestHandler func
        if self.path == '/stats':
            utilization = {
                'cpuPercent': psutil.cpu_percent(interval=0.5),
                'ramUsage': psutil.virtual_memory().percent,
                'diskUsage': psutil.disk_usage('/').percent
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(utilization).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

PORT = input("What port would you like PiPulse to listen on (default 8080): ")
try:
    PORT = int(PORT)
except ValueError:
    print("Must be a number. Setting port to default 8080.")
    PORT = 8080
    
def run_server():
    # listen on all network interfaces
    serverAddress = ('', int(PORT))  
        
    # init the server with custom traffic rules
    httpd = HTTPServer(serverAddress, agent)
    print(f"running and listening on port {PORT}...")
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()