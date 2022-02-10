from http import server
import os
from re import S
import discord
import json
import random
from discord import client
from discord import FFmpegPCMAudio
from discord.ext import commands
import requests
import libWordle as wd
keyPath = "./key.json"

# wordle variables
wordleGameStarted = {}
wordList = []
puzzle = {}
guessCount = {}
guessResult = {}
# end wordle

client = commands.Bot(command_prefix='$')


def getKey(path):
    with open(path, 'rb') as f:
        data = json.load(f)
        return data['Key']


def getID(path, name):
    with open(path, 'rb') as f:
        data = json.load(f)
        return data[name]


def getAudio(path):
    return FFmpegPCMAudio("../audio/" + path)


async def checkInVoice(message):
    voice = discord.utils.get(client.voice_clients, guild=message.author.guild)
    if voice == None:
        return None
    return voice


async def sendPic(file, channel):
    with open('../img/' + file, 'rb') as f:
        picture = discord.File(f)

        await channel.send(file=picture)


async def nolick(message):
    lick = "lick.jpg"
    await message.channel.send('又舔，又舔，又…又舔嘴唇！')
    await sendPic(lick, message.channel)


async def flash(message):
    flash = "flash.gif"
    await message.channel.send('這什麼到底什麼閃現！')
    await sendPic(flash, message.channel)


async def cry(message):
    cryImage = "cry.gif"
    await message.channel.send("哭啊！！！")
    await sendPic(cryImage, message.channel)


async def roulette(message):
    if(message.author.voice != None):
        if(random.randint(0, 5) == 0):
            await message.channel.send(message.author.mention + "射到自己了")
            await message.author.edit(voice_channel=None)
        else:
            await message.channel.send(message.author.mention + "差點把自己轟出語音")
    else:
        await message.channel.send(message.author.mention + "馬的，進語音再用")


async def kick(message):
    if(message.author.voice != None):
        chlID = message.author.voice.channel.id
        chl = client.get_channel(chlID)
        member_ids = chl.voice_states.keys()
        memberlist = []
        for id in member_ids:
            memberlist.append(id)
        userId = random.choice(memberlist)
        # list of members with userid
        user = await message.guild.query_members(user_ids=[userId])
        user = user[0]  # there should be only one so get the first i
        if user:
            await user.edit(voice_channel=None)
            await message.channel.send(user.mention + "下去")
    else:
        await message.channel.send(message.author.mention + "馬的，進語音再用")


async def joinVoice(message):
    if message.author.voice:
        voice = discord.utils.get(
            client.voice_clients, guild=message.author.guild)
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


async def getVC(message):
    if message.author.voice:
        return await message.author.voice.channel.connect()
    else:
        await message.channel.send(message.author.mention + "先進語音")


async def cheeseVoice(message):
    if(await checkVoice(message)):
        return
    source = getAudio("cheese.mp3")
    vc = await checkInVoice(message)
    if(vc == None):
        vc = await getVC(message)
    if not vc.is_playing():
        await message.channel.send(message.author.mention + "我去你媽")
        vc.play(source)
        await sendPic("cheese.jpg", message.channel)
        await message.channel.send("奶酪！！！！")


async def lickVoice(message):
    if(await checkVoice(message)):
        return
    source = getAudio("lick.mp3")
    voice_client = await checkInVoice(message)
    if voice_client == None:
        voice_client = await getVC(message)
    if not voice_client.is_playing():
        await message.channel.send(message.author.mention + "統神直接爆氣給你看")
        voice_client.play(source)


async def brian(message):
    userId = getID(keyPath, "brianID")
    user = await message.guild.query_members(user_ids=[userId])
    msg = ""
    for i in range(5):
        msg = msg + user[0].mention + "打肉叫你上線\n"
    await message.channel.send(msg)


async def dazzle(message):
    userId = getID(keyPath, "dazzle")
    user = await message.guild.query_members(user_ids=[userId])
    msg = ""
    for i in range(5):
        msg = msg + user[0].mention + "布萊恩好像叫你上線\n"
    await message.channel.send(msg)


async def rat(message):
    source = getAudio("rat.mp3")
    await sendPic("rat.png", message.channel)
    await message.channel.send("勞贖")
    if message.author.voice != None:
        voice_client = await checkInVoice(message)
        if voice_client == None:
            voice_client = await getVC(message)
        if not voice_client.is_playing():
            voice_client.play(source)


