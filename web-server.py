# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import threading
import os
import subprocess

hostName = "185.193.143.115"
serverPort = 80

with open('assets/view.html', 'r') as f:
    html = f.read()

class MyServer(BaseHTTPRequestHandler):
    def argv_parser(self, prms):
        parsed = {}
        if b'buttonDirection' in prms.keys():
            parsed['directionArgv'] = '-R'
        else:
            parsed['directionArgv'] = ''
        if b'formTrafficValue' in prms.keys():
            parsed['trafficValueArgv'] = int(prms[b'formTrafficValue'][0]) * 1048576
        else:
            parsed['trafficValueArgv'] = 209715200
        if b'formTrafficTimer' in prms.keys():
            parsed['trafficTimerArgv'] = int(prms[b'formTrafficTimer'][0]) * 60
        else:
            parsed['trafficTimerArgv'] = 86400
        return parsed

    def iperf_runner(self, params_dict):
        os.system(f"iperf3 -c 213.87.200.65 -p 63400 {params_dict['directionArgv']} -b {params_dict['trafficValueArgv']} -t {params_dict['trafficTimerArgv']} > iperf-log.html")

    def do_GET(self):
        print("GET request, path:", self.path)
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))
        elif self.path.endswith(".js"):
            self.send_response(200)
            self.send_header('Content-type', 'text/js')
            self.end_headers()
            with open(os.curdir + os.sep + 'assets' + self.path, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.endswith(".css"):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open(os.curdir + os.sep + 'assets' + self.path, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/check':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            result = subprocess.run(['pgrep', 'iperf3'], stdout=subprocess.PIPE)
            try:
                answer = int(result.stdout)
            except ValueError:
                answer = ''
            self.wfile.write(json.dumps({'answer': answer}).encode('utf-8'))
        elif self.path == '/stop':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            result = subprocess.run(['pgrep', 'iperf3'], stdout=subprocess.PIPE)
            try:
                answer = int(result.stdout)
                os.system(f'sudo kill {answer}')
                print(answer)
                answer = 'stopped successfull'
            except ValueError:
                answer = ''
            self.wfile.write(json.dumps({'answer': answer}).encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = parse_qs(body, encoding='utf-8')
        sys_arguments = self.argv_parser(params)
        print("POST request, path:", self.path, "body:", body.decode('utf-8'))
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(sys_arguments).encode('utf-8'))
            threading.Thread(target = self.iperf_runner, args = (sys_arguments,)).start()
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    if hostName:
        printHost = hostName
    else:
        printHost = '185.193.143.115'
    if serverPort == 80:
        printPort = ''
    else:
        printPort = f":{serverPort}"
    print(f"Server started at http://{printHost}{printPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
