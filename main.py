import os
import discord
import cloudscraper
from requests import Session
from bs4 import BeautifulSoup
import json
import re
import database
import tasikgames
############################################################
# external functions

# replacer

def subRep(content,phr,rep):
  return content[len(phr)+1:].replace(' ',rep)

def wordCheck(content,dbPhr):
  for x in database.db[dbPhr]:
    if x in content.lower().replace(' ',''):
      return True

##################################################################
# server maintenance
from keep_alive import keep_alive

# class calls
client = discord.Client()

# globals
joinPlay = False

@client.event
async def on_ready():
    print(f'I am here as {client.user}')

@client.event
async def on_message(msg):

    # global calls
    global joinPlay, player1 ,player2, playername1, playername2, deck

    if msg.author == client.user:
        return

    # list of commands
    if msg.content == 'help':
        await msg.channel.send(
            'Assalamualaikum, nama saya Tasik Bot.\n\nFeatures:\n1. Stock price --> i.e. !stock TSLA\n2. Crypto price --> i.e. !crypto bitcoin\n3. Etf price --> i.e. !etf SPY\n4. Dota counters --> i.e. !counter juggernaut\n5. Pro CSGO crosshairs --> i.e. !crosshair getright\n6. Blackjack --> !play 21')

######### game of 21 ####################################################
    if msg.content.replace(' ','').lower() == '!play21':
        playername1 = msg.author
        joinPlay = True
        await msg.channel.send(f'Type !join to play a game of 21 with {playername1}')
        
    if joinPlay and msg.content.replace(' ','').lower() == '!join':
        playername2 = msg.author
        await msg.channel.send(f'Player 2 is {playername2}!\n')
        await msg.channel.send(f'{playername1} and {playername2} have decided to play a game of 21.\nCommands:\n1. !draw to draw a card\n2. !done if satisfied with hand')
        joinPlay = False
        
        # start game
        deck = tasikgames.Deck()
        player1 = tasikgames.Player21(playername1, tasikgames.Hand())
        player2 = tasikgames.Player21(playername2, tasikgames.Hand())
        player1.draw_from_deck(deck,2)
        player2.draw_from_deck(deck,2)       
        await playername1.send(f'Your cards are {player1.playercards}')
        await playername2.send(f'Your cards are {player2.playercards}')
    
    if msg.content.replace(' ','').lower() == '!draw':

        if msg.author == player1.name:
            player1.draw_from_deck(deck,1)
            await playername1.send(f'Your cards are {player1.playercards}')
        if msg.author == player2.name:        
            player2.draw_from_deck(deck,1)  
            await playername2.send(f'Your cards are {player2.playercards}')
    if msg.content.replace(' ','').lower() == '!done':
        if msg.author == player1.name:
            player1.ready = True
        if msg.author == player2.name:
            player2.ready = True
        if player1.ready and player2.ready:
            await msg.channel.send(tasikgames.check_winner(player1,player2))
##############################################################################
    # csgo crosshairs
    if msg.content.startswith('!crosshair'):
        rel = subRep(msg.content,'!crosshair','')
        try:
            csCrossHair = 'https://prosettings.net/counterstrike/'+rel+'/'
            response = scraper.get(csCrossHair).text
            soup = BeautifulSoup(response, 'html.parser')    
            all_settings = soup.find_all('code')
            crosshair = f'CROSSHAIR:\n{all_settings[0].text}\n\n'
            viewmodel = f'VIEWMODEL:\n{all_settings[1].text}\n'
            cl_bob = f'CL_BOB:\n{all_settings[2].text}\n'
        except:
            nameSearch = 'https://prosettings.net/search/' + rel
            response = scraper.get(nameSearch).text
            soup = BeautifulSoup(response, 'html.parser')
            realURL = soup.find('a', class_='elementor-post__thumbnail__link')['href']
            response = scraper.get(realURL).text
            soup = BeautifulSoup(response, 'html.parser')    
            all_settings = soup.find_all('code')
            crosshair = f'CROSSHAIR:\n{all_settings[0].text}\n\n'
            viewmodel = f'VIEWMODEL:\n{all_settings[1].text}\n'
            cl_bob = f'CL_BOB:\n{all_settings[2].text}\n'
        
        await msg.channel.send(crosshair+viewmodel+cl_bob)

    # dota hero counters
    if msg.content.startswith('!counter'):

        dotaURL = 'https://www.dotabuff.com/heroes/' + subRep(msg.content,'!counter','-') + '/counters'
        response = scraper.get(dotaURL).text
        soup = BeautifulSoup(response, 'html.parser')

        counters = soup.find('section', class_='counter-outline').article.table.tbody
        counters = counters.find_all('tr')

        printStr = 'Countered by '
        for x in counters:
            printStr += x.find('td')['data-value'] + ', '

        printStr = printStr[0:-2]
        await msg.channel.send(printStr)

    # ETF tracker
    if msg.content.startswith('!etf'):
        rel = subRep(msg.content,'!etf','')
        etfURL = 'https://etfdb.com/etf/' + rel + '/#etf-ticker-profile'
        html = scraper.get(etfURL).text
        soup = BeautifulSoup(html, 'html.parser')
        priceInfo = soup.find('span',id='stock_price_value').text

        await msg.channel.send(f'The price of {rel} is {priceInfo[1:-1]} USD')

    # stock tracker
    if msg.content.startswith('!stock'):
        rel = subRep(msg.content,'!stock','')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
            'Accepts': 'application/json'
        }
        parameters = {
            'access_key': stockAPI,
            'symbols': rel.upper()
        }

        response = scraper.get(marketStackURL, headers=headers, params=parameters).json()
        
        nameStock = response['data'][0]['symbol']
        priceInfo = response['data'][0]['high']
        
        await msg.channel.send(f'The latest high of {nameStock} is {priceInfo} USD, (15min delay)')

    # crypto tracker
    if msg.content.startswith('!crypto'):
        rel = subRep(msg.content,'!crypto','')

        parameters = {
            'slug': rel.lower(),
            'convert': 'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': coinAPI
        }

        session = Session()
        session.headers.update(headers)

        response = json.loads(session.get(coinURL, params=parameters).text)
        idCoin = list(response['data'].keys())[0]
        nameCoin = str(response['data'][idCoin]['name'])
        priceInfo = response['data'][idCoin]['quote']['USD']['price']

        await msg.channel.send(f'The price of {nameCoin} is {round(priceInfo, 4)} USD')

# controversial bot

# billie check
    if wordCheck(msg.content, 'billie'):
        await msg.channel.send(
            f'+stop')
      
# CCP check
    if re.search(u'[\u4e00-\u9fff]', msg.content) or wordCheck(msg.content,'chinph'):
      await msg.channel.send(database.db['chinra'])



keep_alive()

# instances
scraper = cloudscraper.create_scraper()

# URLS
coinURL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
marketStackURL = 'http://api.marketstack.com/v1/intraday/latest'

# db calls

# env calls
coinAPI = os.environ['crptoAPI']
my_secret = os.environ['TOKEN']
stockAPI = os.environ['stockAPI']
# discord instance
client.run(my_secret)
##################################################################
##tests




