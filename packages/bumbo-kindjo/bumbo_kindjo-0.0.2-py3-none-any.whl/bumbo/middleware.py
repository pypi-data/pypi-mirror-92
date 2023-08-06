from webob import Request

class Middleware:
    # it should wrap the WSGI app
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)

    # Should have the ability to add another middleware to the stack
    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    # main method for request processing
    def process_request_called(self, req):
        pass

    # main method for response processing
    def process_response(self, req, resp):
        pass

    # the method that handles incoming requests
    def handle_request(self, request):
        # do something with the request
        self.process_request(request)
        # delegates the response creation to the wrapped app
        response = self.app.handle_request(request)
        # calls the process_response to do something with the resp object
        self.process_response(request, response)
        # returns the response upwards
        return response