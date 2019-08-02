#!/usr/bin/python3

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import sys, requests, yaml, json, os
import pprint
# import npyscreen

# class LinkedinAssistApp(npyscreen.NPSApp):
# 	def create(self):
# 		F = npyscreen.Form(name = "Linkedin Assist App")
# 		ms = F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], 
#name="Pick One", values = ["Option1","Option2","Option3"], scroll_exit=True)
# 		ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], 
#name="Pick Several", values = ["Option1","Option2","Option3"], scroll_exit=True)
# 		F.edit()

from dnt import vault



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



	# from http.server import HTTPServer, SimpleHTTPRequestHandler
	# import ssl
	
	# httpd = HTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)
	# httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert.pem', server_side=True)
	# httpd.serve_forever()
	
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

	from requests_oauthlib import OAuth2Session
	from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

	# Credentials you get from registering a new application
	client_id = vault.CLIENT_ID
	client_secret = vault.CLIENT_SECRET
	# Scope is necessary to avoid permission errors
	scope = ['r_liteprofile', 'r_emailaddress', 'w_member_social']
	redirect_url = 'http://127.0.0.1'
	# OAuth endpoints given in the LinkedIn API documentation (you can check for the latest updates)
	authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
	token_url = 'https://www.linkedin.com/oauth/v2/accessToken'


	
	# Authorized Redirect URL (from LinkedIn configuration)
	linkedin = OAuth2Session(client_id, redirect_uri=redirect_url, scope=scope)
	linkedin = linkedin_compliance_fix(linkedin)
	
	# Redirect user to LinkedIn for authorization
	authorization_url, state = linkedin.authorization_url(authorization_base_url)
	print('Please go here and authorize,', authorization_url)
	
	# Get the authorization verifier code from the callback url
	redirect_response = input('Paste the full redirect URL here:')
	
	# Fetch the access token
	linkedin.fetch_token(token_url,client_secret=client_secret,
		include_client_id=True,authorization_response=redirect_response)

	headers = {'X-Restli-Protocol-Version': '2.0.0'}
	r = linkedin.get('https://api.linkedin.com/v2/me')
	print(r.content)


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

