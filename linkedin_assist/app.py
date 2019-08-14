#!/usr/bin/python3

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import sys, requests, yaml, json
import pprint

from dnt import vault
from classes.LinkedinAssist import LinkedinAssist

import datetime as dt

today = dt.datetime.today()

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
		sugs = []
		lim_age = dt.timedelta(days=config['LIMITS']['post_age'])
		try:
			with open(inp, 'r') as r:
				records = json.load(r)
				for guid in keepers:
					guid_used = False
					for rec in records:
						if guid == rec['guid']:
							datetime_object = dt.datetime.strptime(rec['last_post'], '%Y-%m-%d')
							diff = today-datetime_object
							# print("today {} ---- datetime_object {}    diff {}".format(today, datetime_object, diff.days))
							if ( diff < lim_age) or (rec['counter'] > config['LIMITS']['post_count']):
								print("{} broke config limits. Not suggesting.")
							else:
								sugs.append(guid)
							guid_used = True
							break
					if not guid_used:
						sugs.append(guid)
		except:
			print("error:{}".format(sys.exc_info()))
			raise
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

	# Interface with user.
	if len(suggestions) == 0:
		print("Nothing to post for now. Check back again soon. Bye!")
		sys.exit()
	else:
		print("\nThese are the available jobs:\n")
		for job in it_jobs:
			if job['guid'] in suggestions:
				print("{}\n{}\n\n".format(job['title'], job['location']))

	# Get feedback from user.
	u_inp = None
	input_loop = True
	options = ['y', 'n', 'yes', 'no']
	while input_loop == True:
		u_inp = input("\nWould you like to post these jobs?\nY - Yes\nN - No\n> ")
		if u_inp.lower() in options:
			input_loop = False

	# Read user feedback and exec as required.
	if u_inp.lower() == 'y':
		linkedin_assist_obj = LinkedinAssist(config)
		if linkedin_assist_obj.make_connection():
			user_url = config['URLS']['li_api_get_user_profile']
			urn = linkedin_assist_obj.get_urn(user_url)
		else:
			sys.exit("Connection to Linkedin API could NOT be made. Exiting program.")
		try:
			with open(config['FILES']['records'], "r+") as f:
				data = json.load(f)
				for job in it_jobs:
					if job['guid'] in suggestions:
						post = linkedin_assist_obj.form_post(job, urn)
						if linkedin_assist_obj.make_posts(post):
							print("Posting successful for . . . . . {}".format(job['title']))
							ele_found = False
							for element in data:
								if element['guid'] == job['guid']:
									element['counter'] += 1
									element['last_post'] = str(today)[:10]
									ele_found = True
									f.seek(0)
									json.dump(data, f, indent=2)
									f.truncate()
							if not ele_found:
								data.append({
									"guid": job['guid'],
									"last_post": str(today)[:10],
									"counter": 1})
								f.seek(0)
								json.dump(data, f, indent=2)
								f.truncate()
						else:
							print("Something went wrong with  . . . {}".format(job['title']))
		except:
			print("Error:{}".format(sys.exc_info()))
	else:
		print("No shares made to LinkedIn. Shutting program down. Thank you.")
	#clean_up()

if __name__ == '__main__':
	try:
		main_func()
	except:
		print("MAIN failure:\n{}".format(sys.exc_info()))
		raise