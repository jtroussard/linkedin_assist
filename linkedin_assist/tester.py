import requests, yaml, json, os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
from quick_fixes.oauth2_session import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
from yaml import Loader, Dumper
vault = open('./dnt/vault.yaml','r')
v = yaml.load(vault, Loader=Loader)
config = open('./config/cfg.yaml', 'r')
c = yaml.load(config, Loader=Loader)
client_id = v['KEYS']['client_id']
client_secret = v['KEYS']['client_secret']
scope = ['r_liteprofile', 'w_member_social']
redirect_url = c['URLS']['li_api_redirect']
authorization_base_url = c['URLS']['li_api_auth_base']
token_url = c['URLS']['li_api_token']

session = OAuth2Session(client_id, redirect_uri=redirect_url, scope=scope)
session = linkedin_compliance_fix(session)
authorization_url, state = session.authorization_url(authorization_base_url)
import webbrowser
controller = webbrowser.get('firefox')
controller.open(authorization_url)
redirect_response = input('Paste the full redirect URL here:')
session.fetch_token(token_url,client_secret=client_secret,include_client_id=True,authorization_response=redirect_response)

r = linkedin.get('https://api.linkedin.com/v2/me')
print(r.content)







