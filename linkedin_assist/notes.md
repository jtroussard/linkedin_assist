# Notes

## Global

1. After reworking this app three times, I feel the for looping through dictionaries to keep tabs on posts and make matches across the application are a bit ugly and perhaps this app would benefit from a DBMS... look into that... maybe MongoDB since I won't have to worry about secruity too much... I guess after the application runs the db can dump a setup file for the next run? I dunno ask around for advice on this... perhaps a master json file could replace a DBMS... just need a nicer way to flip through dicts and make matches on the key value for GUID.

2. For development and production runs --- set it up so that instead of having a module named vault that you just tuck a dev config copy in to dnt folder and have it draw the file from there if the runtype is set to DEVELOPMENT and if it is production, set it to the one that is sitting in the project directory

3. Additionally see if you can expand on the run types, instead of just having a test print and production run type create a run type that interacts with the API in a way, research and see if the linkedin api has a sandbox feature where you can test share your post and inspect the status codes.

2. Also read up on sys.exit() and find a graceful way to shut down program when there is nothing to post of user quits program.

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
    - Noticed in this function that the linkedin user identifier, URN could probably be a class variable since the program will only post for one user at a time.
    - There are a lot of comments in this function related to the format of the post once it hits linkedin, this could be moved and used as part of another user interaction, giving a preview of the post before sending it off.