"""
So that your posts don't come across AS spammy the program will randomly select a canned message from this list. At the moment the fields CITY and TITLE can be used anywhere in the message. To add more variables they need referenced from the job JSON object passed to the calling method, search for this line in the main program:

msg = hs.create_message(job, messages.MESSAGES)

Whatever is in the job JSON object is usable.

Notes:

$ = converts the title value to plural with the english module.
"""

STRINGS = {
	'manual_auth_prompt': 'Attention! You will be taken to a LinkedIn page to authenticate.\nEnter Linkedin user login credentials, accept, and then follow\nthese instructions.\n\nTo athenticate;\n   1. Copy the URL from the browser after signing into LinkedIn\n   2. Return to this terminal.\n   3. Paste the address in the prompt and press the ENTER key.\n\n                        [Press ENTER]\n',
	'main_token_not_found': '\n============================================================\nOAuth2 token not found. User will have to authenticate.\n============================================================\n\n             Please follow the prompts.\n',
	'main_token_present':'\n============================================================\nOAuth2 token present, will attempt to use token.\n============================================================\n\n',
	
	}