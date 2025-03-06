# Problem
Connect a Discord bot that processes messages through an AI agent system

# Solution
NEVER SEND TEST MESSAGES
1. Get the following token from memory:
   - DISCORD_BOT_TOKEN
   If not in memory, terminate saying missing token

2. Ask user to input rules into /a0/instruments/default/discord_bot/rules.md. Once the user confirms, proceed.

3. Run "/opt/venv/bin/python3 /a0/discord_bot.py DISCORD_BOT_TOKEN" with the token configured in the script

4. The bot will connect to Discord and print confirmation. If not connected, terminate saying not connected.

5. Bot will be connected asynchronously. Kodeus will answer. Answer strictly in this json format:
  a. Do you respond
    - if you have to respond:
        {
          'resp': 1,
          'text': response,
        }
    - else if you don't have to respond:
        {
          'resp': 0,
          'text': '',
        }
    - else if you have to ban the person 
        {
          'resp': 2,
          'text': reason for ban,
        }