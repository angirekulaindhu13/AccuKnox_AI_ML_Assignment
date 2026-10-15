import json
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "127.0.0.1"
PORT = 8000

# These records are fabricated examples, not real student information.
STUDENTS = [
    {"student_name": "Sample Student 1", "test_score": 82},
    {"student_name": "Sample Student 2", "test_score": 91},
    {"student_name": "Sample Student 3", "test_score": 76},
    {"student_name": "Sample Student 4", "test_score": 88},
    {"student_name": "Sample Student 5", "test_score": 95},
]


class StudentAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/students":
            self.send_error(404, "Endpoint not found")
            return

        response_body = json.dumps(STUDENTS).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)


def main():
    server = HTTPServer((HOST, PORT), StudentAPIHandler)
    print(f"Synthetic student API available at http://{HOST}:{PORT}/students")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping synthetic student API")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()