async def cat(message):
    url = "https://api.giphy.com/v1/gifs/random?api_key=" + \
        getID(keyPath, "giphy") + "&rating=g&tag=cat"
    respone = requests.get(url)
    js = respone.json()
    # print(js)
    gif = js["data"]["url"]

    await message.channel.send("貓")
    await message.channel.send(gif)


async def duck(message):
    url = "https://api.giphy.com/v1/gifs/random?api_key=" + \
        getID(keyPath, "giphy") + "&rating=g&tag=duck"
    respone = requests.get(url)
    js = respone.json()
    # print(js)
    gif = js["data"]["url"]

    await message.channel.send("鴨鴨")
    await message.channel.send(gif)


async def huh(message):
    url = "https://api.giphy.com/v1/gifs/random?api_key=" + \
        getID(keyPath, "giphy") + "&rating=g"
    respone = requests.get(url)
    js = respone.json()
    gif = js["data"]["url"]

    await message.channel.send("蛤")
    await message.channel.send(gif)


async def checkVoice(message):
    if message.author.voice == None:
        await message.channel.send("進語音啊")
        return True
    return False


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
        voice = discord.utils.get(
            client.voice_clients, guild=message.author.guild)
        if voice == None:
            await message.channel.send(message.author.mention + "我沒在語音好ㄇ")
        else:
            await disconnect(message)
    elif message.content == "在語音舔":
        await lickVoice(message)
    elif message.content.find("哭啊") != -1:
        await cry(message)
    elif message.content == "你媽的奶酪":
        await cheeseVoice(message)
    elif message.content == "打肉布萊恩":
        await brian(message)
    elif message.content == "打肉打肉":
        await dazzle(message)
    elif message.content.find("卯咪") != -1:
        await cat(message)
    elif message.content.find("蛤") != -1:
        await huh(message)
    elif message.content.find("老鼠") != -1:
        await rat(message)
    await client.process_commands(message)


@client.command(pass_context=True)
async def roll(ctx, arg='6'):
    top = 6
    if arg and arg.isnumeric():
        top = int(arg)
    if not arg.isnumeric():
        await ctx.send(ctx.author.mention + "同學，這不是數字")
        return
    if top == 0:
        await ctx.send(ctx.author.mention + " 0點你是要骰啥")
        return
    await ctx.send(ctx.author.mention + " 骰出了 " + str(random.randrange(1, top)))


@client.command(pass_context=True, aliases=['wd'])
async def wordle(ctx, arg="2"):
    serverId = str(ctx.guild.id)
    global wordleGameStarted, puzzle, wordList, guessCount, guessResult
    if(serverId not in wordleGameStarted):
        wordleGameStarted[serverId] = False
        puzzle[serverId] = ""
        guessCount[serverId] = 0
        guessResult[serverId] = []
    if(arg == "help"):
        await ctx.send(ctx.author.mention + " 可以用的指令有：\n" + "$wordle new 開始遊戲\n" + "$wd word 猜字\n")
    if(arg == "new" and wordleGameStarted[serverId] == False):
        wordleGameStarted[serverId] = True
        wordList = wd.init()
        puzzle[serverId] = wd.gameInit(wordList['words'])
        guessCount[serverId] = 0
        await ctx.send("遊戲開始，輸入$wordle <word> 來進行猜測")
    elif(arg == "new" and wordleGameStarted[serverId] == True):
        await ctx.send("遊戲已經開始了，使用$wordle <word> 來猜")
    elif (wordleGameStarted[serverId]):
        wordleGameStarted[serverId] += 1
        res = wd.process(
            arg, puzzle[serverId], wordList['words'], wordList['allowGuesses'])
        guessResult[serverId].append(res[1])
        if(res[0] == True):
            await ctx.send(res[1])
            await ctx.send("遊戲結束，猜測次數: " + str(guessCount[serverId]))
            guessStr = ""
            for i in guessResult[serverId]:
                guessStr += i + "\n"
            await ctx.send(guessStr)
            wordleGameStarted[serverId] = False
            return
        await ctx.send(res[1])
        if(guessCount[serverId] > 5):
            await ctx.send("遊戲結束，輸入$wordle new 重新開始\n" + "答案是：" + puzzle[serverId])
            wordleGameStarted[serverId] = False
            return

intents = discord.Intents().all()
key = getKey(keyPath)
client.run(key)
