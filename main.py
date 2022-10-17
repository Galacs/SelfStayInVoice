import threading
import asyncio
import discord
import random
import os
from discord.ext import commands

import config

tokens = config.get_tokens()

clients = []

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# loop = asyncio.get_event_loop()

for i, token in enumerate(tokens):
    # print(f'I: {i}, K: {token.token}')
    client = commands.Bot(command_prefix=':', self_bot=True, help_command=None)
    @client.event
    async def on_ready():
        
        vc = discord.utils.get(client.get_guild(token.guild_id).channels, id=token.channel_id)
        await vc.guild.change_voice_state(channel=vc,
                                        self_mute=token.self_mute,
                                        self_deaf=token.self_deaf)

        status = random.choice(["online", "dnd", "idle"])

        if random.randint(1,2) == 1:
            await client.change_presence(status=discord.Status(status), activity=discord.Game(name=token.game))
        else:
            await client.change_presence(status=discord.Status(status), activity=None)

        print(f"As {client.user} ({client.user.id}). Joined {vc.name} ({vc.id}).")
    
    loop.create_task(client.start(token.token))
    # client.start(token.token)

    clients.append(client)

loop.run_forever()

while True:
    if input() == 'exit':
        os.kill(os.getpid(), 9)
