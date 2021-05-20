import discord
import requests
from bs4 import BeautifulSoup
import os
import datetime
from discord.ext import commands

with open('token.txt', 'r') as file: #gets token from file that is not on github, but is on host server
    token = file.readline()


if __name__ == '__main__':
    print("hello world")

    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="$", intents = intents)

    NUM_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    @client.event
    async def on_connect():
        print("We have connected as {0.user}".format(client))

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))


    @client.event
    async def on_reaction_add(reaction, user):
        if user == client.user or reaction.message.embeds[0].title != "Available Roles:":
            # not a relevant reaction
            return

        # regenerate list of roles
        available_roles = reaction.message.guild.roles
        index = NUM_EMOJIS.index(reaction.emoji)
        try:
            await user.add_roles(available_roles[index])
            await reaction.message.channel.send("Hey, check out the roles on this guy @" + str(user.display_name))
        except:
            await reaction.message.channel.send("Sorry, " + str(user.display_name) + ", I can't let you have the role of "
                                                + str(available_roles[index].name))


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

        if message.content.startswith("$test"):
            guild = message.guild
            await message.channel.send(guild.name)

        if message.content.startswith("$mute"):
            guild = message.guild
            message_content = message.content.split()
            if len(message_content) == 1:
                await message.channel.send("Please specify the user id of the user you would like to mute")
            else:
                user_id = message_content[1]
                timeoutRole = guild.get_role(839236832398671913)
                user = await message.guild.fetch_member(user_id)
                await user.add_roles(timeoutRole)

        if message.content.startswith("$unmute"):
            guild = message.guild
            message_content = message.content.split()
            if len(message_content) == 1:
                await message.channel.send("Please specify the user id of the user you would like to unmute")
            else:
                user_id = message_content[1]
                timeoutRole = guild.get_role(839236832398671913)
                user = await message.guild.fetch_member(user_id)
                await user.remove_roles(timeoutRole)

        if message.content.startswith("$kick"):
            guild = message.guild
            message_content = message.content.split()
            if len(message_content) == 1:
                await message.channel.send("Please specify the user id of the user you would like to kick")
            else:
                user_id = message_content[1]
                user = await message.guild.fetch_member(user_id)
                await guild.kick(user)

        if message.content.startswith("$rolekick"):
            guild = message.guild
            message_content = message.content.split()
            membersList = guild.members
            print(guild.members)
            if len(message_content) == 1:
                await message.channel.send("Please specify the role id of the roles you would like to kick")
            else:
                kickedRoleID = int(message_content[1])
                kickedRole = guild.get_role(kickedRoleID)
                for member in membersList:
                    currentMemberRoleList = member.roles
                    for role in currentMemberRoleList:
                        if role == kickedRole:
                            await guild.kick(member)

        if message.content.startswith("$ban"):
            guild = message.guild
            message_content = message.content.split()
            if len(message_content) == 1:
                await message.channel.send("Please specify the role id of the roles you would like to ban")
            else:
                user_id = message_content[1]
                user = await message.guild.fetch_member(user_id)
                await guild.ban(user)


    @client.command()
    async def poll(ctx):
        if ctx.message.content == "$poll help":
            await ctx.send('To create a poll, use this format: $poll "Question" "Option 1" "Option 2" . ' +
                           'Then let users vote by reacting!')
            return

        poll_content = [line for line in [line.strip() for line in ctx.message.content.split("\"")] if line]
        try:
            question = poll_content[1]
            options = poll_content[2:]
        except:
            await ctx.send('To create a poll, use this format: "Question" "Option 1" "Option 2" ....')
            return

        if len(options) > 10:
            await ctx.send("Sheeeesh, that's too many options! Keep it to 10 or less.")
            return

        option_text = ''
        for i in range(0, len(options)):
            option_text += NUM_EMOJIS[i] + '  ' + options[i] + '\n\n'

        embed = discord.Embed(title="Poll: " + question,
                              description=option_text,
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed)

        for i in range(0, len(options)):
            await msg.add_reaction(NUM_EMOJIS[i])


    @client.command()
    async def roles(ctx):
        if ctx.message.content == '$roles help':
            await ctx.send('Use $roles to list all roles in the server and allow users to add a role by reacting!')
            return

        available_roles = ctx.guild.roles
        if len(available_roles) > 10:
            await ctx.send("Sheeeesh, there are too many roles in this server! Keep it to 10 or less.")
            return

        text = ''
        for i in range(0, len(available_roles)):
            text += NUM_EMOJIS[i] + ' ' + str(available_roles[i].name) + '\n \n'

        embed = discord.Embed(title="Available Roles:",
                              description=text,
                              color=discord.Color.blue())

        msg = await ctx.send(embed=embed)

        for i in range(0, len(available_roles)):
            await msg.add_reaction(NUM_EMOJIS[i])


    client.run(token)