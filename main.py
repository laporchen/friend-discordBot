import discord
import json
import random


keyPath = "key.json"


def getKey(path):
    with open(path,'rb') as f:
        data = json.load(f)
        return data['Key']

async def sendPic(file,channel):
    with open('img/' + file, 'rb') as f:
        picture = discord.File(f)
        await channel.send(file=picture)

async def nolick(message):
    lick = "lick.jpg"
    await message.channel.send('又舔，又舔，又…又舔嘴唇！')
    await sendPic(lick,message.channel)

async def flash(message):
    flash = "flash.gif"
    await message.channel.send('這什麼到底什麼閃現！')
    await sendPic(flash,message.channel)

async def roulette(message):
    if(message.author.voice.channel != None):
        if(random.randint(0,5) == 0):
            await message.channel.send(message.author.mention + "射到自己了")
            await message.author.edit(voice_channel=None)
        else:
            await message.channel.send(message.author.mention + "差點把自己轟出語音")
    else:
        await message.channel.send(message.author.mention + "馬的，進語音再用")

async def kick(message):
    if(message.author.voice != None):
        chlID = message.author.voice.channel.id
        chl= client.get_channel(chlID)
        member_ids = chl.voice_states.keys()
        memberlist = []
        for id in member_ids:
            memberlist.append(id)
        userId =random.choice(memberlist)
        user = await message.guild.query_members(user_ids=[userId]) # list of members with userid
        user = user[0] # there should be only one so get the first i
        if user:
            await user.edit(voice_channel=None)
            await message.channel.send(user.mention + "下去")
    else:
        await message.channel.send(message.author.mention + "馬的，進語音再用")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('舔'):
        await nolick(message)
    elif message.content.startswith('$hello'):
        await message.channel.send('Hello! ' + message.author.name)
    elif message.content == "The 踢":
        kick(message)
    elif message.content == "射":
        roulette(message)
    elif message.content.find("閃現") != -1:
        await flash(message)

        

        
intents = discord.Intents().all()
key = getKey(keyPath)
client.run(key)
