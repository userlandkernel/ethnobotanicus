"""
	Program: Ethnobotanicus
"""
import os
import sys
import logging
import urllib.request
import requests
import json
from bs4 import BeautifulSoup as BSoup

class KewPlantDB(dict):

	def __init__(self):
		self.api = "https://powo.science.kew.org/api/1"
		self._dict = {}
		self.route = {
			'search': self.api+'/search'
		}

	def Search(self, scientificName=None):
		try:
				rsp = requests.get(self.route['search'], params={'q':scientificName})
				if rsp.status_code != 200:
					return {
							'error': rsp.text,
							'status': rsp.status_code 
					}

				# Return plant data
				plantData =  rsp.json()
				if 'results' in plantData:
					if len(plantData['results']) >= 1:
						probable = plantData['results'][0]
						if 'url' in probable.keys():
							# Get taxonomy data
							taxonomyURL = self.api+probable['url']
							rsp = requests.get(taxonomyURL)
							if rsp.status_code != 200:
								print(rsp.text)
								return plantData
							taxonData = rsp.json()
							plantData['results'][0]['taxonomy'] = taxonData # Add toxonomy data to the plant data
				return plantData

		except Exception as exc:
				return {
						'error': exc.message,
						'status': -1
				}