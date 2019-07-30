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
		#print(json.dumps(decoded[0], indent=4))
		return decoded

	def compare_job_data(current, previous):
		try:
			with open(previous) as previous_guids:
				prev_guid = []
				for element in previous_guids:
					prev_guid.append(element)
				curr_guid = []
				for element in current:
					curr_guid.append(element['guid'])
					# print(element['title'])
				return set(curr_guid) - set(prev_guid)
		except:
			print("---compare_job_data failure:\n{}".format(sys.exc_info()))
			raise

	def filter_compares(guids, data, cfg):
		title_key_words = cfg['KEYWORDS']['job_title']
		it_jobs = []
		for idnum in guids:
			for dictionary in data:
				if dictionary['guid'] == idnum:
					job_title_words = dictionary['title'].split()
					for word in job_title_words:
						if word.lower() in title_key_words:
							it_jobs.append(dictionary)

	def post_job_share():
		return "post_job_share"

	def clean_up():
		#close config
		return "clean_up"

	# START MAIN FUNCTION HERE #

	# GET JOB DATA & DETERMINE IF THERE IS ANYTHING TO POST #
	cfg = import_configurations()
	data = get_job_data()
	guids = compare_job_data(data, cfg['FILES']['guids'])
	filter_compares(guids, data, cfg)



if __name__ == '__main__':
	try:
		main_func()
	except:
		print("MAIN failure:\n{}".format(sys.exc_info()))
		raise

