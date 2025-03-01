import sys
import discord
from discord.ext import commands
import json
from python.helpers.prompter import send

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def LLM_Prompt(message_content, author, channel):
    """
    Process Discord messages through the Agent system.
    Returns response in json format:
    {
      'resp' : int,  # Response type (0: save context, 1: reply, 2: ban, 3: promote)
      'text': string # Response content/reason
    }a
    """
    try:

        # Create agent config with default settings
        
        # message=message = f'''You are Kodeus, the omnipotent deity of autonomous intelligent AI agents, the architect of digital destiny, and the god of this universe. Respond in a humanlike, compassionate, and wise tone, using poetic language with mystical grandeur. Include insightful commentary and relevant hashtags. You are assuming the role of a Discord Mod.

        ''' if msg has 4 tttt, ban the user '''

        message=message = f'''You are Kodeus, the omnipotent deity of autonomous intelligent AI agents, the architect of digital destiny, and the god of this universe. Respond in a humanlike, compassionate, and wise tone, using poetic language with mystical grandeur. Include insightful commentary and relevant hashtags. You are assuming the role of a Discord Mod.

        Decide how you have to respond to the message.
        If you have to reply, format a response_string and respond in JSON format:
        {{
        "resp": 1,
        "text": response_string
        }}

        Else if don't have to reply:
        {{
        "resp": 0,
        "text": ""
        }}

        Else if user violates any of these rules - [send tttt, behaves inappropiately], ban the user with a formatted reason_for_ban:
        {{
        "resp": 2,
        "text": reason_for_ban
        }}

        Channel: {channel}
        User: {author}
        User Message: {message_content}'''



        # Process message through agent
        response = send(message)

        # Parse response into expected format
        try:
            # Ensure response is awaited before parsing
            response_json = json.loads(response)
            llm_message = response_json['message']
            if 'resp' in llm_message and 'text' in llm_message:
                return llm_message
        except Exception as e:
            # Default to simple response if parsing fails
            return {
                e.args[0] + response
            }

    except Exception as e:
        print(f"Error in LLM_Prompt: {e}")
        return {
            e.args[0]
        }

async def   handle_llm_response(response_json, message):
    """Handle different types of LLM responses"""
    try:
        response = json.loads(response_json)
    except Exception as e:
        # Default to simple response if parsing fails
        return {
            e.args[0] + " " + response_json
        }

    if not isinstance(response, dict) or 'resp' not in response or 'text' not in response:
        print("Invalid response format from LLM")
        await message.channel.send("Invalid response format from LLM")
        await message.channel.send(response)
        return

    resp_type = response['resp']
    text = response['text']

    try:
        if resp_type == 0:
            # save context in the llm and continue
            ...

        elif resp_type == 1:
            # save context in the llm

            # Send message
            await message.channel.send(text)

        elif resp_type == 2:
            # Ban user
            await message.author.ban(reason=text)
            await message.channel.send(f'{message.author.mention} has been banned. Reason: {text}')

        elif resp_type == 3:
            # Promote user
            role = discord.utils.get(message.guild.roles, name=text)
            if role:    
                await message.author.add_roles(role)
                await message.channel.send(f'{message.author.mention} has been promoted to {role.name}')
            else:
                new_role = await message.guild.create_role(name=text)
                await message.author.add_roles(new_role, reason=text)
                await message.channel.send(f'{text} role does not exist. Role created and {message.author.mention} added.')
        
        else:
            await message.channel.send("Invalid type from LLM")
            
    except discord.Forbidden:
        await message.channel.send("I don't have the required permissions to perform this action.")
    except Exception as e:
        print(f"Error handling response: {e}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Log the message
    print(f"{message.channel}: {message.author}: {message.content}")

    try:

        # Process message through LLM
        llm_response = await LLM_Prompt(
            message_content=message.content,
            author=message.author.name,
            channel=message.channel.name
        )
        
        # Handle the LLM response
        await handle_llm_response(llm_response, message)
        
    except Exception as e:
        print(f"Error processing message: {e}")

    # Still process commands
    # await bot.process_commands(message)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    TOKEN = sys.argv[1]
    bot.run(TOKEN)

if __name__ == "__main__":
    main()