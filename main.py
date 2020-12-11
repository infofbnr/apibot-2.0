import discord
import json
import random
import os
import subprocess as sp
import typing
import aiohttp
from datetime import datetime
from PIL import Image
from PIL import ImageFont
import psutil
from PIL import ImageDraw
from io import BytesIO
from aiohttp import request
import asyncio
from discord.ext import commands
import os
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
# also
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"


async def prefix(bot, message):
    if message.author.id == 639164486846251011:
        return ["a-", ""]
    else:
        return "a-"


intents = discord.Intents.all()
token = open("token.txt", "r").readline()
client = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True,
                      status=discord.Status.online, activity=discord.Game(name='a-help'))
client.launch_time = datetime.utcnow()


@client.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(title="I have been up for:",
                          description=f"Days: {days}\nHours: {hours}\nMinutes: {minutes}\nSeconds: {seconds}", color=random.randint(0, 0xffffff))
    await ctx.send(embed=embed)


@client.command()
async def wanted(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    wanted = Image.open("wanted.jpg")

    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((339, 277))
    wanted.paste(pfp, (67, 230))

    wanted.save("wanted.jpg")
    await ctx.send(file=discord.File("wanted.jpg"))


@client.command()
async def joke(ctx):
    joke_url = f"https://some-random-api.ml/joke"

    async with request("GET", joke_url, headers={}) as response:
        if response.status == 200:
            data = await response.json()
            await ctx.send(data['joke'])


@client.command()
async def triggered(ctx, member: discord.Member = None):
    async with ctx.typing():
        if member == None:
            member = ctx.author
        session = aiohttp.ClientSession()
        async with session.get(f"https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format='jpg')}") as r:
            if r.status != 200:
                await ctx.send("**Unable to load image**")
                await session.close()
                return
            else:
                data = BytesIO(await r.read())
                await ctx.send(file=discord.File(data, 'wasted.gif'))
                await session.close()


@client.command(name="fact")
async def animal_fact(ctx, animal: str):

    if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala", "kangaroo", "racoon", "elephant", "giraffe", "whale"):
        fact_url = f"https://some-random-api.ml/facts/{animal}"
        image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

        async with request("GET", image_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                image_link = data["link"]
            else:
                image_link = None

        async with request("GET", fact_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                embed = discord.Embed(title=f"{animal.title()} fact:",
                                      description=data["fact"],
                                      colour=random.randint(0, 0xffffff))
                if image_link is not None:
                    embed.set_image(url=image_link)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"API returned a {response.status} status.")
    else:
        await ctx.send("No facts are available for that animal!, animals are: dog, cat, panda, fox, bird, koala, kangaroo, racoon, elephant, giraffe and whale")


@client.command()
async def pikagif(ctx):
    pika_img = f"https://some-random-api.ml/img/pikachu"
    async with request("GET", pika_img, headers={}) as response:
        if response.status == 200:
            data = await response.json()
            pika_link = data['link']
            await ctx.send(pika_link)


@client.command()
async def fontone(ctx, color: str, size: str,  text: str):
    session = aiohttp.ClientSession()
    async with session.get(f"https://api.nitestats.com/v1/fnfontgen?color={color}&size={size}&text={text}") as r:
        if r.status != 200:
            await ctx.send(f"**Unable to load image (Status = {r.status})**")
            await session.close()
            return
        else:
            data = BytesIO(await r.read())
            await ctx.send(file=discord.File(data, 'fortnite.png'))
            await session.close()


@client.command()
async def pokedescription(ctx, pokemon: str):
    pokedex_url = f"https://some-random-api.ml/pokedex?pokemon={pokemon}"
    async with request("GET", pokedex_url, headers={}) as r:
        if r.status != 200:
            await ctx.send("Unable to do the thing this command does idk")
            return
        else:
            data = await r.json()
            await ctx.send(data["description"])


@client.command()
async def eject(ctx, name: str, color: str,  imposter: bool):
    session = aiohttp.ClientSession()
    async with session.get(f"https://vacefron.nl/api/ejected?name={name}&impostor={imposter}&crewmate={color}") as r:
        if r.status != 200:
            err = (await r.json())['message']
            await ctx.send(f"**Unable to load image (Status = {r.status}, Error = {err})**")
            await session.close()
            return
        else:
            data = BytesIO(await r.read())
            await ctx.send(file=discord.File(data, 'ejected.png'))
            await session.close()


@client.command()
async def emergencymeeting(ctx, *, text: str):
    session = aiohttp.ClientSession()
    async with session.get(f"https://vacefron.nl/api/emergencymeeting?text={text}") as r:
        if r.status != 200:
            err = (await r.json())['message']
            await ctx.send(f"**Unable to load image (Status = {r.status}, Error = {err})**")
            await session.close()
            return
        else:
            data = BytesIO(await r.read())
            await ctx.send(file=discord.File(data, 'em.png'))
            await session.close()


@client.command()
async def water(ctx, text: str):
    session = aiohttp.ClientSession()
    async with session.get(f"https://vacefron.nl/api/water?text={text}") as r:
        if r.status != 200:
            err = (await r.json())['message']
            await ctx.send(f"**Unable to load image (Status = {r.status}, Error = {err})**")
            await session.close()
            return
        else:
            data = BytesIO(await r.read())
            await ctx.send(file=discord.File(data, 'water.png'))
            await session.close()


@client.command(name="fakeyoutubecomment", aliases=['fakeytcomment', 'fym', 'fakeytcmnt', 'fakeytcom'])
async def fytcomment(ctx, member: typing.Optional[discord.Member], comment: str):
    if member == None:
        member = ctx.author
    session = aiohttp.ClientSession()
    async with session.get(f"https://some-random-api.ml/canvas/youtube-comment?avatar={member.avatar_url_as(format='jpg')}&comment={comment}&username={member.name}") as r:
        if r.status != 200:
            err = (await r.json())['message']
            await ctx.send(f"**Unable to load image (Status = {r.status}, Error = {err})**")
            await session.close()
            return
        else:
            data = BytesIO(await r.read())
            await ctx.send(file=discord.File(data, 'youtube.png'))
            await session.close()


@client.command()
async def pokedex(ctx, pokemon: str):
    pokedex_url = f"https://some-random-api.ml/pokedex?pokemon={pokemon}"
    async with request("GET", pokedex_url, headers={}) as r:
        if r.status != 200:
            await ctx.send("Unable to do the thing this command does idk")
            return
        else:
            data = await r.json()
            await ctx.send(f"Type: {data['type']}  \nSpecies: {data['species']}")


@client.command()
async def rgb(ctx, hex: str):
    session = aiohttp.ClientSession()
    async with session.get(f"https://some-random-api.ml/canvas/rgb?hex={hex}") as r:
        if r.status != 200:
            err = (await r.json())['message']
            await ctx.send(f"**Unable to load image (Status = {r.status}, Error = {err})**")
            await session.close()
            return
        else:
            data = await r.json()
            await ctx.send("R: " + data['r'])
            await session.close()


@client.command()
async def randomusername(ctx):
    session = aiohttp.ClientSession()

    async with session.get(f"https://api.namefake.com/") as r:
        if r.status != 200:
            err = (await r.json())['message']
            await ctx.send(f"**Unable to generate username (Status = {r.status}, Error = {err})**")
            await session.close()
            return
        else:
            data = await r.json()
            await ctx.send(f"Your random username: {data['username']}")
            await session.close()


@client.command()
@commands.is_owner()
async def testwebhooks(ctx, chnl: discord.TextChannel, *, text):
    avatar = await ctx.author.avatar_url_as(format="jpg").read()
    await ctx.message.delete()

    f = await chnl.create_webhook(name=ctx.author.name, avatar=avatar)
    await f.send(content=f"{text}")


@client.command(name="restart", aliases=["r"], help="Restarts the bot")
@commands.is_owner()
async def restart(ctx):
    embed = discord.Embed(
        description=f"{ctx.author.mention} restarting...",
        color=random.randint(0, 0xffffff),
        timestamp=datetime.utcnow()
    )
    embed.set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar_url
    )
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")
    await client.close()


@client.command()
async def CPUxMEM(ctx):
    cpu_percentage = psutil.cpu_percent()
    mem_used = (
        psutil.virtual_memory().total - psutil.virtual_memory().available
    ) / 1000000
    total_mem = psutil.virtual_memory().total / 1000000
    await ctx.send(f"My CPU %: {cpu_percentage}\nMemory used/left: {mem_used}/{total_mem}")


@client.command()
async def invite(ctx):
    await ctx.send(f"My invite: <https://discord.com/oauth2/authorize?client_id={client.user.id}&scope=bot&permissions={member.guild_permissions.value}>\n Note: the permissions are the permissions the bot has in this **__guild__**. Go use the discord permission calculator if you want other permissions.")


extensions = ['cogs.Developer', 'cogs.ServerCommands', 'cogs.HelpCommand', 'cogs.CommandsHelp',
              'cogs.CommandErrors', 'cogs.CommandEvents', 'cogs.CogCommands', 'cogs.FunCommands', 'cogs.MiscCommands']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)


client.load_extension('jishaku')
client.run(token, reconnect=True)
