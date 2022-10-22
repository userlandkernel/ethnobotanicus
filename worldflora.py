import sys
import os
import logging
import requests

class WorldFloraDB(dict):

	def __init__(self):
		self._dict = {}
		self.api = "http://www.worldfloraonline.org/"
		self.sess = requests.Session()
		self.routes = {
			"taxon": "taxon/"
			"image": "image/"
			"reference": "reference/"
			"resource": "resource/"
		}

	def GetTaxon(self, wfoId=None):
		headers = {
			"Accept": "*/*",
			"Content-Type": "application/json"
		}
		rsp = self.sess.get(self.routes['taxon']+wfoId)
		return rsp.json()