import requests
import json

TOKEN = 'DISCORD_TOKEN'

CHANNEL_ID = 'CHANNEL_ID'

url = f'https://discord.com/api/v10/channels/{CHANNEL_ID}/messages'
def NBAMaker():
    title = f"BUY !"
    description = f"BUY !"
    color = 0x00FF00
    SendEmbed(title, description, color)
def PotentialBuyEmbed(type, dom, ext, polymarket_price, winamax_price, amount, size, ev):
    title = f"POTENTIAL BUY :pray:"
    description = f"MATCH : ```{dom} - {ext}```\nTYPE : ```{type}```\nPOLYMARKET : ```{polymarket_price}```\nWINAMAX : ```{winamax_price}```\nAMOUNT : ```{amount}$```\nSIZE : ```{size}$```\nEV : ```{ev}```"
    color = 0xD1A0F3
    SendEmbed(title, description, color)

def PotentialSellEmbed(team, mise, p):
    title = f"POTENTIAL SELL :pray:"
    description = f"TEAM : ```{team}```\nAMOUNT : ```{mise}$```\POLYMARKET : ```{p}```"
    color = 0xD1A0F3
    SendEmbed(title, description, color)

def AcceptBuyEmbed(type, dom, ext, polymarket_price, winamax_price, amount, size, ev):
    title = f"ACCEPTED BUY :money_with_wings:"
    description = f"MATCH : ```{dom} - {ext}```\nTYPE : ```{type}```\nPOLYMARKET : ```{polymarket_price}```\nWINAMAX : ```{winamax_price}```\nAMOUNT : ```{amount}$```\nSIZE : ```{size}$```\nEV : ```{ev}```"
    color = 0x00FF00
    SendEmbed(title, description, color)

def AcceptSellEmbed(team, mise):
    title = f"ACCEPTED Sell :money_with_wings:"
    description = f"TEAM : ```{team}```\nAMOUNT : ```{mise}$```"
    color = 0x00FF00
    SendEmbed(title, description, color)

def DeniedBuyEmbed(type, dom, ext, polymarket_price, winamax_price, amount, size, errorMsg):
    title = f"FAILED BUY :x:"
    description = f"MATCH : ```{dom} - {ext}```\nTYPE : ```{type}```\nPOLYMARKET : ```{polymarket_price}```\nWINAMAX : ```{winamax_price}```\nAMOUNT : ```{amount}$```\nSIZE : ```{size}$```\nERROR : ```{errorMsg}```"
    color = 0xFF7F7F
    SendEmbed(title, description, color)

def DeniedSellEmbed(team, mise):
    title = f"FAILED SELL :x:"
    description = f"TEAM : ```{team}```\nAMOUNT : ```{mise}$```"
    color = 0xFF7F7F
    SendEmbed(title, description, color)

def SendEmbed(title, description, color):
    embed = {
        "title": title,
        "description": description,
        "color": color,
    }

    data = {
        'embeds': [embed],
        'content': "@everyone"
    }

    headers = {
        'Authorization': f'Bot {TOKEN}', 
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        print(f'Erreur: {response.status_code}')
        print(response.text)