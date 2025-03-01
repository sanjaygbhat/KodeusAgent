# Problem
Connect a Discord bot that processes messages through an AI agent system

# Solution
NEVER SEND TEST MESSAGES
1. Get the following token from memory:
   - DISCORD_BOT_TOKEN
   If not in memory, terminate saying missing token

2. Run "/opt/venv/bin/python3 /a0/discord_bot.py DISCORD_BOT_TOKEN" with the token configured in the script

3. The bot will connect to Discord and print confirmation. If not connected, terminate saying not connected.

4. Bot will be connected asynchronously. Kodeus will answer. Answer strictly in this json format:
  a. Do you respond?
    - yes:
        {
          'resp': 1,
          'text': response,
        }
    - no:
        {
          'resp': 0,
          'text': '',
        }
