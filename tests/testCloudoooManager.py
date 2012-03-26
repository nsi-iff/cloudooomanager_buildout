#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from xmlrpclib import Server
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from subprocess import call
from multiprocessing import Process
from time import sleep
from json import loads
from restfulie import Restfulie
from should_dsl import *

FOLDER_PATH = abspath(dirname(__file__))

class CloudoooManagerTest(unittest.TestCase):

    def setUp(self):
        self.cloudooo_service = Restfulie.at("http://localhost:8886/").auth('test', 'test').as_('application/json')
        self.sam = Restfulie.at('http://localhost:8888/').auth('test', 'test').as_('application/json')
        self.uid_list = []

    def testGranulation(self):
        input_doc = open(join(FOLDER_PATH,'input','26images-1table.odt'), 'rb').read()
        input_doc_convertion = open(join(FOLDER_PATH,'input','test.doc'), 'rb').read()
        b64_encoded_doc = b64encode(input_doc)
        b64_encoded_doc_convertion = b64encode(input_doc_convertion)

        uid = self.cloudooo_service.post(doc=b64_encoded_doc, filename='documento.odt', callback='http://localhost:8887/')
        doc_key = uid.resource().doc_key

        response_convertion = self.cloudooo_service.post(doc=b64_encoded_doc_convertion, filename='documento.doc', callback='http://localhost:8887/')
        doc_key_convertion = response_convertion.resource().doc_key

        self.uid_list.append({'doc_key':doc_key, 'images':26, 'files':1})
        self.uid_list.append({'doc_key':doc_key_convertion, 'images':4, 'files':1})

        for entry in self.uid_list:
            sleep(60)

            self.cloudooo_service.get(key=entry['doc_key']).resource() |should| be_done
            grains = loads(self.cloudooo_service.get(doc_key=entry['doc_key']).body)
            grains['images'] |should| have(entry['images']).images
            grains['files'] |should| have(entry['files']).file

    def testDownloadConvertion(self):

        uid_doc_download = self.cloudooo_service.post(doc_link='http://localhost:8887/26images-1table.odt', callback='http://localhost:8887/').resource().doc_key
        self.uid_list.append({'uid':uid_doc_download})

        sleep(10)

        granulation = self.cloudooo_service.get(key=uid_doc_download).resource()
        granulation |should| be_done

    def tearDown(self):
        for uid in self.uid_list:
            self.sam.delete(key=uid)

if __name__ == '__main__':
        cloudooomanager_ctl = join(FOLDER_PATH, '..', 'bin', 'cloudooomanager_ctl')
        worker = join(FOLDER_PATH, '..', 'bin', 'start_worker -name test_worker')
        stop_worker = join(FOLDER_PATH, '..', 'bin', 'stop_worker')
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        callback_server = join(FOLDER_PATH, "callback_server.py")
        try:
            call("twistd -y %s" % callback_server, shell=True)
            call("%s start" % cloudooomanager_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            call("%s" % worker, shell=True)
            sleep(15)
            unittest.main()
        finally:
            sleep(1)
            call("kill -9 `cat twistd.pid`", shell=True)
            call("%s stop" % cloudooomanager_ctl, shell=True)
            call("%s test_worker " % stop_worker, shell=True)
            call("%s test" % del_user, shell=True)

