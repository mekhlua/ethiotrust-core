@'
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

port = 8080
print(f"Starting dashboard server at http://localhost:{port}")
print("Open your browser to http://localhost:8080/dashboard.html")
HTTPServer(("0.0.0.0", port), CORSRequestHandler).serve_forever()
'@ | Out-File -FilePath server.py -Encoding UTF8