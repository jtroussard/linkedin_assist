#!/usr/bin/python3

"""Helper functions for linkedin assist terminal program."""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import yaml, requests, json, sys, random
import datetime as dt
import english as en

def import_configurations(cl_args):
	"""
	Summary: Opens and load configuration file. Configuration file/location is passed to program
	when exec in terminal. Missing, invalid, unsuccessful open processes lead to program exit.
	Configuration file scntains API links, keyword terms, etc. Any data deemed 	variable or might
	change in the future due to versioning from LI API.

	:cl_args: Command line arguments passed from main program.
	:return: yaml file of configuration options and data.
	note:: argument should be unix style file path
	"""
	if len(cl_args) < 2:
		print("Configuration file not specified. Exiting program.")
		return None
	else:
		config = None
		try:
			from yaml import Cloader as Loader, CDumper as Dumper
		except ImportError:
			from yaml import Loader, Dumper
	try:
		config_file = str(cl_args[1])
		with open(config_file, 'r') as ymlfile:
			config = yaml.load(ymlfile, Loader=Loader)
	except:
		print("Error:{}".format(sys.exc_info()))
		raise
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
	"""Determines if GUIDS have been recorded before and whether they are still active.
	Separates each, (keep/remove) into two lists returned as a dictionary.

	:param current: List of guids from current run (active openings)
	:param saved_file-name: file name of saved_guids. Saved GUIDS represent past GUIDS which were known
	to be active since the last run of this program.
	:returns: dict of guids to keep and remove. {'keep':keep,'remove':remove}
	"""	
	keep = []
	remove = []
	curr_guids = []
	sg_list = []

	for d in current:
		curr_guids.append(d['guid'])
	try:
		with open(saved_file_name, 'r') as saved_guids:
			# Loop through old GUIDS, if they exist in the current list they are still active.
			# otherwise add them to the remove list.
			for og in saved_guids:
				sg_list.append(og.strip()) # used to update saved_guids list
				if og in curr_guids:
					keep.append(og)
				else:
					remove.append(og)
			for cg in curr_guids:
				if cg not in keep:
					keep.append(cg)
	except IOError:
		print("File not found or path is incorrect:{}\n{}".format(saved_file_name, sys.exc_info()))
		raise
	try:
		with open(saved_file_name, 'a') as saved_guids:
			for guid in keep:
				if guid not in sg_list:
					saved_guids.write("{}\n".format(guid))
	except IOError:
		print("File not found or path is incorrect:{}\n{}".format(saved_file_name, sys.exc_info()))
		raise
	return {'keep':keep,'remove':remove}

def make_suggestions(keepers, data, inp, limits):
	"""Using limits defined but the argument, 'limits', determines of any pre-existing GUID meets the
	conditions to be reposted. All new posts are automatically suggested."

	:param keepers: List of guids to consider.
	:param data: ??? forgot if I even use this.
	:param inp: File name string for the records JSON data.
	:param limits: Configuration data containing values to set the thresholds for reposting. At this time
	total posts and date since last post are allowed.
	:returns: list of valid GUIDS.
	"""
	sugs = []
	lim_age = dt.timedelta(days=limits['post_age'])
	today = dt.datetime.today()
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
						if ( diff < lim_age) or (rec['counter'] > limits['post_count']):
							# print("{} broke config limits. Not suggesting.".format(rec['guid']))
							pass
						else:
							sugs.append(guid)
						guid_used = True
						break
				if not guid_used:
					sugs.append(guid)
	except IOError:
		print("File not found or path is incorrect:{}\n{}".format(inp))
		raise
	return sugs

def get_user_feedback(options):
	reply = {}
	u_inp = input("\nWould you like to post these jobs?\nY - Yes\nN - No\n> ")
	if u_inp.lower() in options:
		reply['control'] = False
	else:
		reply['value'] = True
	reply['value'] = u_inp
	return reply

def update_records(file, records, job, date):
	ele_found = False
	for element in records:
		if element['guid'] == job['guid']:
			element['counter'] += 1
			element['last_post'] = str(date)[:10]
			ele_found = True
			file.seek(0)
			json.dump(records, file, indent=2)
			file.truncate()
	if not ele_found:
		records.append({
			"guid": job['guid'],
			"last_post": str(date)[:10],
			"counter": 1})
		file.seek(0)
		json.dump(records, file, indent=2)
		file.truncate()
	return True

def search(guid, alist):
	for g in alist:
		if g['guid'] == guid:
			return g

def create_message(job, message_bank):
	m_pattern = random.choice(message_bank)
	m_title = job['title']

	if m_pattern.startswith('$'):
		m_pattern = m_pattern[1:]
		m_title = en.pluralize(m_title)

	msg = m_pattern.format(title=m_title, city=job['city'])
	return msg

def add_hashtags(message, hashtags):
	pattern = ".\n.\n.\n.\n.\n.\n.\n.\n.\n"
	message = "{}{}".format(message, pattern)
	for tag in hashtags:
		message = "{}#{} ".format(message, tag)
	return message

def apply_config_selections(config, list_of_jobs):
	final_list = {'posts': []}
	n = config['SELECTION_OPTION']
	if len(list_of_jobs) > n:
		n = len(list_of_jobs)
	for i in range(n):
		job = random.choice(list_of_jobs)
		final_list['posts'].append("{:<32}: {:>32}".format(job['title'], job['guid']))
	return final_list


