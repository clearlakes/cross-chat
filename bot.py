import discord
from discord.ext import commands
import json
import datetime as dt

TOKEN = 'YOUR BOTS TOKEN HERE'
client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.event
async def on_ready():
    # read each json file for commands
    data = read_json("blacklist")
    data_mod = read_json("moderators")
    data_channel = read_json("channels")
    client.blacklisted_users = data["blacklistedUsers"]
    client.moderators = data_mod["modUsers"]
    client.channel_list = data_channel["channelList"]
    print("ready")

@client.event
async def on_message(message):
    # ignore messages that are commands
    await client.process_commands(message)
    if message.content.startswith("."):
        return
    else:
        # ignore the bot's own messages
        if message.author.id == client.user.id:
            return
        else:
            # find out if the message was sent from one of the channels in channels.json
            find_channel_id = f'{message.channel.id}'
            with open('channels.json', 'r') as read_obj:
                for line in read_obj:
                    if find_channel_id in line:
                        # changes the color of a moderator's post to distinguish it
                        # also adds "[mod]" to the moderator's name
                        # you can add checks to see if a certain id posts a message for custom colors
                        if message.author.id in client.moderators:
                            chat_color = discord.Color.dark_blue()
                            chat_name = f"[mod] {message.author.name}"
                        else:
                            chat_color = discord.Color.blue()
                            chat_name = message.author.name

                        #see if user is blacklisted
                        if message.author.id in client.blacklisted_users:
                            await message.channel.send("You are blacklisted")
                        else:
                            # embed creation, where the description of the embed is replaced with the user's message
                            time = dt.datetime.utcnow()
                            embed = discord.Embed(
                                title = "",
                                description = message.content.format(message),
                                colour = chat_color,
                                timestamp = time
                            )
                            server_name = f"{message.guild}"
                            embed.set_author(name=chat_name, icon_url=message.author.avatar_url)
                            embed.set_footer(text=server_name, icon_url=message.guild.icon_url)
                            embed.timestamp = message.created_at
                            if message.attachments:
                                # support for images
                                embed.set_image(url=message.attachments[0].url)
                            else:
                                await message.delete()

                            # send the embed we just created to every channel id in channels.json
                            data = read_json("channels")
                            for item in data['channelList']:
                                channel = client.get_channel(item)
                                await channel.send(embed = embed)
                            if message.attachments:
                                await message.delete()

@client.command()
async def setchannel(ctx):
    # adds the id of the channel the command was sent in into channels.json
    # so, in "on_message", it sends messages to this channel and others
    await ctx.send("Setting up channel..")
    channel_id = ctx.message.channel.id
    client.channel_list.append(channel_id)
    data = read_json("channels")
    data["channelList"].append(channel_id)
    write_json(data, "channels")
    await ctx.send("Channel has been set up! Type in this channel to cross-chat.")

# commands.is_owner() only allows the bot owner to send the command
@client.command()
@commands.is_owner()
async def mod(ctx, user: discord.Member):
    # add the user id of the to-be moderator to the moderators.json file
    client.moderators.append(user.id)
    data = read_json("moderators")
    data["modUsers"].append(user.id)
    write_json(data, "moderators")
    embed = discord.Embed(
        title = "New Moderator",
        description = f"{user.name} is now a mod",
        color = discord.Color.blurple()
    )
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed = embed)

@client.command()
@commands.is_owner()
async def unmod(ctx, user:discord.Member):
    # remove the mentioned user's id from moderators.json
    client.moderators.remove(user.id)
    data = read_json("moderators")
    data["modUsers"].remove(user.id)
    write_json(data, "moderators")
    embed = discord.Embed(
        title = "Moderator Removed",
        description = f"{user.name} has been removed as a mod",
        color = discord.Color.red()
    )
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed = embed)

@client.command()
async def blacklist(ctx, user:discord.Member):
    # check if the user sending the command is a mod (using the moderators.json file)
    if ctx.message.author.id in client.moderators:
        # adds the mentioned user's id to blacklist.json
        client.blacklisted_users.append(user.id)
        data = read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        write_json(data, "blacklist")
        embed = discord.Embed(
            title = "Member Blacklisted",
            description = f"{user.name} has been blacklisted",
            color = discord.Color.red()
        )
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed = embed)
    else:
        await ctx.send("You are not allowed to do that")

@client.command()
async def unblacklist(ctx, user:discord.Member):
    # check if the user sending the command is a mod (using the moderators.json file)
    if ctx.message.author.id in client.moderators:
        # removes the mentioned user's id frm blacklist.json
        client.blacklisted_users.remove(user.id)
        data = read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        write_json(data, "blacklist")
        embed = discord.Embed(
            title = "Member Un-blacklisted",
            description = f"{user.name} has been un-blacklisted",
            color = discord.Color.green()
        )
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed = embed)
    else:
        await ctx.send("you are not swag enough to do that")
        return

# "def read_json" and "def write_json" are used to read and write data to the json files

def read_json(filename):
    with open(f"{filename}.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file, indent=4)

client.run(TOKEN)
