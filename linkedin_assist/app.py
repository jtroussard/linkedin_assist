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

	def get_job_data(target_url):
		"""This function will get the initial job opportunity data. The url is determined by the
		configuration file. The get request should return a list of or singular JSON/Python 
		dictionary(ies).

		:param target_url: The url to send 'request towards. Should return list of or singular 
		JSON/dict object.
		:type target_url: str.
		:returns: list of dict objects. -- All types of jobs.
		"""
		r = requests.get(target_url)
		decoded = r.json()
		if type(decoded) != list:
			return decoded_as_list.append(decoded)
		return decoded


	def filter_data(data, keywords):
		"""This function will filter out any jobs which title do not have a matching word 
		in the keywords bank. This bank of words is determined by the configuration file.

		:param data: Input containing job opportunties.
		:type data: list.
		:param keywords: Words to match against. These should be words found in IT job titles.
		:type keywords: list
		:returns: list of dict objects -- IT job data.
		"""		
		it_jobs = []
		for element in data:
			title_words = element['title'].split()
			for word in title_words:
				if word.lower() in keywords:
					it_jobs.append(element)
					break
		return(it_jobs)

	def compare_and_keep(current, saved_file_name):
		keep = []
		remove = []
		curr_guids = []
		for d in current:
			curr_guids.append(d['guid'])

		try:
			with open(saved_file_name, 'r') as saved_guids:
				for og in saved_guids:
					if og in curr_guids:
						keep.append(og)
					else:
						remove.append(og)
				for cg in curr_guids:
					if cg not in keep:
						keep.append(cg)
		except:
			print("Error:{}".format(sys.exc_info()))
			raise
		return {'keep':keep,'remove':remove}

	def load_records(records_filename):
		records_list = []
		try:
			with open(records_filename, 'r') as inp:
				for line in inp:
					records_list.append(line)
		except:
			print("Error:{}".format(sys.exc_info()))
		return records_list

	def compare_job_data(current, previous_file):
		"""This function will compare the job inputs from the last run to the current run.
		This allows the program to determine if there are any new posts. Then this function
		will also rebuilb the 'previous' file in preparation for the next run.

		:param current: Data from current run.
		:type current: list. -- of dict objects.
		:param previous_file: Path to previous file.
		:type current: str.
		:returns: dict object containing the new and old guids.
		"""
		new_file_name = previous_file
		try:
			# Load the old records into the buffer list for writing to new file.
			new_file_contents = []
			old_guids = []
			with open(previous_file, 'r') as encoded_inp:
				inp = json.load(encoded_inp)
				for entry in inp:
					new_file_contents.append(entry)
					old_guids.append(entry['guid'])

			# Create and compare two sets. One of previous runs guids and todays.
			# The difference should represent the newest guids.
			previous_guids = []
			current_guids = []
			with open(previous_file, 'r') as encoded_inp:
				inp = json.load(encoded_inp)
				for entry in inp:
					previous_guids.append(entry['guid'])
				for entry in current:
					current_guids.append(entry['guid'])
			diff_guids = set(previous_guids) - set(current_guids) 
			print(diff_guids)

			# Compare the difference GUIDS against the current list of dicts. Matches
			# are old/present dicts, non matches are new. New dicts will get written 
			# to the new 'previous' file.
			new_guids = []
			for element in current:
				if element['guid'] not in diff_guids:
					new_file_contents.append(element)
					new_guids.append(element['guid'])

			# Write to new file.
			with open(new_file_name, 'wt', encoding='utf-8') as new:
				new.seek(0)
				json.dump(new_file_contents, new, ensure_ascii=False, indent=4)
			return {'new':new_guids,'old':old_guids}
		except:
			print("{}\n\n".format(sys.exc_info()))
			raise

	def make_suggestions(keepers, data, inp, config):
		import datetime as dt
		today = dt.datetime.today()
		sugs = []

		try:
			with open(inp, 'r') as records:
				for guid in keepers:
					for r in records:
						rec = json.loads(r)
						if guid == rec['guid']:
							datetime_object = dt.datetime.strptime(rec['date_new'], '%Y-%m-%d')
							lim_age = dt.timedelta(days=config['LIMITS']['post_age'])
							if (today - datetime_object < lim_age) or (sline[2] < config['LIMITS']['post_count']):
								sugs.append(guid)
		except:
			print("error:{}".format(sys.exc_info()))
			raise
		sys.exit()
		return sugs

	#START#

	# Get configurations and load into local variable.
	config = import_configurations()

	# Fetch JSON format job posting data. Store current data to guid file.
	data = get_job_data(config['URLS']['target_url'])

	# Filter out non-IT jobs.
	it_jobs = filter_data(data, config['KEYWORDS']['job_title'])

	# Create KEEP and REMOVE list.
	keep_remove = compare_and_keep(it_jobs, config['FILES']['saved_guids'])

	# Create a list of GUIDS from which the user can choose from.
	suggestions = make_suggestions(keep_remove['keep'], it_jobs, config['FILES']['records'], config)
	

	#leaving off here we have a list of GUIDS to suggest in SUGS 

	# 1. interact with user
	#        show list of titles, their last post date and total count
	#        print all for this version... will allow choice when upgraded to npyscreen
	#        for loop through it_jobs and push data to LINKEDIN object and alter LINKEDIN
	#        post method to process one job at a time....
	#        and return a code, if a posting failure occurs, record in a fast and dirty log
	#        and try to continue... another upgrade will be a real log library.







	# this looks to be working ok, create a sep func and move after IT filter 
	try:
		with open(config['FILES']['data'],'r') as inp, open(config['FILES']['data'],'a') as new:
			past_guids_data = inp.readlines()
			past_guids_data.pop(0) #remove header
			temp_list = []
			for x in past_guids_data:
				temp_list.append(x.split(','))

			found = False
			for i in data:
				for j in temp_list:
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
	guids = compare_job_data(data, config['FILES']['data'])
	it_jobs = filter_data(guids, data, config)

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