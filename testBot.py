import discord
import requests
from bs4 import BeautifulSoup
import os
import datetime

with open('token.txt', 'r') as file: #gets token from file that is not on github, but is on host server
    token = file.readline()


if __name__ == '__main__':
    print("hello world")

    client = discord.Client()

    @client.event
    async def on_connect():
        print("We have connected as {0.user}".format(client))


    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))


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
            message_content = message.content.split()
            userName = message_content[1]
            await message.channel.send("Mutes " + userName)

        if message.content.startswith("$unmute"):
            message_content = message.content.split()
            userName = message_content[1]
            await message.channel.send("Unmutes " + userName)

        if message.content.startswith("$kick"):
            message_content = message.content.split()
            userName = message_content[1]
            await message.channel.send("Kicks " + userName)

        if message.content.startswith("$ban"):
            message_content = message.content.split()
            userName = message_content[1]
            await message.channel.send("Bans " + userName)

        if message.content.startswith("$poll"):
            message_content = message.content.split()
            #userName = message_content[1]
            await message.channel.send("starts a poll with some set options, and uses reactions to record responses")

        if message.content.startswith("$roles"):
            message_content = message.content.split()
            #userName = message_content[1]
            await message.channel.send("Shows an embed and has users react to it, and assigns roles to it based on their reactions")

    client.run(token)
