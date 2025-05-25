import cherrypy

class Root:
    @cherrypy.expose
    def index(self):
        return "Hello from Root controller's index method!"

    @cherrypy.expose
    def example_route(self, id_param):
        # This demonstrates a method that takes a parameter.
        # If this controller is mounted at '/examplec',
        # a URL like /examplec/example_route/123
        # would call this method with id_param = "123".
        return f"Example_route called with id_param: {id_param}"

# Example of how this might be mounted in a main application file (e.g., app.py)
# if __name__ == '__main__':
#     config = {'global': {'server.socket_host': '0.0.0.0',
#                          'server.socket_port': 8080}}
#     cherrypy.quickstart(Root(), '/', config=config)
