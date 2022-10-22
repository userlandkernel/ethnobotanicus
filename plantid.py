"""
	Program: Ethnobotanicus
	File: Ethnobotanicus
	Author: Sem Voigtlander (info@kernelprogrammer.com)
	Purpose: Main interface bridging the components of the Ethnobotanicus together
"""
import os
import sys
import logging
import urllib.request
import requests
import json
from bs4 import BeautifulSoup as BSoup

class PlantIdentifier(dict):

	def __init__(self, logger=logging.getLogger('EthnoBotanicus')):
		self.logger = logger
		self._dict = {}
		self.sess = requests.Session()
		self.api = "https://api.plantnet.org/v1"
		self.route = {
			'images': self.api+'/images', 
			'identify': self.api+'/projects/the-plant-list/queries/identify?illustratedOnly=true&clientType=web&clientVersion=3.0.0&lang=en&mediaSource=file'
		}
		self.imageIds = [] # List containing the ids of the uploaded plant images
		self.registry = [] # Registry containing identified plants and retrieved information

	def upload(self, image=None):

		# Validate path
		path = os.path.normpath(image)		
		if not os.path.exists(path):
			raise FileNotFoundError
		if not os.path.isfile(path):
			raise FileNotFoundError
		self.path = path

		# Prepare upload data
		imageBytes = open(path, 'rb').read()
		uploadData = {'file': imageBytes}

		# Upload the image file
		rsp = self.sess.post(self.route['images'], files=uploadData)
		
		# Validate response
		if rsp.status_code != 200:
			raise ValueError("API returned with error: "+rsp.text)
		apiRsp = rsp.json()
		if not 'id' in apiRsp:
			print("[!] Failed uploading.")
			return
		self.imageIds.append(apiRsp['id'])
		self.logger.info("[*] Successfully uploaded file!")

	def uploadFolder(self, path=None):

		""" Iterate over folder and upload images """
		for entry in os.listdir(path):
			ext = os.path.splitext(entry)[1]
			if ext.lower() not in [".jpg", ".gif", ".png", ".tga", ".bmp", ".jpeg"]:
				continue
			self.upload(os.path.join(path, entry))

	def identifyWeb(self, url=None):

		if url == None:
			raise ValueError("Needs a valid URL to work!")

		postData = {
			"images": [{"url": str(url)}]
		}

		req = urllib.request.Request(self.route['identify'])
		req.add_header('Content-Type', 'application/json; charset=utf-8')
		jsondata = json.dumps(postData) # Convert post data to JSON type
		jsondataasbytes = jsondata.encode('utf-8') # needs to be bytes

		# Submit data to API
		rsp = urllib.request.urlopen(req, jsondataasbytes).read()
		apiRsp = json.loads(rsp) # Load the response dictionary
	
		# Check error messages
		if 'message' in apiRsp.keys():
			if apiRsp['message'] != None:
				raise ValueError(apiRsp['message'])

		# Validate the plant was identified
		if 'results' not in apiRsp.keys():
			raise ValueError("Unidentified plant")

		# Print the identified plant's most probable info
		mostProbable = apiRsp['results'][0]
		self.logger.info("Identified: "+str(mostProbable['species']['name']), "\nProbability:", mostProbable['score'])

		# Add the plant result to the dictionary
		self.registry.append({
			'id': apiRsp['results'][0]['images'][0]['id'],
			'results': apiRsp['results']
		})

		self._dict[apiRsp['results'][0]['images'][0]['id']] = mostProbable['species']['name']


	def identifyUploaded(self):

		headers = {
			'Content-type': 'application/json', 
			'Accept': 'application/json', 
			'charset':'utf-8', 
			'Accept-Encoding':'gzip, deflate, br',
			"Accept-Language":"en-US,en;q=0.9,nl-NL;q=0.8,nl;q=0.7",
  			"Origin":"https://identify.plantnet.org",
  			"Referer":"https://identify.plantnet.org/",
  			"Sec-Fetch-Dest":"empty",
			"Sec-Fetch-Mode":"cors",
			"Sec-Fetch-Site":"same-site"
		}

		for imgId in self.imageIds:
			
			postData = {
				"images": [{"url": f"https://bs.plantnet.org/v1/image/o/{imgId}"}]
			}

			req = urllib.request.Request(self.route['identify'])
			req.add_header('Content-Type', 'application/json; charset=utf-8')
			jsondata = json.dumps(postData) # Convert post data to JSON type
			jsondataasbytes = jsondata.encode('utf-8') # needs to be bytes

			# Submit data to API
			rsp = urllib.request.urlopen(req, jsondataasbytes).read()
			apiRsp = json.loads(rsp) # Load the response dictionary
		
			# Check error messages
			if 'message' in apiRsp.keys():
				if apiRsp['message'] != None:
					raise ValueError(apiRsp['message'])

			# Validate the plant was identified
			if 'results' not in apiRsp.keys():
				raise ValueError("Unidentified plant")

			# Print the identified plant's most probable info
			mostProbable = apiRsp['results'][0]
			logger.info("Identified: "+str(mostProbable['species']['name']), "\nProbability:", mostProbable['score'])

			# Add the plant result to the dictionary
			self.registry.append({
				'id': imgId,
				'results': apiRsp['results']
			})

	#		self._dict[imgId] = mostProbable['species']['name']