import asyncio
import os

import discord
import psycopg2
import toml
import time
import random
import client as client
import database_interface as database_interface


print('Loading config...')
with open('config.toml', 'r') as f:
    config = toml.load(f)
"""
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
"""
if __name__ == '__main__':
    kagameshi = client.KagameshiBot(token=config['token'])
    kagameshi.run()
