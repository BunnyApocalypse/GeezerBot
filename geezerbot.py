import discord
import os
from commands import *
import asyncio
from discord import embeds
from discord.enums import Status


client = discord.Client()
token = 'MTkzOTQ3MjcyMTA5NzUyMzIx.DCcT6Q.TmCx00hpqMPmWjWtM2bYyzr178c'
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
                await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!tellmeabout'):
         tellmeabout(message, client)
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run(token)
