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
encouragements = ['Cheer up!', 'Hang in there.', 'You are a great person!']
base_stats = {'str': 10, 'con': 10, 'dex': 10, 'int': 10, 'wis': 10, 'cha': 10}
combat_stats = {'armor_class': 10, 'initiative': 0, 'speed': 30}

if 'responding' not in db.keys():
  db['responding'] = True
if 'xp' not in db.keys():
  db['xp'] = {}
if 'stats' not in db.keys():
  db['stats'] = {}
if 'combat_stats' not in db.keys():
  db['combat_stats'] = {}

def initialize_stats(character):
  if character:
    db['stats'][character] = base_stats
    db['combat_stats'][character] = combat_stats
    return f'Stats initialized for {character}'
  return 'Stats not initialized'

def get_stats(character):
  if db['stats'].get(character):
    return dict(db['stats'][character])
  return f'No stats for {character}'

def get_combat_stats(character):
  if db['combat_stats'].get(character):
    return dict(db['combat_stats'][character])
  return f'No combat stats for {character}'

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

def get_xp(character):
  xp = db['xp'].get(character.lower())
  if xp is not None:
    return f'{character} has {xp} experience points'
  return f'No experience found for {character}'

def update_xp(character, xp):
  if character and xp is not None and db['xp'].get(character):
    db['xp'][character.lower()] += int(xp)
    return f'Added {xp} experience points for {character}'
  elif character and xp is not None:
    db['xp'][character.lower()] = int(xp)
    return f'Added {xp} experience points for {character}'
  return f'No experience added for {character}'

def delete_xp(character):
  xp = db['xp'].get(character.lower())
  if xp is not None:
    del db['xp'][character.lower()]
    return f'Deleted experience points for {character}'
  return f'No experience found for {character}'

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
    options = encouragements
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

    if msg.startswith('$addxp'):
      value = msg.split('$addxp ', 1)[1]
      character, xp = value.split()
      await message.channel.send(update_xp(character, xp))

    if msg.startswith('$showxp'):
      character = msg.split('$showxp ', 1)[1]
      await message.channel.send(get_xp(character))

    if msg.startswith('$removexp'):
      character = msg.split('$removexp ', 1)[1]
      await message.channel.send(delete_xp(character))

    if msg.startswith('$initstats'):
      character = msg.split('$initstats ', 1)[1]
      await message.channel.send(initialize_stats(character))

    if msg.startswith('$stats'):
      character = msg.split('$stats ', 1)[1]
      await message.channel.send(get_stats(character))

    if msg.startswith('$combat'):
      character = msg.split('$combat ', 1)[1]
      await message.channel.send(get_combat_stats(character))
  except Exception as e:
    print(e)

if __name__ == "__main__":
  keep_alive()
  client.run(os.getenv('TOKEN'))
