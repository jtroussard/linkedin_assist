#!/usr/bin/python3

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import sys, requests
import pprint

from classes.LinkedinAssist import LinkedinAssist
from dnt import vault

import helpers as hs
import datetime as dt

today = dt.datetime.today()

def main_func():

	# Get configurations and load into local variable.
	config = hs.import_configurations(sys.argv)
	if not config:
		sys.exit()

	# Unpack the configuration variables
	TARGET_URL          = config['URLS']['target_url']
	KEYWORDS            = config['KEYWORDS']['job_title']
	FN_SAVED_GUIDS      = config['FILES']['saved_guids']
	FN_RECORDS          = config['FILES']['records']
	LIMITS              = config['LIMITS']
	UI_FO_GLOBAL_ACCEPT = config['UI']['feedback_options']['global_accept']
	API_URL_GET_USER    = config['URLS']['li_api_get_user_profile']


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
		print("Nothing to post for now. Check back again soon. Bye!")
		sys.exit()
	else:
		print("\nThese are the available jobs:\n")
		for job in it_jobs:
			if job['guid'] in suggestions:
				print("{}\n{}\n\n".format(job['title'], job['location']))

	# Get feedback from user.
	input_loop = True
	reply = {}
	while input_loop == True:
		reply = hs.get_user_feedback(UI_FO_GLOBAL_ACCEPT)
		input_loop = reply['control']

	# Read user feedback and perform necessary action.
	if reply['value'].lower() == 'y':
		linkedin_assist_obj = LinkedinAssist(config) # <-- Basically a modified OAuth2 Request Object
		
		try: # Get Authenticated
			if linkedin_assist_obj.make_connection():
				urn = linkedin_assist_obj.get_urn(API_URL_GET_USER)
			else:
				sys.exit("Connection to Linkedin API could NOT be made. Exiting program.")
		except SystemExit:
			pass
		
		try: # POST request to LinkedIn & updating records
			with open(FN_RECORDS, "r+") as f:
				data = json.load(f)
				for job in it_jobs:
					if job['guid'] in suggestions:
						post = linkedin_assist_obj.form_post(job, urn)
						if linkedin_assist_obj.make_posts(post):
							print("Posting successful for . . . . . {}".format(job['title']))
							hs.update_records(data)
						else:
							print("Something went wrong with  . . . {}".format(job['title']))
		except:
			print("Error:{}".format(sys.exc_info()))
			raise
	else:
		print("No shares made to LinkedIn. Shutting program down. Thank you.")
	#clean_up() <-- Maybe create a clean up step in the future.

if __name__ == '__main__':
	try:
		main_func()
	except SystemExit:
		pass
	except:
		print("Error:{}".format(sys.exc_info()))
		raise