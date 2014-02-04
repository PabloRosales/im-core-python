from werkzeug.wrappers import BaseResponse
from im.core.templates.mako import Template

class Response(BaseResponse):
    def __init__(self, content=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False, controller=None):
        response = None
        if not controller:
            response = content
        else:
            response = prepare_response(controller, status, content)
            
        super(Response, self).__init__(response, status, headers, mimetype, content_type, direct_passthrough)
        
    def prepare_response(self, controller, status, content):
        if not controller.layouts or not controller.layouts[status]:
            return content
        
        layout_template = controller.layouts[status]
        
        print "LAYOUT"
        print layout_template
        
        print "TEMPLATE"
        print Template(layout_template, {})
