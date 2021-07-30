from app import keep_alive
from random import randint
from replit import db
import requests
import random
import discord
import json
import os

client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']

starter_encouragements = ['Cheer up!', 'Hang in there.', 'You are a great person!']

if 'responding' not in db.keys():
  db['responding'] = True

def roll_multiple_dice(dice):
  times, num_mod = dice.split('d')
  if '+' in num_mod:
    number, modifier = num_mod.split('+')
    modifier = int(modifier)
  elif '-' in num_mod:
    number, modifier = num_mod.split('-')
    modifier = -int(modifier)
  else:
    number, modifier = int(num_mod), 0
  
  if not times:
    return roll_die(int(number)) + modifier
  elif int(times) > 0:
    return sum([roll_die(int(number)) for x in range(int(times))]) + modifier
  return 0

def roll_die(max_value):
  if max_value > 0:
    return randint(1, max_value)
  else:
    return 0

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' - ' + json_data[0]['a']
  return quote

def update_encouragements(message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [message]

def delete_encouragement(index):
  encouragements = db['encouragements']
  print(encouragements)
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db['responding']:
    options = starter_encouragements
    if 'encouragements' in db.keys():
      options += db['encouragements']

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  try:
    if msg.startswith('$new'):
      encouraging_message = msg.split('$new ', 1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send('New message added.')

    if msg.startswith('$del'):
      encouragements = []
      if 'encouragements' in db.keys():
        index = int(msg.split('$del ', 1)[1])
        delete_encouragement(index)
        encouragements = db['encouragements']
      await message.channel.send(list(encouragements))

    if msg.startswith('$list'):
      encouragements = []
      if 'encouragements' in db.keys():
        encouragements = db['encouragements']
      await message.channel.send(list(encouragements))

    if msg.startswith('$responding'):
      value = msg.split('$responding ', 1)[1]

      if value.lower() == 'true':
        db['responding'] = True
        await message.channel.send('Responding is on.')
      else:
        db['responding'] = False
        await message.channel.send('Responding is off.')

    if msg.startswith('$roll'):
      value = msg.split('$roll ', 1)[1]
      dice = value.split()
      rolls = []
      total = 0
      for die in dice:
        rolls.append(roll_multiple_dice(die))
      await message.channel.send(f'You rolled: {rolls}')

  except Exception as e:
    print(e)

keep_alive()
client.run(os.getenv('TOKEN'))
