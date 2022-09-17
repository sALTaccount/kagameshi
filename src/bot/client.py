import asyncio
import os
import discord
from discord.ext import commands
import toml

class KagameshiBot():
    def __init__(self, **kwargs):
        self.client = discord.Bot(description='Dataset labeller', intents=discord.Intents.all(), status=discord.Activity(type=discord.ActivityType.watching, name='the stars.'))
        self.client.load_extension('datacog')
        self.kwargs = kwargs
    
    def close(self):
        asyncio.run(self.client.close)
    
    def run(self):
        self.client.run(self.kwargs['token'])
