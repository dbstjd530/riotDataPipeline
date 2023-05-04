import requests
from urllib import parse
import pprint

pp = pprint.PrettyPrinter(indent=4)

api_key = 'RGAPI-a0b17c3a-858a-43b1-bc81-3b55a768124b'
server_url = "https://kr.api.riotgames.com"

request_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

def summoner_v4_by_summoner_name(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    url = server_url + f"/lol/summoner/v4/summoners/by-name/{encodingSummonerName}"
    response_json = requests.get(url, headers=request_header).json()
    return response_json

def league_v4_entries(summonerId):
    url = server_url + f"/lol/league/v4/entries/by-summoner/{summonerId}"
    response_json = requests.get(url, headers=request_header).json()
    return response_json

#티어 검색 (summonerId :id, queueType : solo or free)
def myTier(summonerName, queueType):
    summonerId = summoner_v4_by_summoner_name(summonerName)['id']
    tierDatas = league_v4_entries(summonerId)

    
    if queueType == 'solo':
        type = 'RANKED_SOLO_5x5'
    else:
        type = 'RANKED_FLEX_SR'
    
    for tierdata in tierDatas:
        if tierdata['queueType'] == type:
            data = tierdata
      
    tier = data['tier'] + ' ' + data['rank'] + ' : ' + str(data['leaguePoints'])
    winCount = data['wins']
    loseCount = data['losses']
    winRate = str(int(round((winCount / (winCount + loseCount)) * 100,0))) + '(%)'    
    
    tierInformation = [summonerName, tier, winCount, loseCount, winRate]
    return tierInformation

summonerName = '야스오의점심식사'
myTier(summonerName,'solo')