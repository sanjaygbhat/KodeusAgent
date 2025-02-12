# Problem
Perform a recurring task with a given schedule. 
# Solution
1. collect the schedule and text from the user 
2. format schedule into cron command schedule and call it user_schedule
3. run the cron job with command "<user_schedule> /opt/venv/bin/python3 /a0/python/helpers/prompter.py <text>"
4. wait for the terminal to finish 