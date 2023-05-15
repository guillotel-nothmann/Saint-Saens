import time
import sys, os
import argparse
from pathlib import Path
import json 
import codecs

from xml.dom import minidom

sys.path.append("..")
from lib.music.opusmeta import OpusMeta

utfx = "utf-16"

def main(argv=None):
	"""Utilitaire d'extraction de données MEI"""

	current_path = os.path.dirname(os.path.abspath(__file__))
	out_dir = os.path.join(current_path, 'json')

	# On accepte des arguments
	parser = argparse.ArgumentParser(description='Utilitaire corpus')
	parser.add_argument('-f', '--file', dest='fname', required=True,
                   help='Nom du fichier MEI à analyser')
	parser.add_argument('-a', '--action', dest='action', required=True,
                   help="Action: 'extract', ou 'analyze'")
	args = parser.parse_args()
	
	input_file = os.path.join("mei", args.fname)
	if not os.path.exists(input_file):
		sys.exit (input_file + "  does not exist. Please check.")
	if not os.path.isfile(input_file):
		sys.exit (input_file + "  is not a file. Please check.")
		
	# Get the file name without extension
	input_file_root = os.path.splitext(os.path.basename(input_file))[0]

	if args.action == "extract":
		print (f"Extracting data from {input_file}")
		with codecs.open(input_file, 'r', encoding=utfx) as f:
			mei = f.read()

		doc = minidom.parseString(mei)
		
		# Example: extracting a title
		opus_title = ""
		titles = doc.getElementsByTagName("title")
		for title in titles:
			for txtnode in title.childNodes:
				opus_title += txtnode.data + " "
			break

		# extracting a composer
		opus_composer = ""
		composers = doc.getElementsByTagName("composer")
		for composer in composers:
			for txtnode in composer.childNodes:
				opus_composer += txtnode.data + " "
			break

		#exctracting a lyricist
		opus_lyricist =""
		if doc.getElementsByTagName("lyricist"):
			lyricists = doc.getElementsByTagName("lyricist")
			for lyricist in lyricists:
				for txtnode in lyricist.childNodes:
					opus_lyricist += txtnode.data + " "
				break

		# extracting date
		creation_tag = doc.getElementsByTagName("creation")
		for element in creation_tag:
			opus_date_after = None
			opus_date_before = None
			date_tag = element.getElementsByTagName("date")
			for date in date_tag:
				if date.hasAttribute("notbefore"):
					opus_date_before=date.getAttribute("notbefore")
				if date.hasAttribute("notafter"):
					opus_date_after=date.getAttribute("notafter")
				if opus_date_before and opus_date_after:
					opus_date = "[" + opus_date_after + " - " + opus_date_before + "]"
				elif opus_date_before:
					opus_date = "[avant " + opus_date_before + "]"
				elif opus_date_after:
					opus_date = "[après " + opus_date_after + "]"
				else :
					opus_date = date.firstChild.nodeValue

		#extracting ark
		ark_tag=""
		sources = doc.getElementsByTagName("source")
		for source in sources:
			if source.hasAttribute("auth.uri"):
				ark_tag = source.getAttribute("auth.uri")
			break

		#extracting cote
		opus_cote=""
		cotes = doc.getElementsByTagName("bibl")
		for cote in cotes:
			for txtnode in cote.childNodes:
				opus_cote += txtnode.data + " "
			
		# To be continued...
		opusmeta = OpusMeta(ref=input_file_root, title=opus_title, composer=opus_composer, lyricist=opus_lyricist, date = opus_date, sources = ark_tag, cote = opus_cote)
		json_name = os.path.join(out_dir, input_file_root + '.json')
		json_object = json.dumps(opusmeta.to_json(), indent=4, ensure_ascii=False).encode(utfx)
		with open(json_name, "w") as outfile:
			json_str = json_object.decode(utfx)
			outfile.write(json_str)
		print (f"Extraction written to {json_name}")
		
	elif args.action == "analyze":
		print ("Analyze")
	else:
		print ("Unknown action : " + args.action)

if __name__ == "__main__":
	main()