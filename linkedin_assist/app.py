#!/usr/bin/python3

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import sys, requests, yaml, json

def main_func():

	cfg = None

	def get_login_creds():
		return "get_login_creds"

	def get_linkedin_token():
		return "get_linkedin_token"

	def import_configurations():
		if len(sys.argv) < 2:
			sys.exit("Configuration file not specified. Exiting program.")
		else:
			try:
				from yaml import Cloader as Loader, CDumper as Dumper
			except ImportError:
				from yaml import Loader, Dumper
		try:
			config_file = str(sys.argv[1])
			with open(config_file, 'r') as ymlfile:
				cfg = yaml.load(ymlfile, Loader=Loader)
		except:
			print("---import_configurations failure:\n{}".format(sys.exc_info()))
		return cfg

	def get_job_data():
		target_url = cfg['URLS']['input_jobs']
		print(target_url)
		r = requests.get(target_url)
		#print(r.text)
		decoded = r.json()		
		print(json.dumps(decoded[0], indent=4))

		return "get_job_data"

	def post_job_share():
		return "post_job_share"

	def clean_up():
		#close config
		return "clean_up"

	# START MAIN FUNCTION HERE #
	cfg = import_configurations()
	get_job_data()



if __name__ == '__main__':
	try:
		main_func()
	except:
		print("MAIN failure:\n{}".format(sys.exc_info()))
		raise

