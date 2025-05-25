import cherrypy
import os

# Import project configurations
from config import settings

# Import previously created controllers
# from controllers import root as root_controller # root.py was created, but IndexController handles '/'
from controllers import index_controller
from controllers import example_controller
# from controllers import error_controller # Error handling can be configured later
from controllers import api_controller # Contains ApiInfoV1, ApiInfoV2, ApiVersion

# The Root class from the template is not strictly necessary if IndexController handles '/'
# class Root:
#     @cherrypy.expose
#     def index(self):
#         return "Welcome to the CherryPy version of the application!"

if __name__ == '__main__':
    # Apply global CherryPy configuration from settings.py
    # This should contain {'server.socket_host': '0.0.0.0', 'server.socket_port': 8080, ...}
    global_conf = settings.CHERRYPY_CONFIG.get('global', {})
    cherrypy.config.update(global_conf)

    # Mount the IndexController at the root path '/'
    # The config passed to mount can be specific for this mount point
    mount_config_index = {
        '/': {
            'tools.sessions.on': True, # Example: Enable sessions for the index controller
            # Add other specific configurations for this mount point if needed
        }
    }
    cherrypy.tree.mount(index_controller.IndexController(), '/', config=mount_config_index)

    # Mount the ExampleController at '/example'
    # It can use parts of CHERRYPY_CONFIG if structured appropriately, or specific config.
    # For now, we assume settings.CHERRYPY_CONFIG might contain a section for '/example' or global settings apply.
    cherrypy.tree.mount(example_controller.ExampleController(), '/example', config=settings.CHERRYPY_CONFIG)

    # Mount API controllers
    # These might require MethodDispatcher if their methods are GET, POST etc.
    # This should be part of their configuration in settings.CHERRYPY_CONFIG or passed here.
    # Example for one API, assuming CHERRYPY_CONFIG in settings.py has appropriate sections:
    # config_api_v1 = settings.CHERRYPY_CONFIG.get('/api/info/v1', {})
    # if 'request.dispatch' not in config_api_v1: # Ensure MethodDispatcher if needed
    #     config_api_v1['request.dispatch'] = cherrypy.dispatch.MethodDispatcher()
    
    # Mounting API controllers as per the template structure
    # The CHERRYPY_CONFIG from settings.py should ideally contain configurations
    # for these specific paths if they need special dispatchers (like MethodDispatcher).
    cherrypy.tree.mount(api_controller.ApiInfoV1(), '/api/info/v1', config=settings.CHERRYPY_CONFIG)
    cherrypy.tree.mount(api_controller.ApiInfoV2(), '/api/info/v2', config=settings.CHERRYPY_CONFIG)
    cherrypy.tree.mount(api_controller.ApiVersion(), '/api/version', config=settings.CHERRYPY_CONFIG)
    
    # In settings.py, CHERRYPY_CONFIG could look like:
    # CHERRYPY_CONFIG = {
    #     'global': {...},
    #     '/api/info/v1': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(), ...},
    #     '/api/info/v2': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(), ...},
    #     '/api/version': {'request.dispatch': cherrypy.dispatch.MethodDispatcher(), ...},
    #     ...
    # }
    # If not, MethodDispatcher might need to be explicitly set here for API controllers, e.g.:
    # api_default_conf = {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    # cherrypy.tree.mount(api_controller.ApiInfoV1(), '/api/info/v1', config={'/':api_default_conf})


    # Configure static file serving for the '/static' path
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    static_config = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': static_dir,
            'tools.staticdir.index': 'index.html', # Optional: serves index.html for /static/
            # 'tools.staticdir.content_types': {'css': 'text/css', 'js': 'application/javascript'} # Example
        }
    }
    cherrypy.tree.mount(None, '/static', config=static_config)
    
    # Error handling (can be refined later)
    # Example: To use the ErrorController for 404 errors:
    # from controllers import error_controller as err_ctrl_module
    # custom_error_controller = err_ctrl_module.ErrorController()
    # cherrypy.config.update({'error_page.404': custom_error_controller.index})
    # Note: error_controller.index method signature needs to match what CherryPy error dispatch expects
    # or adapt it. The current error_controller.index(code, message) is not directly compatible.
    # A wrapper function might be needed. For now, rely on default CherryPy error pages.

    # Start the CherryPy server engine
    cherrypy.engine.start()
    cherrypy.engine.block()
