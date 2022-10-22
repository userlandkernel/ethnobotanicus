#https://discord.com/api/oauth2/authorize?client_id=1032752693564944474&permissions=1634235578432&scope=bot
import os
import sys
import logging
import urllib.request
import requests
import json
from bs4 import BeautifulSoup as BSoup
import bot

# TEST
if __name__ == "__main__":
	log = logging.getLogger("PlantID")
	log.setLevel(logging.INFO)
	bot.run_discord_bot()