import requests
import datetime
import math
from mcuuid.api import GetPlayerData
from time import sleep

def hypixel_api_scrapper(playername):
    API_KEY = "" #API Key here
    url = f"https://api.hypixel.net/player?key={API_KEY}&name={playername}"
    res = requests.get(url)
    data = res.json()
    if data['player'] is None:
        return None   
    elif 'lastLogout' not in data['player']:
        return None
    
    data_player = data['player'] 
    last_login = data_player['lastLogin']
    last_logout = data_player['lastLogout']
    
    if last_logout > last_login:
#         print(playername)
#         print(convert_miliseconds(last_logout - last_login))
        return None
    
    exp = int(data['player']['networkExp']) 
    player_level = math.floor(1 + temp + math.sqrt(temp + temp2 * exp))  

    
    miliseconds_online = (datetime.datetime.now().timestamp() * 1000) - last_login
    print(playername)
    print("Player level:",player_level)
    print("Last login time:", datetime.datetime.fromtimestamp(last_login/1000).strftime('%m-%d-%Y %H:%M:%S'))
    print("Last logout time:", datetime.datetime.fromtimestamp(last_logout/1000).strftime('%m-%d-%Y %H:%M:%S'))
    if 'mostRecentGameType' in data_player:
        print("Player has been online for:", convert_miliseconds(miliseconds_online))
        print("Most recent game type:", data_player['mostRecentGameType'].title(), "\n")
    else:
        print("Player has been online for:", convert_miliseconds(miliseconds_online),"\n")


def convert_miliseconds(miliseconds):
    millis = int(miliseconds)
    seconds = int((millis/1000)%60)
    minutes = int((millis/(1000*60))%60)
    hours = (millis/(1000*60*60))%24
    if hours > 1 and minutes > 1 and seconds > 1:
        return ("%d hours %d minutes %d seconds" % (hours, minutes, seconds))
    elif hours < 1 and minutes > 1 and seconds > 1:
        return ("%d hours %d minutes %d seconds" % (hours, minutes, seconds))
    elif hours < 1 and minutes > 1 and seconds < 1:
        return ("%d hours %d minutes %d second" % (hours, minutes, seconds))
    elif hours > 1 and minutes > 1 and seconds < 1:
        return ("%d hours %d minutes %d second" % (hours, minutes, seconds))
    else: 
        return ("%d hours %d minute %d seconds" % (hours, minutes, seconds))



def main(names):
    user = GetPlayerData(names)
    if user.valid is True:
        playeruuid = user.uuid
    else:
        return None
    
    global temp,temp2
    temp = -(10_000 - 0.5 * 2_500) / 2_500
    temp2 = 2/2_500
    
    API_KEY = "" #API Key here
    url = f"https://api.hypixel.net/friends?key={API_KEY}&uuid={playeruuid}"
    res = requests.get(url)
    data = res.json()
    for player in data['records']:
        if player['uuidSender'] == playeruuid:
            player = GetPlayerData(player['uuidReceiver'])
            if player.valid is True:
                hypixel_api_scrapper(player.username)
                sleep(.2)
        else:
            player = GetPlayerData(player['uuidSender'])
            if player.valid is True:
                hypixel_api_scrapper(player.username)
                sleep(.2)

names = "" #Username here
main(names)