#!/usr/bin/python3

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import sys, requests, yaml, json
import pprint

from dnt import vault
from classes.LinkedinAssist import LinkedinAssist

def main_func():

	config = None

	def import_configurations():
		"""
		Summary: Opens and load configuration file. Configuration file/location is passed to program
		when exec in terminal. Missing, invalid, unsuccessful open processes lead to program exit.
		Configuration file scntains API links, keyword terms, etc. Any data deemed 	variable or might
		change in the future due to versioning from LI API.

		:return: yaml file of configuration options and data.
		note:: argument should be unix style file path
		"""
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
				config = yaml.load(ymlfile, Loader=Loader)
		except:
			print("---import_configurations failure:\n{}".format(sys.exc_info()))
		return config

	def get_job_data():
		target_url = config['URLS']['input_jobs']
		r = requests.get(target_url)
		decoded = r.json()		
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
				return set(curr_guid) - set(prev_guid)
		except:
			print("---compare_job_data failure:\n{}".format(sys.exc_info()))
			raise

	def filter_compares(guids, data, config):
		title_key_words = config['KEYWORDS']['job_title']
		it_jobs = []
		for idnum in guids:
			for dictionary in data:
				if dictionary['guid'] == idnum:
					job_title_words = dictionary['title'].split()
					for word in job_title_words:
						if word.lower() in title_key_words:
							it_jobs.append(dictionary)
		return(it_jobs)

	def clean_up():
		#close config
		return "clean_up"

	

	#START#

	# Get configurations and load into local variable.
	config = import_configurations()

	# Fetch JSON format job posting data. Store current data to guid file.
	data = get_job_data()

	try:
		with open(config['FILES']['guids'],'r') as inp, open(config['FILES']['guids'],'a') as new, open('./testout.txt', 'w') as out:
			past_guids_data = inp.readlines()
			past_guids_data.pop(0) #remove header
			temp_list = []
			for x in past_guids_data:
				temp_list.append(x.split(','))

			found = False
			for i in data:
				for j in temp_list:
					print("{} = {}".format(i['guid'], j[0]))
					if i['guid'] == j[0]:
						found = True
						break
				if not found:
					add_to_history = True
					new.write("{},{},{},{}\n".format(i['guid'],i['date_new'],0,'active'))
				found = False

	except:
		print("FILE error:\n{}".format(sys.exc_info()))
		raise

	# Compare current data with previous pulls.
	guids = compare_job_data(data, config['FILES']['guids'])
	print(guids)
	sys.exit()
	it_jobs = filter_compares(guids, data, config)

	# Interface with user.
	print("\nThese are the available jobs:\n")
	for job in it_jobs:
		print("{}\n{}\n\n".format(job['title'], job['location']))

	# GUID Analysis


	# GET FEEDBACK #
	u_inp = None
	input_loop = True
	options = ['y', 'n', 'Y', 'N']
	while input_loop == True:
		u_inp = input("Would you like to post these jobs? [Y/N] > ")
		if u_inp in options:
			input_loop = False

	# MAKE CONNECTION AND SHARE POSTS #
	if u_inp.lower() == 'y':
		linkedin_assist_obj = LinkedinAssist(config)
		if linkedin_assist_obj.make_connection():
			user_url = config['URLS']['li_api_get_user_profile']
			print(type(user_url))
			urn = linkedin_assist_obj.get_urn(user_url)
		else:
			sys.exit("Connection to Linkedin API could NOT be made. Exiting program.")
		if linkedin_assist_obj.make_posts(linkedin_assist_obj.form_posts(it_jobs, urn)):
			print("Posting successful")
		else:
			print("Something went wrong.")
	else:
		print("No shares made to LinkedIn. Shutting program down. Thank you.")
	clean_up()

if __name__ == '__main__':
	try:
		main_func()
	except:
		print("MAIN failure:\n{}".format(sys.exc_info()))
		raise

