"""
Nextcord application that deploys a bot used to remind users about what they want.
They have to set a reminder with the slash command.
You should create a .env file holding the API_TOKEN,GUILD_ID and ROLE_ID.
"""
#!/usr/bin/env python3
# coding: utf-8
#
# reminder-bot
#
# ===
# Todo:
# Notes
#
# ===
# M.Alexandre   apr.28  creation
#

# #############################################################################
#
# Import zone
#
import logging
import os
from pathlib import Path
from datetime import datetime, timedelta
import asyncio
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands, tasks


from reminder import Reminder

# #############################################################################
#
# Config
#

#Logger
logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)

dotenv_path = Path("/app/config/credentials.env")
load_dotenv(dotenv_path=dotenv_path)
API_TOKEN = os.getenv('API_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
ROLE_ID = os.getenv('ROLE_ID')

bot = commands.Bot()

REMINDER_LIST:list[Reminder] = []

# #############################################################################
#
# Events
#

@tasks.loop(seconds=1.0)
async def check_times():
    """
    Task loop to check if the time is up
    for each reminder
    """
    logger.debug("Loop called")
    for reminder in REMINDER_LIST:
        logger.debug("reminder : %s",reminder)
        if reminder.time<=datetime.now():
            #Time to send
            embed = nextcord.Embed(
                    title="It's time to remind",
                    timestamp=reminder.time,
                    description=reminder.content,
                    color=nextcord.Colour.green()
                    )
            embed.set_author(name=reminder.author,icon_url=reminder.author_pic)
            content=f"<@&{ROLE_ID}>"
            message = await reminder.channel.send(content=content,embed=embed)
            await message.add_reaction("✅")
            REMINDER_LIST.remove(reminder)
            break

@bot.event
async def on_raw_reaction_add(reaction_add: nextcord.RawReactionActionEvent):
    """
    Function to delete a reminder when someone reacted to it
    """
    #IDs
    user_id=reaction_add.user_id
    message_id=reaction_add.message_id
    channel_id = reaction_add.channel_id
    #Fetch channel and message
    channel = await bot.fetch_channel(channel_id)
    message = await channel.fetch_message(message_id)

    #Check if the author of the message is the bot
    if message.author!=bot.user:
        return

    #Check that I have reacted to this message and if someone else have
    deletion = False
    for reaction in message.reactions:
        if reaction.emoji == '✅':
            users = await reaction.users().flatten()
            for user in users:
                if user == bot.user and len(users)>1:
                    deletion = True
                if user.id == user_id:
                    reaction_user = user
                    logger.debug("User : %s",reaction_user)

    if deletion:
        logger.debug("Deleting message")
        #Get description
        desc = None
        if message.embeds:
            timestamp = message.embeds[0].timestamp
            timestamp = datetime.timestamp(timestamp)
            timestamp = int(timestamp//1)
            desc = message.embeds[0].description+f' <t:{timestamp}:R>'
        embed = nextcord.Embed(title="Reminder marked as done",
                               description=desc,
                               color=nextcord.Colour.green())
        embed.set_author(name=reaction_user.display_name,icon_url=reaction_user.avatar)
        await channel.send(embed=embed)
        await message.delete()



@bot.event
async def on_ready():
    """
    Function called when the bot is ready
    """
    logger.info('We have logged in as %s',bot.user)
    logger.debug("API : %s, GUILD : %s",API_TOKEN,type(GUILD_ID))
    check_times.start()

@bot.slash_command(name='set_reminder',description="Set reminder", guild_ids=[GUILD_ID])
async def set_reminder(
    interaction: nextcord.Interaction,
    text: str = nextcord.SlashOption(description="Reminder content"),
    days: int = nextcord.SlashOption(description="Days to wait",required=False),
    hours: int = nextcord.SlashOption(description="Hours to wait",required=False),
    minutes: int = nextcord.SlashOption(description="Minutes to wait",required=False),
    seconds: int = nextcord.SlashOption(description="Seconds to wait",required=False),
    ):
    """
    Slash command that sets a reminder
    Params:
        interaction:nextcord.Interaction : Nextcored object identifying the interaction
        text:str : Content of the reminder
        days:int : Days to wait
        hours:int : Hours to wait
        minutes:int : Minutes to wait
        seconds:int : Seconds to wait

    """
    logger.debug("Set reminder called")
    #Get time of command
    now = datetime.now()

    #Compute reminder_time
    reminder_time = now
    if days:
        reminder_time += timedelta(days=days)
    if hours:
        reminder_time += timedelta(hours=hours)
    if minutes:
        reminder_time += timedelta(minutes=minutes)
    if seconds:
        reminder_time += timedelta(seconds=seconds)

    #Building response
    if reminder_time == now:
        embed = nextcord.Embed(
            title="Error",
            description="Specified time is same as now",
            color=nextcord.Colour.dark_red()
            )
    else:
        embed = nextcord.Embed(
                    title="Reminder set",
                    timestamp=reminder_time,
                    description=text,
                    color=nextcord.Colour.blue()
                    )
        reminder = Reminder(
                    content=text,
                    time=reminder_time,
                    channel=interaction.channel,
                    author=interaction.user.display_name,
                    author_pic=interaction.user.avatar
                    )
        REMINDER_LIST.append(reminder)
    message = await interaction.send(embed=embed)
    full_message = await message.fetch()
    #Wait 5s and delete
    await asyncio.sleep(5)
    await full_message.delete()



@bot.slash_command(name='gauntlet',description="Set a gautlet reminder (16h)", guild_ids=[GUILD_ID])
async def gauntlet(
    interaction: nextcord.Interaction,
    text: str = nextcord.SlashOption(description="Reminder content")
    ):
    """
    Slash command that sets a reminder
    Params:
        interaction:nextcord.Interaction : Nextcored object identifying the interaction
        text:str : Content of the reminder

    """
    logger.debug("Gautlet time")
    #Get time of command
    now = datetime.now()

    #Compute reminder_time
    reminder_time = now+timedelta(hours=16)

    #Building response
    embed = nextcord.Embed(
                title="Reminder set",
                timestamp=reminder_time,
                description=text,
                color=nextcord.Colour.blue()
                )
    reminder = Reminder(
                content=text,
                time=reminder_time,
                channel=interaction.channel,
                author=interaction.user.display_name,
                author_pic=interaction.user.avatar
                )
    REMINDER_LIST.append(reminder)
    message = await interaction.send(embed=embed)
    full_message = await message.fetch()
    #Wait 5s and delete
    await asyncio.sleep(5)
    await full_message.delete()


@bot.slash_command(name='show_reminders',description="Show active reminders", guild_ids=[GUILD_ID])
async def show_reminders(
    interaction: nextcord.Interaction,
    ):
    """
    Show active reminders
    Params:
        interaction:nextcord.Interaction : Nextcored object identifying the interaction
    """
    logger.debug("Show reminder called")

    #Build embed
    embed = nextcord.Embed(title="Reminders list")

    count = 0
    for reminder in REMINDER_LIST:
        timestamp = datetime.timestamp(reminder.time)
        timestamp = int(timestamp//1)
        if count==0:
            embed.add_field(name='ID',value=count,inline=True)
            embed.add_field(name='Time',value=f'<t:{timestamp}:t>',inline=True)
            embed.add_field(name='Content',value=reminder.content,inline=True)
        else:
            embed.add_field(name='',value=count,inline=True)
            embed.add_field(name='',value=f'<t:{timestamp}:t>',inline=True)
            embed.add_field(name='',value=reminder.content,inline=True)
        count += 1
    await interaction.send(embed=embed)

@bot.slash_command(name='delete_reminder',description="Show active reminders", guild_ids=[GUILD_ID])
async def delete_reminder(
    interaction: nextcord.Interaction,
    index:int = nextcord.SlashOption(description="ID of the reminder to delete")
    ):
    """
    Delete the reminder of ID id
    Params:
        interaction:nextcord.Interaction : Nextcored object identifying the interaction
        index:int : ID of the reminder to delete
    """
    logger.debug("Show reminder called")

    if index>=len(REMINDER_LIST):
        embed = nextcord.Embed(
            title="Error",
            description="Specified ID is not in the list",
            color=nextcord.Colour.dark_red()
            )
    else:
        embed = nextcord.Embed(title="Removed reminder",color=nextcord.Colour.green())
        embed.add_field(name='ID',value=index,inline=True)
        embed.add_field(name='Time',value=REMINDER_LIST[index].time,inline=True)
        embed.add_field(name='Content',value=REMINDER_LIST[index].content,inline=True)
        REMINDER_LIST.pop(index)
    await interaction.send(embed=embed)


if __name__ == "__main__":
    logging.info('Starting application')
    bot.run(API_TOKEN)
