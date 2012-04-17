import unittest
from os.path import dirname, abspath, join
from json import dumps, loads
from base64 import b64encode
from restfulie import Restfulie
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.Lipsum import Lipsum
from funkload.utils import Data


FOLDER_PATH = abspath(dirname(__file__))


class DocumentGranulateBench(FunkLoadTestCase):
    """This test use a configuration file Simple.conf."""

    def __init__(self, *args, **kwargs):
        FunkLoadTestCase.__init__(self, *args, **kwargs)
        """Setting up the benchmark cycle."""
        self.server_url = self.conf_get('main', 'url')
        self.user = self.conf_get('main', 'user')
        self.password = self.conf_get('main', 'password')
        self.cloudooo = Restfulie.at(self.server_url).auth(self.user, self.password).as_('application/json')
        self.lipsum = Lipsum()
        self.uid_list = []
        self.document = b64encode(open(join(FOLDER_PATH, 'input', '26images-1table.odt')).read())

    def test_convert(self):
        server_url = self.server_url
        self.setBasicAuth(self.user, self.password)

        # The description should be set in the configuration file

        body = dumps({'doc': self.document, 'filename': 'test.odt'})

        # begin of test ---------------------------------------------
        self.post(server_url, description='Send many docs with 1mb each.',
                  params=Data('application/json', body))
        response = loads(self.getBody())
        self.uid_list.extend(response["grains_keys"]["images"])
        self.uid_list.extend(response["grains_keys"]["files"])
        self.uid_list.extend(response["doc_key"])
        # end of test -----------------------------------------------

    def tearDown(self):
        for uid in self.uid_list:
            self.sam.delete(key=uid)


if __name__ in  ('__main__', 'main'):
       unittest.main()
