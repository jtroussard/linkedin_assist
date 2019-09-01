LinkedIn Assist Terminal Application (Share automation)
==================

## Purpose  

A python program to collect job data and partially automate shares to your LinkedIn account. For this version, job data is sourced from the career website of [Dollar Bank FSB](https://dollarbankcareers.dejobs.org/). Maybe even earn that sweet sweet referral bonus :moneybag:
> **Important Note:**
> This is **NOT a production quality program** and does not adhere to best practices/security recommendations from LinkedIn or the maintainers of Requests HTTP library for Python.
> This is a toy program to experiment with LinkedIn API, application designs, and project structure. It is intended to be **RUN LOCALLY ONLY**. Do not host this publicly without considering security and vulnerabilities to end users.

## Environment  

This program was developed for **Ubuntu 18.04**, and has not been tested in any other environment. It is strongly suggested if you'd like to use this program to set yourself up in the same environment.

## Setup - For running the program manually.  

1. Install major dependencies.  
    -  [Install Python 3.x](https://www.python.org/downloads/)
    -  Install venv (You might have to use the `sudo` command)  
    `$ apt-get install python3-venv`  
    
2. Clone this repository onto your local machine.  
`$ git clone https://github.com/jtroussard/linkedin_assist.git`

3. Change into the root project directory and setup a virtual environment.  
`$ cd linkedin_assist && python3 -m venv venv && source venv/bin/activate`  

4. Install program level dependencies.  
`$ pip3 install -r requirements`  

5. Obtain LinkedIn OAuth2 app credentials. Open the following link in a new tab/window for instructions.
[Get LinkedIn Credentials](https://github.com/jtroussard/linkedin_assist/blob/master/linkedin_assist/docs/get-linkedin-keys.md)  

6. Fill out the configuration file. Open the configuration file, `linkedin_assist/linkedin_assist/config/cfg.yaml` in your favorite text editor and fill out the options without quotes. A short document explaining how to configure the options can be found at the following link, [LinkedIn Configuration File Documentation](https://github.com/jtroussard/linkedin_assist/blob/master/linkedin_assist/docs/configuration-file-documentation.md).  

7. Program is ready to be kicked off.  
`$ cd ./linkedin_assist && python3 app.py config/cfg.yaml`

8. 


## Programming Notes  

1. Modified OAuth2 Requests library: Under linkedin_assist/linkedin_assist/quick_fixes/ is a modified copy of the oauth2_session.py module. Changes to this module in particular were necessary to line up requests made to LinkedIn's API. Specifically the authentication code gets appended to the request twice, once as "oauth2_access_token" and again as "access_token". When making the request with both parameters the response would indicate unpremitted fields. The only solution I could come up with involved a quick and dirty if statement that checked the URL value for the second access_token field, if present it reverts the string to an older version of the URL before `.add_token()` method is called. This is all done within the `request()` method. (See code block below) I've made comments on the requests github repo with regards to this issue and received no reply. After reviewing the Requests main page, there was a notice that explained the library was in maintenance mode only and the contributors/maintainers/developers were engaged with a Requests 3 roll out. [*Side Note: Disheartening but interesting blog post I found while looking into this issue*](https://vorpus.org/blog/why-im-not-collaborating-with-kenneth-reitz/)

```python
old_version_URL = URL
URL, headers, data = self._client.add_token(URL, http_method=method, body=data, headers=headers)
# Dirty work around to prevent the `access_token` parameter from being added
# to the URL, causing a unpermitted parameters error requesting linkedin resource.
if "&access_token=" in URL:
    URL = old_version_URL
```

2. Npyscreen canceled. I'm sure this is a great library, but personally the documentation left a lot to be desired. I was wondering around the docs for a few hours, tinkering with a few things here and there and decided that to get any value from it I'd have to spend absolutely way to much time. Ultimately the widget classes seemed to be missing lots of interfacing instructions. Also I noticed that passing arbitrary arguments to the add_widget method didn't seem to bother the program at all. I would think at least some sort of warning would be thrown. As I mentioned before, it is probably just above me at this moment as the stress on OOP principles in the tutorial were impressive, it just wasn't very "get something going quickly" friendly. Anyways a little more reading online and I found a more straight forward library, PyInquirer. Without really going into to deep I have a simple selector menu done and might come back and do more with this UI and library.

## Progress (Version 1.0)  

- [X] YOLO code.
- [X] Modularize.
- [X] Add selection feature ~~NpyScreen~~ PyInquirer
- [?] Persistent token. **Need to add logic to renew expired tokens**
- [ ] CRON automation with e-mail alerts.
- [ ] Test and verify entire program.
- [ ] Create documentation.

## Possible Upgrades  

- Picture generator
- Web Application Version.
- Track and offer statistical analysis on posts made.
- ~~Variable post message formats.~~ __DONE__
- ~~Determine and add collection of hashtags to posts.~~ __DONE__ without determination (just simple tag bank)
- Browser preference selection or perhaps autodetection feature.
- Embed SQLite, drop files all together.
- Build out LinkedIn class into my own vanilla lib.
- Double check job post link (404/missing/titles match?)