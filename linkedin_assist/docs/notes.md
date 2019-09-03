# Notes

## From README.md


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


## Global

1. ~~After reworking this app three times, I feel the for looping through dictionaries to keep tabs on posts and make matches across the application are a bit ugly and perhaps this app would benefit from a DBMS... look into that... maybe MongoDB since I won't have to worry about secruity too much... I guess after the application runs the db can dump a setup file for the next run? I dunno ask around for advice on this... perhaps a master json file could replace a DBMS... just need a nicer way to flip through dicts and make matches on the key value for GUID.~~ __Moved__ SQLite added to possible future updates list.

2. ~~For development and production runs --- set it up so that instead of having a module named vault that you just tuck a dev config copy in to dnt folder and have it draw the file from there if the runtype is set to DEVELOPMENT and if it is production, set it to the one that is sitting in the project directory~~ __Complete__

3. ~~Additionally see if you can expand on the run types, instead of just having a test print and production run type create a run type that interacts with the API in a way, research and see if the linkedin api has a sandbox feature where you can test share your post and inspect the status codes.~~

4. Also read up on sys.exit() and find a graceful way to shut down program when there is nothing to post of user quits program.

5. Wrap up version 1 asap and then do a arch restructure of the program where the job data remains intact and passed through the program instead of building all these lists. Update records using the intact data via the use of sub functions i.e. hs.search(x,x,x,x,type of search, etc...)

6. ~~Token persistence. Store token somewhere check if present first thing....~~  

## app.py

### Main

1. Think about how to check for inactive guids and remove them from the records.json file.

### Functions

1. get_job_data
    - Consider checking for empty return or checking response status. Function can return a dictionary with go/nogo indicator and possible payload.

## LinkedinAssist.py

### Logic/Approach

1. Find time to unhardcode post message so that it can be referenced from configuration and referenced into form post and test posts.

### Functions

1. form_post
    - This thought was not entirely true, so the note can be ignored. ~~Noticed in this function that the linkedin user identifier, URN could probably be a class variable since the program will only post for one user at a time.~~
    - There are a lot of comments in this function related to the format of the post once it hits linkedin, this could be moved and used as part of another user interaction, giving a preview of the post before sending it off.
