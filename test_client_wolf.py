#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import json
# import pytest
import urllib2
import urllib
import httplib
from xml.etree import ElementTree as etree
import wolframalpha
import sys
app_id = '7QHVE4-JKHK7KQEQ8'
"App ID for testing this project. Please don't use for other apps."

def test_basic():
	client = wolframalpha.Client(app_id)
	res = client.query('p/e msft')
	# assert len(res.pods) > 0
	print len(list(res))
	print list(res)
	# results = list(res.results)
	# print results
	# assert results[0].text == '86 °F  (degrees Fahrenheit)'

def test_invalid_app_id():
	client = wolframalpha.Client('abcdefg')
	with pytest.raises(Exception):
		client.query('30 deg C in deg F')
 
class wolfram(object):
    def __init__(self, appid):
        self.appid = appid
        self.base_url = 'http://api.wolframalpha.com/v2/query?'
        self.headers = {'User-Agent':None}
 
    def _get_xml(self, ip):
        url_params = {'input':ip, 'appid':self.appid}
        data = urllib.urlencode(url_params)
        req = urllib2.Request(self.base_url, data, self.headers)
        xml = urllib2.urlopen(req).read()
        return xml
 
    def _xmlparser(self, xml):
        data_dics = {}
        tree = etree.fromstring(xml)
        #retrieving every tag with label 'plaintext'
        for e in tree.findall('pod'):
            for item in [ef for ef in list(e) if ef.tag=='subpod']:
                for it in [i for i in list(item) if i.tag=='plaintext']:
                    if it.tag=='plaintext':
                        data_dics[e.get('title')] = it.text
        return data_dics
 
    def search(self, ip):
    	print ip
        xml = self._get_xml(ip)
        result_dics = self._xmlparser(xml)
        #return result_dics 
        #print result_dics
        print result_dics
 
if __name__ == "__main__":
    appid = '7QHVE4-JKHK7KQEQ8'
    query = sys.argv[0]
    w = wolfram(appid)
    w.search(query)