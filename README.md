LinkedIn Assist Terminal Application (Share automation)
==================

## Purpose
A python program to collect job data and paritally automate shares to your LinkedIn account. For this version, job data is sourced from the career website of [Dollar Bank FSB](https://dollarbankcareers.dejobs.org/). Maybe even earn that sweet sweet referal bonus :moneybag:
> **Important Note:**
> This is **NOT a production quality program** and does not adhere to best practices/security recommendations from LinkedIn or the maintainers of Requests HTTP library for Python.
> This is a toy program to experiment with LinkedIn API, application designs, and project structure. It is intended to be **RUN LOCALLY ONLY**. Do not host this publicily without considering security and vulnerabilities to end users.


## Setup
1. [Install Python 3.x](https://www.python.org/downloads/)
2. See `requirements.txt` for additional dependencies. Install requirements.

## Getting Started

## Programming Notes
1. Modified OAuth2 Requests library: Under linkedin_assist/linkedin_assist/quick_fixes/ is a modified copy of the oauth2_session.py module. Changes to this module in particular were necessary to line up requests made to LinkedIn's API. Specifically the athentication code gets appended to the request twice, once as "oauth2_access_token" and again as "access_token". When making the request with both parameters the response would indicate unpremitted fields. The only solution I could come up with involved a quick and dirty if statement that checked the url value for the second access_token field, if present it reverts the string to an older version of the url before `.add_token()` method is called. This is all done within the `request()` method. (See code block below) I've made comments on the requests github repo with regards to this issue and recieved no reply. After reviewing the Requests main page, there was a notice that exaplined the library was in maintenance mode only and the contributors/maintainers/developers were engaged with a Requests 3 rollout. [*Side Note: Disheartening but interesting blog post I found while looking into this issue*](https://vorpus.org/blog/why-im-not-collaborating-with-kenneth-reitz/)

```python
old_version_url = url
url, headers, data = self._client.add_token(url, http_method=method, body=data, headers=headers)
# Dirty work around to prevent the `access_token` parameter from being added
# to the url, causing a unpermitted parameters error requesting linkedin resource.
if "&access_token=" in url:
    url = old_version_url
```

2. Npyscreen canceled. I'm sure this is a great library, but personally the documentation left a lot to be desired. I was wondering around the docs for a few hours, tinkering with a few things here and there and decided that to get any value from it I'd have to spend absolutly way to much time. Ultimately the widget classes seemed to be missing lots of interfacing instructions. Also I noticed that passing arbitraty arguments to the add_widget method didn't seem to bother the program at all. I would think at least some sort of warning would be thrown. As I mentioned before, it is probably just above me at this moment as the stress on OOP principles in the tutorial were impressive, it just wasn't very "get something going quickly" friendly. Anyways a little more reading online and I found a more straight forward library, PyInquirer. Without really going into to deep I have a simple selector menu done and might come back and do more with this UI and library.

## Progress (Version 1.0)
- [X] YOLO code.
- [X] Modularize.
- [X] Add selection feature ~~NpyScreen~~ PyInquirer
- [ ] Presistent token.
- [ ] CRON automation with e-mail alerts.
- [ ] Test and verify entire program.
- [ ] Create documentation.

## Possible Upgrades
- Picture generator
- Web Application Version.
- Track and offer statistical analysis on posts made.
- Presistent Token (?)
- ~~Variable post message formats.~~ __DONE__
- ~~Determine and add collection of hashtags to posts.~~ __DONE__ without determination (just simple tag bank)
- Browser preference selection or perhaps autodetection feature.
- Embed SQLite, drop files all together.
- Build out LinkedIn class into my own vanilla lib.
