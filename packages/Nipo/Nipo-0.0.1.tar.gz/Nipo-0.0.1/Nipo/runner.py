from http.server import BaseHTTPRequestHandler
from .urls import urls
class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = None
        for pathD in urls:
            if pathD[0] == self.path:
                message = pathD[1]()
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        if message != None:
            self.wfile.write(message.res)
        else:
            self.wfile.write("<h1>ERROR: THE URL IS INVALID</h1>")

def main(host="localhost",port=8080):
    from http.server import HTTPServer
    server = HTTPServer((host, port), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()