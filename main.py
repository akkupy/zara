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

print(r'''
     __       _       _           
    /  \     | |     | | 
   /    \    | | /\  | | /\   _   _
  /  /\  \   | |/ /  | |/ /  | | | |  
 /  ____  \  | |\ \  | |\ \  | |_| |
/__/    \__\ |_| \_\ |_| \_\  \___/  ''')
print("\n*************************************")
print("\n* Copyright of Akash, 2022          *")
print("\n* https://akkupy.me                 *")
print("\n* https://t.me/akkupy               *")
print("\n*************************************")

bot = commands.Bot(command_prefix='.',intents=discord.Intents.all())


def convertTime(input):
    h, m = int(input[0:2]), int(input[2:4])

    postfix = 'am'

    if h > 12:
        postfix = 'pm'
        h -= 12

    return '{}:{:02d}{}'.format(h or 12, m, postfix)

def convertDate(input):
    y,m,d = int(input[0:4]),int(input[4:6]),int(input[6:8])

    return '{}/{}/{}'.format(d,m,y)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is Online")


@bot.command()
async def schedule(ctx,fTime,fDate,tTime,tDate):
    username = str(ctx.author).split("#")[0]
    channel = str(ctx.channel.name)

    if channel == "scheduler":
        fromFormatedTime = convertTime(fTime)
        toFormatedTime = convertTime(tTime)
        fromFormatedDate = convertDate(fDate)
        toFormatedDate = convertDate(tDate)
        emb = discord.Embed(title="Poll for Meeting",description=f'''
        The Meeting is about to be  scheduled.
        Start Date : {fromFormatedDate}
        Start Time : {fromFormatedTime}
        End Date : {toFormatedDate}
        End Time : {toFormatedTime}
        Description: AR workshop
        React if you are okay or not (Available for 5min)!
        ''')
        poll = bot.get_channel(int(pollid))
        msg = await poll.send(embed=emb)
        await msg.add_reaction('👍') 
        await msg.add_reaction('👎')

        await asyncio.sleep(10)
        userz = bot.get_user(int(botid))
        await msg.remove_reaction('👍',userz)
        await msg.remove_reaction('👎',userz)
        vote_msg = await msg.channel.fetch_message(msg.id)
        positive = 0
        negative = 0
        users = set()
        for reaction in vote_msg.reactions:
            if reaction.emoji == '👍':
                positive = reaction.count
                async for user in reaction.users():
                    users.add(user)
            if reaction.emoji == '👎':
                negative = reaction.count
        


        if positive > negative:

            announcement = bot.get_channel(int(annid))
  
            response = discord.Embed(title="A meeting is Scheduled.",description=f'''
            Start Date : {fromFormatedDate}
            Start Time : {fromFormatedTime}
            End Date : {toFormatedDate}
            End Time : {toFormatedTime}
            Description: AR workshop
            Scheduled by : {username}
            ''')

            await announcement.send(embed=response)

            viz = list(users)
            title = "Meeting"
            button = Button(label="Add to Calender",style=discord.ButtonStyle.green,url=f"https://calendar.google.com/calendar/u/0/r/eventedit?text={title}&dates={fDate}T{fTime}/{tDate}T{tTime}&ctz=Asia/Kolkata&details=Njoy+Lyf")
            view = View()
            view.add_item(button)

            for i in range(0,len(viz)):
                await viz[i].send(embed=response,view=view)


bot.run(TOKEN)
