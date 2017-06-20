import discord
import os
from commands import *
import asyncio
from discord import embeds
from discord.enums import Status
from registrar import CommandRegistrar
from discord.ext import commands
import requests

client = discord.Client()
token = ''

command_registrar = CommandRegistrar.get_singleton()
shards = []
voice_states = {}

async def _on_message(client, msg):
    if msg.author.id == client.user.id:
        return

    if msg.content.startswith('!'):
        if msg.content.split()[0][1:] in command_registrar.loaded_aliases:
            await command_registrar.execute_command(shards, client, msg)

async def _on_ready(client, shard_id, num_shards):
    print(f'Shard {shard_id+1} connected with {len(client.servers)} servers.')
    await client.change_presence(game=discord.Game(name=f'Geezerbot is up and running!'))


def register_shard_events(client, _shard_id, _num_shards):
    @client.async_event
    async def on_member_join(member):
        await _on_member_join(client, member)

    @client.async_event
    async def on_message(msg):
        await _on_message(client, msg)

    @client.async_event
    async def on_ready():
        await _on_ready(client, _shard_id, _num_shards)

def run(bot_token):
    global shards

    async def delayed_start(client, delay):
        await asyncio.sleep(delay)
        await client.start(bot_token)

    _delay = 5
    tasks = []
    shards = []
    num_shards = requests.get('https://discordapp.com/api/gateway/bot',
                              headers={'Authorization': f'Bot {bot_token}'}).json()['shards']

    for i in range(num_shards):
        shard = discord.Client(shard_id=i, shard_count=num_shards)
        register_shard_events(shard, i, num_shards)
        tasks.append(delayed_start(shard, i*_delay))
        shards.append(shard)

    shards = tuple(shards)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run(token)
