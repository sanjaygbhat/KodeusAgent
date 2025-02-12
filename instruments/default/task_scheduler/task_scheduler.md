# Problem
Perform a task with a given schedule. 
# Solution
1. collect the schedule and text from the user 
2. format schedule into an at command schedule and call it user_schedule
3. run the at job with command: echo "/opt/venv/bin/python3 /a0/python/helpers/prompter.py <text>" | at <user_schedule>
4. wait for the terminal to finish 