import discord
from actions.hello import hello
from actions.pumpdump import pumpdump
from actions.long_short import long_short
from actions.chart import chart
from actions.wallet import wallet

import os
import logging
import traceback

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


# python3 -m pip install python-binance
# pip install ta
# pip install apscheduler
# pip install discord
# pip install plotly
# pip install kaleido
# https://github.com/Rapptz/discord.py
#d doc du framework : https://discordpy.readthedocs.io/en/latest/api.html#discord.Member

# problem pybit de syncronisation sur WSL :  sudo hwclock -s
#       sudo ntpdate pool.ntp.org

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        # Test part
        #await show_wallet(Test=True)
        

    async def on_message(self, message):
        try:
            # we do not want the bot to reply to itself
            if message.author.id == self.user.id:
                return


            if (
                    (message.channel.id != 956956942633414817) 
                and (message.channel.id != 955193076668829696)
                and (message.channel.id != 958078641483427880)
                ):
                return

            a_message = message.content.split(' ')

            if a_message[0] == '!help':
                await message.channel.send('Commandes disponibles \n\
    !hello => just say hello :)\n\
    !chart => show a chart\n\
    !ls => longshort ratio\n\
    !w user => Show Wallet user=[tedy, jojo]\n\
        ')

            if a_message[0] == '!hello':
                await hello(message)

            if a_message[0] == '!chart':
                await chart(message)

            if a_message[0] == '!ls':
                await long_short(message)

            if a_message[0] == '!w':
                await wallet(message)

            # if 'dump' in message.content:
            #     await pumpdump(message, 'dump')
            # elif 'pump' in message.content:
            #     await pumpdump(message, 'pump')
                

            # Garé pour les infos
            # await message.channel.send('Hello {0.author.mention}'.format(message))
            # await message.channel.send('Hello {0.author.mention}'.format(message))
            # await message.channel.send('Hello {0.author}'.format(message))
        except Exception as e:
            logging.error(traceback.format_exc())
            # Logs the error appropriately.
            await message.channel.send('Mauvaise commande.') 

client = MyClient()
base_dir = os.path.realpath(os.path.dirname(os.path.abspath(__file__))+'/')+'/'

async def show_wallet(Test=False):
    await client.wait_until_ready()

    # 926406999107846245 channel grid-passivbot
    # 955193076668829696 channel test
    # 910612726081024010 channel onlyupx3
    if not Test:
        c = client.get_channel(926406999107846245)  
        data = {'content': "!w tedy from_auto_bot", 'channel': c}
        message = Struct(**data)
        await wallet(message)

        c = client.get_channel(910612726081024010)  
        data = {'content': "!w jojo from_auto_bot", 'channel': c}
        message = Struct(**data)
        await wallet(message)

        c = client.get_channel(958078641483427880)  
        data = {'content': "!w pro from_auto_bot", 'channel': c}
        message = Struct(**data)
        await wallet(message)
        
    else:
        c = client.get_channel(955193076668829696)  
        data = {'content': "!w tedy from_auto_bot", 'channel': c}
        message = Struct(**data)
        await wallet(message)


#initializing scheduler
scheduler = AsyncIOScheduler()
#sends "Your Message" at 12PM and 18PM (Local Time)
scheduler.add_job(show_wallet, CronTrigger(hour="9", minute="0", second="0")) 
#starting the scheduler
scheduler.start()


client.run(open(base_dir+"/config/token.txt", 'r').read())

