#!/usr/bin/python3

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import sys, requests, selector, json
import helpers as hs
import datetime as dt

from classes.LinkedinAssist import LinkedinAssist
from config import messages

today = dt.datetime.today()

def main_func():

	# Get configurations and load into local variable.
	config = hs.import_configurations(sys.argv)
	if not config:
		sys.exit()

	# Unpack the configuration variables
	RUN_MODE            = config['RUN_MODE']
	RUN_TYPE            = config['RUN_TYPE']
	TARGET_URL          = config['URLS']['target_url']
	KEYWORDS            = config['KEYWORDS']['job_title']
	HASHTAGS            = config['KEYWORDS']['hashtags']
	FN_SAVED_GUIDS      = config['FILES']['saved_guids']
	FN_RECORDS          = config['FILES']['records']
	LIMITS              = config['LIMITS']
	API_URL_GET_USER    = config['URLS']['li_api_get_user_profile']

	tkn = None

	# Fetch JSON format job posting data. Store current data to guid file.
	data = hs.get_job_data(TARGET_URL)

	# Filter out non-IT jobs.
	it_jobs = hs.filter_data(data, KEYWORDS)

	# Create KEEP and REMOVE list.
	keep_remove = hs.compare_and_keep(it_jobs, FN_SAVED_GUIDS)
	keepers = keep_remove['keep']

	# Create a list of GUIDS from which the user can choose from.
	suggestions = hs.make_suggestions(keepers, it_jobs, FN_RECORDS, LIMITS)

	# Interface with user.
	if len(suggestions) == 0:
		print("Nothing to post for now. Check back again soon. Exiting program.")
		sys.exit()
	else:
		job_list_json = []
		for job in it_jobs:
				if job['guid'] in suggestions:
					job_list_json.append(job)
		if RUN_MODE == 'MANUAL':
			user_selections = selector.present_menu(job_list_json)
		else:
			user_selections = hs.apply_config_selections(config, job_list_json)

	if user_selections:
		linkedin_assist_obj = LinkedinAssist(config) # <-- Basically a modified OAuth2 Request Object

		# Check for existing token
		try:
			token_file = open('./data/token')
			tkn = json.load(token_file)
		except IOError:
			tkn = None
		# Make connection either with token or manual user authentication.
		if not tkn:
			print("\n============================================================\nOAuth2 token not found. User will have to authenticate.\n============================================================\n\n             Please follow the prompts.\n")
			token = linkedin_assist_obj.get_access().token
			if token:
				try: # Save the auth token for future logins
					with open('./data/token', 'w') as token_save:
						token_save.seek(0)
						json.dump(token, token_save, indent=2)
						token_save.truncate()
				except IOError:
					print("File not found or path is incorrect:{}\n{}".format(saved_file_name, sys.exc_info()))
					raise
		else:
			print("\n============================================================\nOAuth2 token present, will attempt to use token.\n============================================================\n\n")
			linkedin_assist_obj.get_access(tkn)
		# Exit program if connection unsuccessful, otherwise configure target resource link
		if not linkedin_assist_obj.authorized:
			sys.exit("Authentication to Linkedin API could NOT be made. Exiting program.")
		else:
			urn = linkedin_assist_obj.get_urn(API_URL_GET_USER)

		try: # POST request to LinkedIn & updating records
			with open(FN_RECORDS, "r+") as r:
				records = json.load(r)
				for selection in user_selections['posts']:
#					print('\n\n')
					job = hs.search(selection.split(':')[1].strip(), job_list_json)
					msg = hs.create_message(job, messages.MESSAGES)
					msg = hs.add_hashtags(msg, HASHTAGS)
					post = linkedin_assist_obj.form_post(job, urn, msg)
					if linkedin_assist_obj.make_posts(post):
						if ("DEVELOPMENT" or "TEST") in RUN_TYPE:
							print('DEMO print:')
						else:
							print('POSTED text:')
							hs.update_records(r, records, job, today)
						print(msg)
						print("\nSuccess! [{}]\n\n".format(job['title']))
					else:
						print("\nFailed :( [{}]\n\n".format(job['title']))
		except IOError:
			print("Error!!:{}".format(sys.exc_info()))
			raise
	else:
		print("No shares made to LinkedIn. Exiting Program.")
	#clean_up() <-- Maybe create a clean up step in the future.

if __name__ == '__main__':
	try:
		main_func()
	except SystemExit:
		pass
	except:
		print("Error:{}".format(sys.exc_info()))
		raise