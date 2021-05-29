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


    @client.command()
    async def mute(ctx):
        message_content = ctx.message.content.split(" ")
        userIDString = message_content[1]
        user_id = int(message_content[1])
        timeoutRole = discord.utils.get(ctx.guild.roles, name = "Timeout")

        for member in ctx.guild.members:
            print(member.name)

        try:
            user_to_mute = discord.utils.get(ctx.guild.members, id=user_id)
            await user_to_mute.add_roles(timeoutRole)
            await ctx.send('success')
        except:
            await ctx.send('yikes')


    @client.command()
    async def kick(ctx):
        message_content = ctx.message.content.split(" ")
        #userIDString = message_content[1]
        user_id = int(message_content[1])
        #timeoutRole = discord.utils.get(ctx.guild.roles, name="Timeout")

        for member in ctx.guild.members:
            print(member.name)

        try:
            user_to_mute = discord.utils.get(ctx.guild.members, id=user_id)
            await ctx.guild.kick(user_to_mute)
            await ctx.send('success')
        except:
            await ctx.send('yikes')


    @client.command()
    async def ban(ctx):
        message_content = ctx.message.content.split(" ")
        # userIDString = message_content[1]
        user_id = int(message_content[1])
        # timeoutRole = discord.utils.get(ctx.guild.roles, name="Timeout")

        for member in ctx.guild.members:
            print(member.name)

        try:
            user_to_mute = discord.utils.get(ctx.guild.members, id=user_id)
            await ctx.guild.ban(user_to_mute)
            await ctx.send('success')
        except:
            await ctx.send('yikes')


    @client.command()
    async def unmute(ctx):
        message_content = ctx.message.content.split(" ")
        # userIDString = message_content[1]
        user_id = int(message_content[1])
        timeoutRole = discord.utils.get(ctx.guild.roles, name="Timeout")

        for member in ctx.guild.members:
            print(member.name)

        try:
            user_to_mute = discord.utils.get(ctx.guild.members, id=user_id)
            await user_to_mute.remove_roles(timeoutRole)
            await ctx.send('success')
        except:
            await ctx.send('yikes')

    # async def rolekick(ctx):
    #     message_content = ctx.message.content.split(" ")
    #     # userIDString = message_content[1]
    #     membersList = ctx.guild.members
    #     #timeoutRole = discord.utils.get(ctx.guild.roles, name="Timeout")
    #
    #     for member in ctx.guild.members:
    #         print(member.name)
    #
    #     try:
    #         role_to_kick = discord.utils.get(ctx.guild.roles)
    #         for member in membersList:
    #             currentMemberRoleList = member.roles
    #                 for role in currentMemberRoleList:
    #                     if role == role_to_kick:
    #                         await ctx.guild.kick(member)
    #     except:
    #         await ctx.send('yikes')



    #     if message.content.startswith("$rolekick"):
    #         guild = message.guild
    #         message_content = message.content.split()
    #         membersList = guild.members
    #         print(guild.members)
    #         if len(message_content) == 1:
    #             await message.channel.send("Please specify the role id of the roles you would like to kick")
    #         else:
    #             kickedRoleID = int(message_content[1])
    #             kickedRole = guild.get_role(kickedRoleID)
    #             for member in membersList:
    #                 currentMemberRoleList = member.roles
    #                 for role in currentMemberRoleList:
    #                     if role == kickedRole:
    #                         await guild.kick(member)



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