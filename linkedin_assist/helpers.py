#!/usr/bin/python3

"""Helper functions for linkedin assist terminal program."""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import yaml, requests, json, sys
import datetime as dt

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
	keep = []
	remove = []
	curr_guids = []
	sg_list = []

	for d in current:
		curr_guids.append(d['guid'])
	try:
		with open(saved_file_name, 'r') as saved_guids:
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

def make_suggestions(keepers, data, inp, limits):
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