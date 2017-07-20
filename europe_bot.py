import discord
import asyncio
import smashgg

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!ping'):
       await client.send_message(message.channel, 'Pong!')

    elif message.content.startswith('!countnotable'):
        data = smashgg.count_notable(smashgg.url_to_api(message.content[14:]),smashgg.nps)
        text = "A total of **" + str(data[0]) + "** notable players\n**" + str(data[1]) + "** ranked 1-5\n**"+str(data[0]-data[1]) + "** ranked 6-10"
        await client.send_message(message.channel,text)
    elif message.content.startswith('!info'):
        text = smashgg.get_eventInfo(message.content[6:])
        await client.send_message(message.channel,text)


client.run("CONNECTION-KEY")
