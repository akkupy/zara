from discord.ext import commands
import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ui import Button,View

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
pollid = os.getenv('POLL_CHANNEL')
annid = os.getenv('ANNOUNCEMENT_CHANNEL')
botid = os.getenv('BOT_ID')

bot = commands.Bot(command_prefix='.',intents=discord.Intents.all())


def convertTime(input):
    h, m = int(input[0:2]), int(input[2:4])

    postfix = 'am'

    if h > 12:
        postfix = 'pm'
        h -= 12

    return '{}:{:02d}{}'.format(h or 12, m, postfix)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is Online")


@bot.command()
async def schedule(ctx,message,fdate,ttime,tdate):
    username = str(ctx.author).split("#")[0]
    channel = str(ctx.channel.name)

    if channel == "scheduler":
        tim = convertTime(message)
        timf = convertTime(ttime)
        emb = discord.Embed(title="Poll for Meeting",description=f"The meeting is about to be scheduled from {tim} to {timf}.Is it okay?(React in 5min)")
        poll = bot.get_channel(int(pollid))
        msg = await poll.send(embed=emb)
        await msg.add_reaction('👍') 
        await msg.add_reaction('👎')

        await asyncio.sleep(10)
        userz = bot.get_user(int(botid))
        await msg.remove_reaction('👍',userz)
        vote_msg = await msg.channel.fetch_message(msg.id)
        positive = 0
        negative = 0
        users = set()
        for reaction in vote_msg.reactions:
            if reaction.emoji == '👍':
                positive = reaction.count - 1 
                async for user in reaction.users():
                    users.add(user)
            if reaction.emoji == '👎':
                negative = reaction.count - 1
        


        if positive > negative:

            announcement = bot.get_channel(int(annid))
  
            response = "Scheduled a meeting  from " + tim +" to " + timf + " by " + username
            await announcement.send(response)

            viz = list(users)
            title = "Meeting"
            datef = fdate
            timef = message
            date = tdate
            time = ttime
            button = Button(label="Add to Calender",style=discord.ButtonStyle.green,url=f"https://www.google.com/calendar/render?action=TEMPLATE&text={title}&dates{datef}T{timef}Z/{date}T{time}Z&details=For+details,+link+here:+http://www.akkupy.me&sf=true&output=xml".format(title,datef,timef,date,time))
            view = View()
            view.add_item(button)

            for i in range(0,len(viz)):
                await viz[i].send(response,view=view)


bot.run(TOKEN)
