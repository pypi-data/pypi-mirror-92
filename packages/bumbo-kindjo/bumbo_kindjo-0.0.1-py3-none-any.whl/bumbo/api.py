import os
import inspect

from parse import parse
from webob import Request
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise

from .response import Response
from .middleware import Middleware


class API:
    # templates_dir were given a default value of "templates"
    def __init__(self, templates_dir="templates", static_dir="static"):
        # creates a dictionary
        # stores paths as keys and handlers as variables
        self.routes = {}

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )
        # variable that stores the exception handler
        self.exception_handler = None

        # the wsgi_app is wrapped with WhiteNoise and given a path to the static folder
        # static_dir was made configurable by making it an argument in the __init__ method
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
        
        # wrapped around self, which is a WSGI app
        self.middleware = Middleware(self)

    # runs every time the API class i called
    # the environ and start_response props come defaultly with the webob lib
    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if path_info.startswith("/static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    # Adding routes the Django way
    def add_route(self, path, handler, allowed_methods=None):
        assert path not in self.routes, "Such route already exists."

        # if allowed methods are not specified by the user, we're allowing all
        if allowed_methods is None:
            allowed_methods = ["get", "post", "put", "patch", "delete", "options"]

        # we're storing self.routes[path] as a dictionary
        self.routes[path] = {"handler": handler, "allowed_methods": allowed_methods}

    # a decorator that accepts a path and wraps the methods
    def route(self, path, allowed_methods=None):
        def wrapper(handler):
            self.add_route(path, handler, allowed_methods)
            return handler

        return wrapper

    # the default response in case of TypeError
    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, request_path):
        # iterates over the self route
        for path, handler_data in self.routes.items():
            # tries to parse data from URL
            parse_result = parse(path, request_path)
            if parse_result is not None:
                # returns the handler if the paths are the same
                return handler_data, parse_result.named
        # returns none if no handler is found
        return None, None

    # returns the response
    def handle_request(self, request):
        response = Response()

        handler_data, kwargs = self.find_handler(request_path=request.path)

        try:
            # checks if handler is valid
            if handler_data is not None:
                handler = handler_data["handler"]
                allowed_methods = handler_data["allowed_methods"]
                # checks if handler is a class
                if inspect.isclass(handler):
                    # if its a class-based handler it returns the first param
                    # it returns the attribute name to get as the second
                    # The third argument is the return value if nothing is found
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method not allowed", request.method)
                else:
                    if request.method.lower() not in allowed_methods:
                        raise AttributeError("Method not allowed", request.method)
                
                # if the handler_function was found, then call it
                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        # Checks and then calls the custom exception handler 
        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

        return response

    # to use the Requests WSGI Adapter, it needs to be mounted to a Session object
    # that way any request made using test_session, and using this url prefix
    # will use the RequestsWSGIAdapter
    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    # implementing the template method
    # "context" is set to None by default, checked and then assigned a value of {}
    # This is done because dict is a mutable object, and it is a bad practice to
    # set a mutable object as a default value
    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    # Exception handler method
    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)