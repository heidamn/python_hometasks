import asyncore
import asynchat
import argparse
import logging
import mimetypes
import multiprocessing
import os
from urllib.parse import urlparse, unquote
from time import strftime, gmtime
import email
import re
from io import StringIO


def url_normalize(path):
    print( 'url_normalize')
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1 + 3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = unquote(path)
    return path


class FileProducer(object):

    def __init__(self, file, chunk_size=4096):
        print( 'FileProducer init')
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        print( 'FileProducer more')
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class AsyncHTTPServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=8888, handler_class=None):
        print( 'AsyncHTTPServer init')
        super().__init__()
        self.handler_class = handler_class
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def serve_forever(self):
        print( 'AsyncHTTPServer serve_forever')
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            logging.debug("Worker shutdown.")
        finally:
            self.close()

    def handle_accepted(self, sock, address):
        print( 'AsyncHTTPServer handle_accepted')
        
        logging.debug(address,  "connected.")
        self.handler_class(sock) 


class AsyncHTTPRequestHandler(asynchat.async_chat):
    

    def __init__(self, sock):
        print( 'AsyncHTTPRequestHandler init')
        super().__init__(sock) 
        self.ibuffer = '' 
        self.obuffer = b'' 
        self.set_terminator(b'\r\n\r\n') 
        self.headings_were_parsed = False 
        self.request = '' 
        self.headers = {} 
        self.response = '' 

    def collect_incoming_data(self, data):
        print( 'AsyncHTTPRequestHandler collect_incoming_data')
        if self.headings_were_parsed:
            self.obuffer = data
        else:
            self.ibuffer += data.decode('utf-8')

    def found_terminator(self):
        print( 'AsyncHTTPRequestHandler found_terminator')
        self.parse_request()

    def parse_request(self):
        print( 'AsyncHTTPRequestHandler parse_request')
        if not self.headings_were_parsed:
            self.headings_were_parsed = True  
            request, headers = self.ibuffer.split('\r\n', 1)
            self.parse_headers(headers)
            self.headers['method'], self.headers['path'], self.headers['protocol'] = request.split()
            self.headers['path'] = url_normalize(self.headers['path'])
            if self.headers['method'] == 'POST':
                clen = self.headers['Content-Length']  
                print(self.headers, '\n')
                print(clen, '\n')
                if clen == '0':  
                    print(clen , '\n')
                    self.send_error(400)
                    logging.debug("400 ERROR")
                    return
                self.set_terminator(int(clen)) 
            else:                                                           
                self.request = urlparse('http://' + self.headers['Host'] + self.headers['path']).path
                self.ibuffer = ''
                print(self.headers, '\n')
                self.handle_request()
        else:
            self.request = urlparse('http://' + self.headers['Host'] + self.headers['path']).path
            self.ibuffer = ''
            self.handle_request()

    def parse_headers(self, headers):
        print( 'AsyncHTTPRequestHandler parse_headers')
        message = email.message_from_file(StringIO(headers))
        self.headers = dict(message.items())

    def handle_request(self):
        print( 'AsyncHTTPRequestHandler handle_request')
        method_name = 'do_' + self.headers['method']
        if not hasattr(self, method_name):
            self.send_error(405)
            return
        handler = getattr(self, method_name)
        handler()

    def do_GET(self):
        print( 'AsyncHTTPRequestHandler do_GET')
        f = self.send_headers()
        if f:
            resp = bytes(self.response.encode('utf-8')) + f
            self.send(resp)
            self.close()

    def do_HEAD(self):
        print( 'AsyncHTTPRequestHandler do_HEAD')
        f = self.send_headers()
        if f:
            resp = bytes(self.response.encode('utf-8'))
            self.send(resp)
            self.close()

    def do_POST(self):
        print( 'AsyncHTTPRequestHandler do_POST')
        self.init_response(200, "OK")
        self.add_header("Content-Type", self.headers['Content-Type'])
        self.add_header("Connection", "close")
        self.add_header("Content-Length", self.headers['Content-Length'])
        self.end_headers()
        resp = bytes(self.response.encode('utf-8')) + self.obuffer
        self.send(resp)
        self.close()

    def send_headers(self):
        print( 'AsyncHTTPRequestHandler send_head')
        path = url_normalize(os.getcwd() + self.request)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
            if not os.path.exists(path):
                self.send_error(403)
                return None
        try:
            file = bytes()
            fp = FileProducer(open(path, 'rb'))
            while True:
                cur_chunk = fp.more()
                if not cur_chunk:
                    break
                file += cur_chunk
        except IOError:
            self.send_error(404)
            return None

        _, ext = os.path.splitext(path)
        ctype = mimetypes.types_map[ext.lower()]

        self.init_response(200)
        self.add_header("Server", "server")
        self.add_header("Date", "date")
        self.add_header("Content-Type", ctype)
        self.add_header("Content-Length", os.path.getsize(path))
        self.end_headers()
        return file
        
    def send_error(self, code, message=None):
        print( 'AsyncHTTPRequestHandler send_error')
        print(code, 'ERROR happend.' '\n')
        try:
            short_msg, long_msg = self.responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg
        self.init_response(code, message)
        self.add_header("Content-Type", "text/plain")
        self.add_header("Connection", "close")
        self.end_headers()
        self.send(bytes(self.response.encode('utf-8')))
        self.close()
        
    def init_response(self, code, message=None):
        print( 'AsyncHTTPRequestHandler init_response')
        self.response = f'HTTP/1.1 {code} {message}\r\n'

    def add_header(self, keyword, value):
        print( 'AsyncHTTPRequestHandler add_header')
        self.response += f"{keyword}: {value}\r\n"

    def end_headers(self):
        print( 'AsyncHTTPRequestHandler end_headers')
        self.response += "\r\n"
        print(self.response)


    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
    }


def parse_args():
    print( 'parse_args')
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=8888)
    parser.add_argument("--log", dest="loglevel", default="debug")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default=".")
    return parser.parse_args()

def run():
    print( 'run')
    server = AsyncHTTPServer(host=args.host, port=args.port, handler_class=AsyncHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    args = parse_args()

    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")
    log = logging.getLogger(__name__)

    DOCUMENT_ROOT = args.document_root
    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run)
        p.start()
