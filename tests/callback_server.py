import json
import cyclone.web
from twisted.application import service, internet

class HttpHandler(cyclone.web.RequestHandler):

    def _load_request_body_as_json(self):
        return json.loads(self.request.body)

    def post(self):
        doc = self._load_request_body_as_json()
        print doc

        doc_is_done = doc.get('done')
        grains_key = doc.get('grains_keys')
        if doc_is_done:
            doc_status = "done"
        else:
            doc_status = "not done"
        self.write("Document with uid %s is %s.\n" % (doc.get('doc_key'), doc_status))
        self.write("Document grains keys: %s" % str(grains_key))

class FileHandler(cyclone.web.RequestHandler):

    def get(self):
        video =  open('input/26images-1table.odt')
        video_data = video.read()
        video.close()

        self.write(video_data)
        self.finish()


class CallbackService(cyclone.web.Application):

    def __init__(self):
        handlers = [
            (r"/", HttpHandler),
            (r"/26images-1table.odt", FileHandler),
        ]

        settings = {
                'xheaders':True,
                }

        cyclone.web.Application.__init__(self, handlers, **settings)

application = service.Application("Callback Service")
srv = internet.TCPServer(8887, CallbackService(), interface='0.0.0.0')
srv.setServiceParent(application)

