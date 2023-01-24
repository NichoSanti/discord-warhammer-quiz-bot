import os
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
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


def get_question():
    question = ''
    id = 1
    answer = 0
    response = requests.get("http://127.0.0.1:8000/trivia/random")
    json_data = json.loads(response.text)
    question += json_data[0]['title'] + '\n'
    for item in json_data[0]['answer']:
        question += str(id) + "." + item['answer'] + "\n"

        if item['is_correct']:
            answer = id
            
        id += 1

    return(question, answer)

@client.event
async def on_message(message) -> str:
    if message.author == client.user:
        return

    if message.content.startswith('!trivia'):
        question, answer = get_question()
        await message.channel.send(question)

        def check(m):
            return m.author == message.author and m.content.isdigit()
        try:
            guess = await client.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            return await message.channel.send('Timeout')

        if int(guess.content) == answer:
            await message.channel.send('You got it right!')
        else:
            await message.channel.send('Try again')

class WarHammerQuestionBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True


client.run(TOKEN)

