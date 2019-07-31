#!/usr/bin/python3

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import sys, requests, yaml, json
import pprint
# import npyscreen

# class LinkedinAssistApp(npyscreen.NPSApp):
# 	def create(self):
# 		F = npyscreen.Form(name = "Linkedin Assist App")
# 		ms = F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", values = ["Option1","Option2","Option3"], scroll_exit=True)
# 		ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], name="Pick Several", values = ["Option1","Option2","Option3"], scroll_exit=True)
# 		F.edit()



def main_func():

	cfg = None

	def get_login_creds():
		
		return "get_login_creds"

	def get_linkedin_token(credentials):
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
		return(it_jobs)

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
	it_jobs = filter_compares(guids, data, cfg)

	# DISPLAY RESULTS #
	print("\nThese are the available jobs:\n")
	for job in it_jobs:
		print("{}\n{}\n\n".format(job['title'], job['location']))

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
		creds = get_login_creds()
		token = get_linkedin_token(creds)
		if post_job_share():
			print("Posting successful")
		else:
			print("Something went wrong.")
	else:
		print("No shares made to LinkedIn. Shutting program down. Thank you.")
	clean_up()



# next version convert to npyscreen terminal app
if __name__ == '__main__':
	# App = TestApp()
	# App.run()
	try:
		main_func()
	except:
		print("MAIN failure:\n{}".format(sys.exc_info()))
		raise

