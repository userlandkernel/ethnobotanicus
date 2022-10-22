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

import plantid
import kewdb

class EthnoBotanicus(object):

	"""docstring for EthnoBotanicus"""
	def __init__(self):
		super(EthnoBotanicus, self).__init__()
		self.registry = {}
		self.KewDB = kewdb.KewPlantDB()
		self.Identifier = plantid.PlantIdentifier()
