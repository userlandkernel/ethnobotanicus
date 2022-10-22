import json
from ethnobotanicus import EthnoBotanicus
botanicus = EthnoBotanicus()

""" TODO: Rewrite shitty code to be in kewdb """
def GetTaxonomyData(scientificName=""):
	try:
			info = botanicus.KewDB.Search(scientificName=scientificName)
			if 'results' in info.keys():
				taxonData = info['results'][0]
				taxonDataText = (
					f"https:{taxonData['images'][0]['thumbnail']}\n"
					f"Name: {taxonData['name']}\n"
					f"Kingdom: {taxonData['kingdom']}\n"
					f"Family: {taxonData['family']}\n"
				)

				if 'taxonomy' in taxonData.keys():
					natives = [distribution['tdwgCode'] for distribution in taxonData['taxonomy']['distributions'] if distribution['establishment'] == 'Native']
					introduced = [distribution['tdwgCode'] for distribution in taxonData['taxonomy']['distributions'] if distribution['establishment'] == 'Introduced']
					taxonDataText += (
						"Native in:"+' '.join(natives)+"\n"
						"Introduced in:"+' '.join(introduced)+"\n"
					)
				
				return taxonDataText
	except Exception as exc:
		return exc

def handle_response(message, imageURL=None) -> str:
	p_message = message.lower()

	if p_message == '!identify':
		try:
			botanicus.Identifier.identifyWeb(url=imageURL)
			plantData = botanicus.Identifier.registry.pop()['results']
			taxonData = GetTaxonomyData(scientificName=plantData[0]['species']['name'])
			return (
				f"TAXONOMY DATA:\n{taxonData}\n\n"
				f"Identified as:\n{plantData[0]['species']['name']}\n"
				f"Common Names: {' '.join(plantData[0]['species']['commonNames'])}\n"
				f"Probability: {str(plantData[0]['score'])}\n"
			)

		except ValueError as err:
			return err

	if p_message.startswith("!taxonomy "):
		try:
			name = p_message[10:]
			return GetTaxonomyData(name)

		except ValueError as err:
			return err

	if p_message == '!help':
		return "A bot that helps you identify plants"
