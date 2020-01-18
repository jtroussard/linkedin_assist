#!/usr/bin/python3 5D4D96B080D656A6B34A29C64894B852.txt

"""Terminal program to partially automate Linkedin Shares"""

__author__ = "Jacques Troussard"
__copyright__ = "Copyright 2019, TekkSparrow"

import datetime as dt
import json
import selector
import sys

import helpers as hs
from classes.LinkedinAssist import LinkedinAssist
from config import messages
from config.strings import STRINGS as s

today = dt.datetime.today()


def main_func():

    # Get configurations and load into local variable.
    config = hs.import_configurations(sys.argv)
    if not config:
        sys.exit()

    # Unpack the configuration variables
    RUN_MODE = config["RUN_MODE"]
    RUN_TYPE = config["RUN_TYPE"]
    TARGET_URL = config["URLS"]["target_url"]
    KEYWORDS = config["KEYWORDS"]["job_title"]
    HASHTAGS = config["KEYWORDS"]["hashtags"]
    FN_SAVED_GUIDS = config["FILES"]["saved_guids"]
    FN_RECORDS = config["FILES"]["records"]
    LIMITS = config["LIMITS"]
    API_URL_GET_USER = config["URLS"]["li_api_get_user_profile"]

    # Fetch JSON format job posting data. Store current data to guid file.
    data = hs.get_job_data(TARGET_URL)

    # Filter out non-IT jobs.
    it_jobs = hs.filter_data(data, KEYWORDS)

    # Create KEEP and REMOVE list.
    keep_remove = hs.compare_and_keep(it_jobs, FN_SAVED_GUIDS)
    keepers = keep_remove["keep"]

    # Create a list of GUIDS from which the user can choose from.
    suggestions = hs.make_suggestions(keepers, it_jobs, FN_RECORDS, LIMITS)

    # Interface with user.
    if len(suggestions) == 0:
        print("Nothing to post for now. Check back again soon. Exiting program.")
        sys.exit()
    else:
        job_list_json = []
        for job in it_jobs:
            if job["guid"] in suggestions:
                job_list_json.append(job)
        if RUN_MODE == "MANUAL":
            user_selections = selector.present_menu(job_list_json)
        else:
            user_selections = hs.apply_config_selections(config, job_list_json)

    # Make connection with LinkedIn API
    if user_selections:
        linkedin_assist_obj = LinkedinAssist(
            config
        )  # <-- Basically a modified OAuth2 Request Object

        # Check for existing token
        try:
            token_file = open("./data/token")
            token = json.load(token_file)
            linkedin_assist_obj.get_access(token=token)
            print(s["main_token_present"])
        except IOError:
            print(
                "[main] Warning: File access error. Reverting to manual authentication."
            )

        # Perform manual authentication if Token isn't present or expired.
        if not linkedin_assist_obj.session.authorized:
            if RUN_MODE != "AUTO":
                linkedin_assist_obj.get_access()
                if not linkedin_assist_obj.session.authorized:
                    print(
                        "[main] Error: Authentication could not be made. Exiting Program"
                    )
                    sys.exit()
            else:
                print("[main] Authentication Error: Token problem. Possibly expired.")
                sys.exit()
        # Token is good - save to file for future use.
        else:
            try:
                with open("./data/token", "w") as token_save:
                    token_save.seek(0)
                    json.dump(token, token_save, indent=2)
                    token_save.truncate()
            except IOError:
                print("[main] Error saving token to file.")

        # Set URN
        urn = linkedin_assist_obj.get_urn(API_URL_GET_USER)

        try:  # POST request to LinkedIn & update records

            # Load records file (date last posted, total times posted)
            with open(FN_RECORDS, "r+") as r:
                records = json.load(r)

                # For each selection:
                #  1. Create the base message (from random message bank (templates))
                #  2. Add hashtags from hashtagbank
                #  3. edit_language is a catch all method to fix small language bugs for example using UX abbrv. (might move this into the english module.)
                #  4. Create the job request post.
                #  5. Submit request to POST or print to console.
                for selection in user_selections["posts"]:
                    job = hs.search(selection.split(":")[1].strip(), job_list_json)
                    msg = hs.create_message(job, messages.MESSAGES)
                    msg = hs.add_hashtags(msg, HASHTAGS)
                    msg = hs.edit_language(msg)
                    post = linkedin_assist_obj.form_post(job, urn, msg)
                    if linkedin_assist_obj.make_posts(post):
                        if ("DEVELOPMENT" or "TEST") in RUN_TYPE:
                            print("DEMO print:")
                        else:
                            print("POSTED text:")
                            hs.update_records(r, records, job, today)
                        print(msg)
                        print("\nSuccess! [{}]\n\n".format(job["title"]))
                    else:
                        print("\nFailed :( [{}]\n\n".format(job["title"]))
        except IOError:
            print("[main] Error: Records file could not be accessed.")
            print(
                "              No posts made to LinkedIn:\n\n{}".format(sys.exc_info())
            )
            raise
    else:
        print("No shares made to LinkedIn. Exiting Program.")
    # clean_up() <-- Maybe create a clean up step in the future.


if __name__ == "__main__":
    try:
        main_func()
    except SystemExit:
        pass
    except:
        print("Error:{}".format(sys.exc_info()))
        raise
