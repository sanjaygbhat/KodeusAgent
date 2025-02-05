# Problem
Post a tweet on X
# Solution
NEVER SEND TEST TWEETS
1. Get the following tokens from memory:
   -  X_TWITTER_API_TOKEN_KEY 
   -  X_TWITTER_API_TOKEN_SECRET 
   -  X_TWITTER_ACCESS_TOKEN 
   -  X_TWITTER_ACCESS_TOKEN_SECRET
   If not in memory, terminate saying missing tokens
2. Run "python3 /a0/instruments/default/x_tweet/x_tweet.py X_TWITTER_API_TOKEN_KEY X_TWITTER_API_TOKEN_SECRET X_TWITTER_ACCESS_TOKEN X_TWITTER_ACCESS_TOKEN_SECRET <text>" with text from the user
3. Wait for the terminal to finish 