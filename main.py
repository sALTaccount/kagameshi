import asyncio
import os

import discord
import psycopg2
import toml
import time
import random

import database_interface

from os import listdir
from os.path import isfile, join
from discord.ext import tasks

print('Loading config...')
with open('config.toml', 'r') as f:
    config = toml.load(f)

print('Loading file list...')
bucket_path = 'dataset\\' + config['bucket']
start = time.time()
files = [f for f in listdir(bucket_path) if isfile(join(bucket_path, f))]
end = time.time()
print(f'Loaded {len(files)} files in {round(end - start, 3)} seconds')
print('connecting to database...')
db_connection = psycopg2.connect(
    host=config['host'],
    database=config['database'],
    user=config['user'],
    password=config['password'])

cursor = db_connection.cursor()
print('Connected!')

database_interface.create_table_if_not_exist(db_connection)

# remove images that we already have in the dataset
db_response = database_interface.get_responses(db_connection)
if db_response is not None:
    # each item is a tuple of strings as follows: (image_name, bucket, user_id, response)
    for entry in db_response:
        if config['bucket'] == entry[1]:
            try:
                files.remove(entry[0])
            except Exception as error:
                print(f'error removing file entry {entry[0]}, {error}')

global current_image
global current_message_id
global channel


class KagameshiClient(discord.Client):
    async def on_message(self, message):
        global channel
        global current_image
        if message.channel.id != channel.id:
            return
        if message.author.bot:
            return
        if message.reference is None:
            await message.add_reaction('❌')
            await message.reply("You must reply to the image to have your response recorded!")
            return
        if message.reference.message_id == current_message_id:
            database_interface.insert_response(db_connection,
                                               current_image,
                                               config['bucket'],
                                               str(message.author.id),
                                               message.content)
            await message.add_reaction('✅')
            print(database_interface.get_responses(db_connection))
            return

        await message.add_reaction('❌')

    async def start_image_loop(self):
        global channel
        global current_message_id
        global current_image
        while True:
            current_image = random.choice(files)
            files.remove(current_image)
            message = await channel.send(
                file=discord.File(os.path.join(os.getcwd(), bucket_path, current_image)))
            current_message_id = message.id
            await asyncio.sleep(config['timer_delay'])

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        global channel
        channel = client.get_channel(int(config['channel']))
        await self.start_image_loop()


intents = discord.Intents.default()
intents.message_content = True

client = KagameshiClient(intents=intents)
client.run(config["token"])
