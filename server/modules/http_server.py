import os
try:
    from . import utils
except:
    import utils

http_server=None


# PORT = 8080
# Handler = http.server.SimpleHTTPRequestHandler

# class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.path = os.path.join(utils.get_current_dir(__file__),'../../web')
#         return http.server.SimpleHTTPRequestHandler.do_GET(self)

# # Create an object of the above class
# handler_object = MyHttpRequestHandler


# with socketserver.TCPServer(("", PORT), handler_object) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()

def start():
    global http_server
    if http_server==None:
        http_server=os.popen('cd '+os.path.join(utils.get_current_dir(__file__),'../../web')+' && python3 -m http.server')
        # http_server=os.popen('')
        os.popen('start http://localhost:8000/magic-card.html')
    return  

# def stop_http_server():
#     global http_server
#     if http_server:
#         http_server.close()
