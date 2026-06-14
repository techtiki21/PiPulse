import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import psutil

# modify to your choosing
PORT = 8000 

class agent(BaseHTTPRequestHandler):
    def sendData(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):  # overrides BaseHTTPRequestHandler func
        parsedURL = urlparse(self.path) 
        queryParams = parse_qs(parsedURL.query)
        data = {}
        if parsedURL.path == '/stats':
            data = {
                'cpuPercent': psutil.cpu_percent(interval=1),
                'ramUsage': psutil.virtual_memory().percent,
                'diskUsage': psutil.disk_usage('/').percent
            }
        elif parsedURL.path == '/disk':
            disk = psutil.disk_usage('/')
            data = {
                'total': f"{disk.total / (1024**3):.2f}",
                'used': f"{disk.used / (1024**3):.2f}",
                'free': f"{disk.free / (1024**3):.2f}",
                'percent': disk.percent
            }
        elif parsedURL.path == '/memory':
            ram = psutil.virtual_memory()
            data = {
                'total': f"{ram.total / (1024**3):.2f}",
                'used': f"{ram.used / (1024**3):.2f}",
                'available': f"{ram.available / (1024**3):.2f}",
                'percent': ram.percent
            }
        elif parsedURL.path == '/cpu':
            seconds = int(queryParams.get("seconds", ["1"])[0])
            coreUsage = psutil.cpu_percent(interval=seconds, percpu=True)
            data = {
                'count': psutil.cpu_count(),
                'physical': psutil.cpu_count(logical=False),
                'usage': round(sum(coreUsage) / len(coreUsage), 2),
                'coreUsage': coreUsage
            }
        else:
            self.send_response(404)
            self.end_headers()
        self.sendData(data)

    
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