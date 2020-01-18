from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
from time import sleep

import os, json, yaml
from config.strings import STRINGS as s


class Vault:
    def __init__(self, config):
        self.config = config
        self.CLIENT_ID = config["KEYS"]["client_id"]
        self.CLIENT_SECRET = config["KEYS"]["client_secret"]


class LinkedinAssist:
    """Creates a very manual type connection to LinkedIn API,
    and then acts as a delivery vehicle for formated posts.
    """

    def __init__(self, config, job_data=[], session=None):
        """Construct a new LinkedinAssist Object.

        :param job_data: list of JSON objects containing job post 
                         data. Data is unformated for Linkedin
                         share ppost.
        :param session: Linkedin OAuth2 session obj."""
        self.job_data = job_data
        self.session = session
        self.config = config
        self.authorized = False
        self.uri = None

        if config["RUN_TYPE"] == "DEVELOPMENT":
            try:
                from yaml import Cloader as Loader, CDumper as Dumper
            except ImportError:
                from yaml import Loader, Dumper
            try:
                with open(config["FILES"]["dev_vault"], "r") as dev_keys:
                    v = yaml.load(dev_keys, Loader=Loader)
                    self.vault = Vault(v)

            except IOError:
                print("Error loading development keys: {}")
                raise
        else:
            self.vault = Vault(config)

    def get_access(self, token=None):
        """Have the user authenticate."""

        """ This is NOT a production quality program ad the os environ attr
        is being set accordingly. Only run this program locally"""
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        """ Made some changes to OAuth2Session class to work around some 
        bugs introduced by linkedin's API updates and changes."""
        # from requests_oauthlib import OAuth2Session
        from dnt.devlib.roa2.requests_oauthlib.oauth2_session import OAuth2Session
        from dnt.devlib.roa2.requests_oauthlib.compliance_fixes import (
            linkedin_compliance_fix,
        )

        # from quick_fixes.oauth2_session import OAuth2Session
        # from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

        # Credentials you get from registering a new application
        client_id = self.vault.CLIENT_ID
        client_secret = self.vault.CLIENT_SECRET

        # Scope is necessary to avoid permission errors
        scope = ["r_liteprofile", "w_member_social"]
        redirect_url = self.config["URLS"]["li_api_redirect"]

        # OAuth endpoints given in the LinkedIn API documentation .
        authorization_base_url = self.config["URLS"]["li_api_auth_base"]
        token_url = self.config["URLS"]["li_api_token"]

        self.session = OAuth2Session(
            client_id, redirect_uri=redirect_url, scope=scope, token=token
        )
        self.session = linkedin_compliance_fix(self.session)
        authorization_url, state = self.session.authorization_url(
            authorization_base_url
        )

        if not self.session.token:
            input(s["manual_auth_prompt"])
            # Redirect user to LinkedIn for authorization
            import webbrowser

            controller = webbrowser.get("firefox")
            controller.open(authorization_url)
            # Get the authorization verifier code from the callback url
            redirect_response = input("Paste the full redirect URL here:")
            self.session.fetch_token(
                token_url,
                client_secret=client_secret,
                include_client_id=True,
                authorization_response=redirect_response,
            )
        return self.session

    def get_urn(self, res_link):
        # Extract the Linkedin URN
        r = self.session.get(res_link)
        print(r)
        return r.json()["id"]

    def form_post(self, job, urn, message):
        # LINKEDIN SHARE FORMAT TESTING ZONE & INFO ##########################
        # From counting looks like about 80 characters per line
        # Third line cut off is at 70ish
        #          10        20        30        40        50        60        70        80
        # 012345678901234567890123456789012345678901234567890123456789012345678901234567890
        # Pittsburgh, PA area IT job seekers, Dollar Bank is looking for a wicked talented
        # Systems Administrator Level II to join our team! Interested? Follow this link to
        # apply, referral mentions greatly appreciated! Also, did you know? This [CUT]
        # post was generated by a python script, check my github(jtroussard) account for more details.

        # {} area IT job seekers, Dollar Bank is looking for a wicked talented {} to join our team! Interested? Follow this link to apply, referral mentions greatly appreciated! Also, did you know? This post was generated by a python script, check my github(jtroussard) account for more details."

        ######################################################################
        p = {
            "author": "urn:li:person:{}".format(str(urn)),
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {
                                "text": "{} - {}".format(job["title"], job["city"])
                            },
                            "originalUrl": job["url"],
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }
        return json.dumps(p)

    # The returns for this function definitely feel stupid. Sleep on this and figure out a less convoluted way of returning status on this function.
    # Yeah what's up withi this dooder... figure something out.
    def make_posts(self, job):
        status = 0
        req_link = self.config["URLS"]["li_api_share"]
        if self.config["RUN_TYPE"] == "PRODUCTION":
            r = self.session.post(
                req_link,
                data=job,
                headers={
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0",
                    "x-li-format": "json",
                },
            )
            sleep(3)
        elif ("DEVELOPMENT" or "TEST") in self.config["RUN_TYPE"]:
            # elif self.config['RUN_TYPE'] == 'DEVELOPMENT':
            job = json.loads(job)
            post_text = job["specificContent"]["com.linkedin.ugc.ShareContent"][
                "shareCommentary"
            ]["text"]

            output = ""
            counter = 0
            for char in post_text:
                counter += 1
                if counter < 80:
                    output = "{}{}".format(output, char)
                else:
                    output = "{}\n{}".format(output, char)
                    counter = 0
            print("\n")
        return True
