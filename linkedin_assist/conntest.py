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

	def post_job_share():
		return "post_job_share"

	def clean_up():
		#close config
		return "clean_up"

	# START MAIN FUNCTION HERE #

	# GET JOB DATA & DETERMINE IF THERE IS ANYTHING TO POST #
	cfg = import_configurations()

	url = 'https://api.linkedin.com/v2/shares'
	payload = {}
	
	headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
	params = {'oauth2_access_token': 'YgR1ReQvjLZ6nEIW'}
	response = requests.post(url,data=payload,params=params)
	print(response.text)




	u_inp = 'y'
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

