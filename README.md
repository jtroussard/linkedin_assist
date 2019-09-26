LinkedIn Assist Terminal Application (Share automation)
==================

## Purpose  

A python program to collect job data and partially automate shares to user's LinkedIn account. For this version, job data is sourced from the career website of [Dollar Bank FSB](https://dollarbankcareers.dejobs.org/). Maybe even earn that sweet referral :moneybag: bonus :moneybag:
> **Important Note:**
> This is **NOT a production quality program** and does not adhere to best practices/security recommendations from LinkedIn or the maintainers of Requests HTTP library for Python.
> This is a toy program to experiment with LinkedIn API, application designs, and project structure. It is intended to be **RUN LOCALLY ONLY**. Do not host this publicly without considering security and vulnerabilities to end users.

## Environment  

This program was developed for **Ubuntu 18.04**, and has not been tested in any other environment. If using this program, it is strongly suggested to setup in the same environment.

#### Tested Environments  
- Ubuntu 16.04 [OK!]

## Setup - For running the program manually.  

1. Install major dependencies.  
    -  [Install Python 3.x](https://www.python.org/downloads/)
    -  Install venv (You might have to use the `sudo` command)  
    `$ apt-get install python3-venv`
    -  During authentication a browser will need to be used. At this point the only browser supported is **Firefox**.
    
2. Clone this repository onto your local machine.  
`$ git clone https://github.com/jtroussard/linkedin_assist.git`

3. Change into the root project directory and setup a virtual environment.  
`$ cd linkedin_assist && python3 -m venv && source venv/bin/activate`  

4. Install program level dependencies.  
`$ pip3 install -r requirements`  

5. Obtain LinkedIn OAuth2 app credentials. Open the following link in a new tab/window for instructions.
[Get LinkedIn Credentials](https://github.com/jtroussard/linkedin_assist/blob/master/linkedin_assist/docs/get-linkedin-keys.md)  

6. Fill out the configuration file. Open the configuration file, `linkedin_assist/linkedin_assist/config/cfg.yaml` using a text editor and fill out the options. A short document mapping all the non-default options can be found at the following link, [LinkedIn Configuration File Documentation](https://github.com/jtroussard/linkedin_assist/blob/master/linkedin_assist/docs/configuration-file-documentation.md).  

7. Program is ready to be kicked off. Follow prompts to create posts.  
`$ cd ./linkedin_assist && python3 app.py config/cfg.yaml`


## Programming Notes  

Moved to ./linkedin_assist/docs/notes.md  

## Progress (Version 1.0)  
- [X] YOLO code.
- [X] Modularize.
- [X] Add selection feature ~~NpyScreen~~ PyInquirer
- [X] ~~Persistent token.~~ **Renewing tokens is not available to normal consumer. See programming notes for details.**
- [X] CRON automation with e-mail alerts.
- [ ] Test and verify entire program. (WIP)
- [ ] Create documentation. (WIP)

## Version 1.1
- [ ] Drop english.py and replace with Python Pattern. (NLP library)
- [ ] Add function to verify link to post posting is good.
- [ ] Possible consolidation of configuration files (At least use the same standard across config files.)
- [ ] Test and verify.
- [ ] Update documentation.

## Version 1.2
- [ ] Include image with post.
- [ ] Restructure for image hosting/storage/reference.
- [ ] Add configuration for browser selection.
- [ ] Update documentation.

## Version 2.0
- [ ] Convert to web application framework. (Django)
- [ ] Implement backend. (PostgreSQL)
- [ ] Implement best practices/security/apply ssl.
- [ ] Test and verify.
- [ ] Update documentation.

## Version 2.1
- [ ] Create dashboard.
- [ ] Test and verify.
- [ ] Update documentation.

## Version 2.2
- [ ] Add data viz to dashboard.
- [ ] Create functions to measure and predict impact of posts.
- [ ] Test and verify.
- [ ] Update documentation.

## Possible Upgrades  
- Picture generator. (1.2)
- Web Application Version. (2.0)
- Create dashboard: Post history, frequency, and impact is possible. (2.1)
- Track and offer statistical analysis on posts. (2.2)
- ~~Variable post message formats. (1.0)~~ __DONE__
- ~~Determine and add collection of hashtags to posts. (1.0)~~ __DONE__
- Browser preference selection or perhaps autodetection feature. (1.2)
- ~~Embed SQLite, drop files altogether.~~ Implement backend. (2.0)
- Build out LinkedIn class into my own vanilla lib. (?)
- Double check job post link (404/missing/titles match?) (1.1)
