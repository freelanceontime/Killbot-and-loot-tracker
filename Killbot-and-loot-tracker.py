import websocket
from discord import SyncWebhook
from websocket import create_connection
import discord
import re
import requests
import json
from bs4 import BeautifulSoup
import time

minitemprice = 50000000

# Add your Corp or Alliance ID
allianceID = ""
allianceName = ""
corporationID = ""
corpName = ""
allalliancekillswebhookurl = ""
lootchannelwebhookurl = ""

global toggle
toggle = False

def getkill():

    print("New Connection Established")
    ws = create_connection("wss://zkillboard.com/websocket/")

    # Comment Out Either the Alliance or Corp
    ws.send('{"action":"sub","channel":"alliance:' + str(allianceID) + '"}')
    #ws.send('{"action":"sub","channel":"corporation:' + str(corporationID) + '"}')

    while True:
        urls = []
        result =  ws.recv()
        data = json.loads(result)
        urls.append(data['url'])

        for i in range(len(urls)): 
          
            killid = (str(urls[i]))

            webhook = SyncWebhook.from_url(allalliancekillswebhookurl) 
            webhook.send(killid)

            print("kill reported")

            itemname = []
            quantity = []
            price = []
            
            table1 = soup.find_all('table')[5]
            row = table1.find_all('tr')

            for row in table1.find_all('tr'):    
                columns = row.find_all("td", {"class": "item_dropped"})
                if(columns != []):
                    itemname.append(columns[0].text.strip())
                    string = str(columns[0])
                    y = re.search(r"item/([0-9.]+)/", string)
                    item = y.group(1)
                    amount = (columns[1].text.strip())
                    amount = amount.replace(',','')
                    quantity.append(amount)
                    page1 = requests.get("https://api.evemarketer.com/ec/marketstat?typeid=" + item)
                    soup1 = BeautifulSoup(page1.content, 'html.parser', on_duplicate_attribute='ignore')
                    data = str(soup1)
                    x = re.search(r"max>([0-9.]+)<", data)
                    value = x.group(1)
                    valuestrip = value[:-3]
                    priceitem = int(valuestrip) * int(amount)
                    price.append(priceitem)

            for i in range(len(price)):
                if price[i] >= minitemprice:
                    global toggle
                    toggle = True
                    valuenumber = "{:,}".format(price[i])
                    webhook = SyncWebhook.from_url(lootchannelwebhookurl)    
                    webhook.send(str(quantity[i]) + " " + itemname[i] + "\nValued at " + str(valuenumber))
                else:
                    print("Not Worth Looting")

            if toggle == True:
                webhook = SyncWebhook.from_url(lootchannelwebhookurl) 
                webhook.send(killid) 
                toggle = False

while True:
    # try:
    getkill()
    # except:
    #     print("Connection Lost")
    #     pass


