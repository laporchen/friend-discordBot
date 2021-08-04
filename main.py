from shlex import join
import discord
import json
import random
from discord import client
from discord import FFmpegPCMAudio
keyPath = "key.json"



def getKey(path):
    with open(path,'rb') as f:
        data = json.load(f)
        return data['Key']

def getAudio(path):
    return FFmpegPCMAudio("audio/" + path)

async def checkInVoice(message):
    voice = discord.utils.get(client.voice_clients, guild=message.author.guild)
    if voice == None:
        return None
    return voice
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

async def cry(message):
    cryImage = "cry.gif"
    await message.channel.send("哭啊！！！")
    await sendPic(cryImage,message.channel)

async def roulette(message):
    if(message.author.voice != None):
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

async def joinVoice(message):
    if message.author.voice:
        voice = discord.utils.get(client.voice_clients, guild=message.author.guild)
        if(voice == None):
            channel = message.author.voice.channel
            await channel.connect()
            await message.channel.send("來了啦幹")
        else:
            await message.channel.send(message.author.mention + "我已經在語音了 北七")
    else:
        await message.channel.send(message.author.mention + "馬的，進語音再用")

async def disconnect(message):
    for x in client.voice_clients:
        if(x.guild == message.author.guild):
            await message.channel.send("FK U ALL")
            await x.disconnect()

async def lickVoice(message):
    source = getAudio("lick.mp3")
    voice_client = await checkInVoice(message)
    print(type(source))
    if voice_client == None:
        if message.author.voice:
            voice_client = await message.author.voice.channel.connect()
        else:
            await message.channel.send(message.author.mention + "先進語音")
    if not voice_client.is_playing():
        await message.channel.send(message.author.mention + "統神直接爆氣給你看")
        player = voice_client.play(source)
    else:
        await message.channel.send(message.author.mention + "先讓我播完")

client = discord.Client()


async def queueYT(message):
    url = message.content.split()[1]
    

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
        await kick(message)
    elif message.content == "射":
        await roulette(message)
    elif message.content.find("閃現") != -1:
        await flash(message)
    elif message.content == "我叫你進":
        await joinVoice(message)
    elif message.content == "滾":
        voice = discord.utils.get(client.voice_clients, guild=message.author.guild)
        if voice == None:
            await message.channel.send(message.author.mention + "我沒在語音好ㄇ")
        else:
            await disconnect(message)
    elif message.content == "在語音舔":
        await lickVoice(message)
    elif message.content.find("哭啊") != -1:
        await cry(message)

intents = discord.Intents().all()
key = getKey(keyPath)
client.run(key)
