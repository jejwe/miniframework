import cherrypy
import xml.etree.ElementTree as ET # For basic XML construction

class ApiInfoV1:
    """
    API for Info - Version 1.
    Equivalent to App/Api/Info.php
    """
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self): # Corresponds to the get() method in PHP
        # PHP: $this->response(200, 'success', 'Hello World!');
        cherrypy.response.status = 200
        return {
            "code": 200, # MiniFramework Rest::response puts code first
            "message": "success", # Renamed from 'status' for clarity if preferred
            "data": "Hello World!"
        }

class ApiInfoV2:
    """
    API for Info - Version 2.
    Equivalent to App/Api/Info_V2.php
    """
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def GET(self): # Corresponds to the get() method in PHP
        # PHP: $headers = $this->_request->getHeaders(); $info = 'Hello World!(V' . $headers['Ver'] . ')';
        # PHP: $this->response(200, 'success', $info);
        version_from_header = cherrypy.request.headers.get('Ver', 'Unknown')
        data_message = f"Hello World!(V{version_from_header})"
        cherrypy.response.status = 200
        return {
            "code": 200,
            "message": "success",
            "data": data_message
        }

class ApiVersion:
    """
    API for Version information.
    Equivalent to App/Api/Version.php
    
    This class's methods (GET, POST, PUT, DELETE) are intended to be dispatched
    by CherryPy's MethodDispatcher if the class instance is mounted directly.
    e.g. conf = {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
             cherrypy.tree.mount(ApiVersion(), '/api/version', conf)
    """

    def __init__(self):
        """
        Equivalent to _init() in PHP.
        """
        # do something...
        pass

    @cherrypy.expose
    def GET(self, type='json'):
        # PHP: $version = '1.0.0'; $type = $this->params->getParam('type');
        version = '1.0.0'
        
        if type == 'json':
            # PHP: $this->type('json')->response(200, 'success', $version);
            cherrypy.response.headers['Content-Type'] = 'application/json'
            cherrypy.response.status = 200
            # Using json_out tool, so just return the dict
            return {
                "code": 200,
                "message": "success",
                "data": version
            }
        elif type == 'xml':
            # PHP: $this->type('xml')->response(200, 'success', ['version' => $version]);
            cherrypy.response.headers['Content-Type'] = 'application/xml'
            cherrypy.response.status = 200
            # Construct basic XML
            root = ET.Element("response")
            ET.SubElement(root, "code").text = "200"
            ET.SubElement(root, "message").text = "success"
            data_node = ET.SubElement(root, "data")
            ET.SubElement(data_node, "version").text = version
            return ET.tostring(root, encoding='unicode')
        else:
            raise cherrypy.HTTPError(400, "Invalid type parameter. Use 'json' or 'xml'.")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def POST(self, **params):
        # PHP: $params = $this->params->getParams(); $this->responseJson(201, 'success', $params);
        # CherryPy collects POST params into kwargs if expose is used like this.
        # For JSON body, one would use @cherrypy.tools.json_in() and cherrypy.request.json
        cherrypy.response.status = 201
        return {
            "code": 201,
            "message": "success",
            "data": params # Echo back received parameters
        }

    @cherrypy.expose
    def PUT(self):
        # PHP: $this->forbidden();
        raise cherrypy.HTTPError(403, "Forbidden")

    @cherrypy.expose
    def DELETE(self):
        # PHP: Commented out, implies 403 or method not found.
        # CherryPy would give 405 if MethodDispatcher is used and DELETE is defined but not allowed for some reason,
        # or 404 if the path itself is not found.
        # Raising 403 to match PHP's apparent intent for non-existent/disallowed method.
        raise cherrypy.HTTPError(403, "Forbidden - Method not implemented or allowed")

# Example mounting (would be in the main application script):
# if __name__ == '__main__':
#     config = {
#         'global': {
#             'server.socket_host': '0.0.0.0',
#             'server.socket_port': 8080,
#         },
#         # Config for MethodDispatcher for classes that define GET, POST, etc.
#         '/api/info/v1': {
#             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
#             'tools.response_headers.on': True,
#             'tools.response_headers.headers': [('Content-Type', 'application/json')]
#         },
#         '/api/info/v2': {
#             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
#             'tools.response_headers.on': True,
#             'tools.response_headers.headers': [('Content-Type', 'application/json')]
#         },
#         '/api/version': {
#             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
#             # Content-Type for /api/version is handled by the GET method itself
#         }
#     }
#     cherrypy.tree.mount(ApiInfoV1(), '/api/info/v1', config)
#     cherrypy.tree.mount(ApiInfoV2(), '/api/info/v2', config)
#     cherrypy.tree.mount(ApiVersion(), '/api/version', config)
#
#     cherrypy.engine.start()
#     cherrypy.engine.block()
