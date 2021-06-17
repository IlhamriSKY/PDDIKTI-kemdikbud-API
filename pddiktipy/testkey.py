# -*- coding: utf-8 -*-
import requests
import base64
import json
import time
import sys
import os
from helper import helper as H

class key(object):
    def __init__(self):
        self.api_link = base64.b64decode('YUhSMGNITTZMeTloY0drdFpuSnZiblJsYm1RdWEyVnRaR2xyWW5Wa0xtZHZMbWxrTDJsdWFXdGxlVzU1WVE9PQ==').decode()
        self.api_version = 'v2'
        self.key = "f0bc412bea18f490ad36b4748a53b11a"
        self.id = "aW5pa2V5"
        
        if len(self.key)!=32:
            print ('Key Invalid')
            exit(1)

    def generatekey(self):
        if sys.version_info >= (3, 0):
            return os.urandom(16).hex()
        return os.urandom(16).encode('hex')

    def generateurl(self):
        return self.generatekey()+self.key+base64.b64decode(self.id).decode()+self.api_link

    def bukan(self):
        punya = "DA08C192-D22E-4D48-86D7-D3F413C3CF06"
        saya = "/detail_mhs/"+base64.b64encode(punya.encode()).decode()
        return saya
        
    def ini(self):
        hanya = self.generateurl()
        mencoba = base64.b64decode(self.id).decode()
        endpoint = hanya.split(mencoba)
        untuk = base64.b64decode(endpoint[1]).decode()
        validasi = untuk.replace(mencoba,'').replace('/nya','')
        return validasi

    def post(self, endpoint, data):
        payloads = "{\"nama\":\""+data+"\",\"nipd\":\"\",\"pt\":\"Universitas Katolik Soegijapranata\",\"prodi\":\"Sistem Informasi\"}"
        return H.post(str(endpoint)+'/'+self.api_version+'/search_mhs', payloads)

    def validate(self):
        r = self.post(self.ini(), 'ilham riski wibowo')
        ids = r['mahasiswa'][0]['id']
        if ids == self.bukan().replace('/detail_mhs/',''):
            return r['mahasiswa'][0]['id']
        else:
            time.sleep(10)
            exit(1)