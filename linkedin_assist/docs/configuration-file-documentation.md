# Configuration File Documentation  

Only the non-default options are listed below. All other fields are defaults. The `target_url` field could be modified to extract data from another source however this would require some program modification or at least the retrieved data to be in the same format this program is configured.  

  - RUN_TYPE:  
      - "DEVELOPMENT" - this allows the program to run to completion, however will not actually post to LinkedIn. Instead a demo of the post will print to console.  
      - "PRODUCTION" - This should be self explainitory.  
        
  - RUN_MODE:  
      - "AUTO" - Using `crontab` this program can be automated setting this option. Otherwise this can be left balnk for manual runs.
      
  - KEYS: This is were the keys obtained in step 5 should be placed. Do not put this in quotes.  
      - client_id:  get-this-from-linkedin  
      - client_secret:  get-this-from-linkedin  

  - LIMITS:  
      - post_age: In terms of days, how long you'd like the program to ignore suggesting a previously posted job.
      - post_count: In terms of times posted, how many posts you'd like to limit a previously posted job.
    
  - SELECTION_OPTION: When RUN_MODE is set to AUTO this option determines how many of the post suggestions to post. Use an integer.  

  - KEYWORDS:  
      - job_title: List the words that you'd expect to find in the job title which you'd like to post.
      - hashtags: List the hashtags to include with each post.
