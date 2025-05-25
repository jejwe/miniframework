import unittest
import cherrypy
from cherrypy.test import helper
import json

# Import controllers to be tested
from python_app.controllers import index_controller
from python_app.controllers import api_controller

# It's generally better not to import the main app.py in unit tests
# to avoid running the full application setup (global config, all mounts)
# unless specifically testing the integrated application.
# For unit testing controllers, mount them individually.

class TestIndexController(helper.CPWebCase):
    @staticmethod
    def setup_server():
        # Mount only the IndexController for this test case
        cherrypy.tree.mount(index_controller.IndexController(), '/', config={
            '/': {
                # Add any specific config for IndexController if needed for tests
                # e.g., 'tools.sessions.on': True, if session usage is tested
            }
        })

    def test_index_page(self):
        self.getPage("/")
        self.assertStatus('200 OK')
        # If IndexController.index explicitly sets content type, test it.
        # Otherwise, CherryPy's default for string is text/html;charset=utf-8
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')
        self.assertInBody("Index Page Content")

class TestApiController(helper.CPWebCase):
    @staticmethod
    def setup_server():
        # Mount only the ApiInfoV1 controller for this test case
        # The ApiInfoV1.GET method is named 'GET' and returns a dict,
        # so MethodDispatcher and json_out tool are essential.
        conf = {
            '/': {
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                'tools.json_out.on': True
            }
        }
        cherrypy.tree.mount(api_controller.ApiInfoV1(), '/api/info/v1', config=conf)

    def test_api_info_v1_get(self):
        self.getPage("/api/info/v1") # This will hit ApiInfoV1.GET
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'application/json')
        
        expected_response = {"code": 200, "message": "success", "data": "Hello World!"}
        
        # self.body is bytes, so decode and load with json
        response_data = json.loads(self.body.decode('utf-8'))
        self.assertEqual(response_data, expected_response)

if __name__ == '__main__':
    # This allows running the tests directly from this file
    unittest.main()
