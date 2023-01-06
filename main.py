import os
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    members = '\n -'.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message) -> str:
    if message.author == client.user:
        return

    if message.content.startswith('!trivia'):
        question = get_question()
        await message.channel.send(question)

def get_question():
    response = requests.get("http://127.0.0.1:8000/trivia/")
    print(response.status_code)
    json_data = json.loads(response.text)
    question = json_data[0]['question']
    return(question)


class WarHammerQuestionBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True


client.run(TOKEN)

