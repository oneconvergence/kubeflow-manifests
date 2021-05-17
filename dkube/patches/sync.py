from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Controller(BaseHTTPRequestHandler):
    def sync(self, parent, children):
        return {"status": {}, "children": []}


    def do_POST(self):
        # Serve the sync() function as a JSON webhook.
        observed = json.loads(
            self.rfile.read(int(self.headers.get("content-length"))))
        desired = self.sync(observed["parent"], observed["children"])

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(desired), 'utf-8'))


HTTPServer(("", 8080), Controller).serve_forever()