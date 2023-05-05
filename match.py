import requests
from urllib import parse
import pprint
import datetime


api_key = 'my api key'
server_url = "https://asia.api.riotgames.com"

# Item, Spell, Runes URL
items_url = 'https://ddragon.leagueoflegends.com/cdn/13.8.1/data/ko_KR/item.json'
spell_url = 'https://ddragon.leagueoflegends.com/cdn/13.8.1/data/ko_KR/summoner.json'
runes_url = 'https://ddragon.leagueoflegends.com/cdn/10.6.1/data/ko_KR/runesReforged.json'



request_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

def summoner_v4_by_summoner_name(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encodingSummonerName}"
    response_json = requests.get(url, headers=request_header).json()
    return response_json

# Match Information Data
def match_v5_get_list_match_id(puuid, start, count):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    return requests.get(url, headers=request_header).json()

def match_v5_get_match_history(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
    return requests.get(url, headers=request_header).json()


def match_v5_get_match_timeline(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline"
    return requests.get(url, headers=request_header).json()


# Primary, sub 룬 번호 -> 이름으로 변경하는 함수
def runesNameFunc(runes_json,runesList, runeStyleNumber, runeType):
    myRuneList=[]
    myRuneSlot = runeStyleNumber
    selectSlotInfo = [run_slot for run_slot in runes_json if run_slot['id'] == myRuneSlot]
    selectSlot = selectSlotInfo[0]['slots']
    selectSlotName = selectSlotInfo[0]['name']

    myRuneList.append(selectSlotName)
    
    if runeType == 'primary':
        for selectRunes in range(len(runesList)):
            seletRunesId = runesList[selectRunes]
            runeSection = selectSlot[selectRunes]['runes']
            
            for runes in runeSection:
                runeId = runes['id']
                
                if runeId == seletRunesId:
                    myRuneList.append(runes['name'])
                    
    elif runeType == 'sub':
        for selectRunes in runesList:
            seletRunesId = selectRunes

            for runeSection_obj in selectSlot:
                runeSection = runeSection_obj['runes']
                
                for runes in runeSection:
                    runeId = runes['id']
                    
                    if runeId == seletRunesId:
                        myRuneList.append(runes['name'])
                    
    return myRuneList



'''
puuid = summoner_v4_by_summoner_name('버즈는쩝쩝이')['puuid']
matchId = match_v5_get_list_match_id(puuid,0,10)[0]
historyData = match_v5_get_match_history(matchId)
'''


# summonerName : '버즈는쩝쩝이', start : 0, count : 10
def matchDataInfo(summonerName, start, count):
    puuid = summoner_v4_by_summoner_name(summonerName)['puuid']
    matchId = match_v5_get_list_match_id(puuid, start, count)
    
    for match in matchId:
        historyData = match_v5_get_match_history(match) # history json
        infoParicipantsIndex = historyData['metadata']['participants'].index(puuid) # json에서 내 닉네임 인덱스 찾기
        myIndexData = historyData['info']['participants'][infoParicipantsIndex ]
        
        #  퍼스트블러드, 더블킬, 트리플킬, 쿼드라킬, 펜타킬 판단
        firstBloodKill = myIndexData['firstBloodKill']
        doubleKills = myIndexData['doubleKills']
        tripleKills = myIndexData['tripleKills']
        quadraKills = myIndexData['quadraKills']
        pentaKills = myIndexData['pentaKills']

        ## 퍼스트블러드, 더블킬, 트리플킬, 쿼드라킬, 펜타킬 Dictionary
        consecutiveKills = {'FirstBlood': int(firstBloodKill), 
                            'DoubleKill': doubleKills,
                            'TripleKill': tripleKills,
                            'QuadraKill': quadraKills,
                            'PentaKill': pentaKills}

        binaryConsecutiveKills = list(map(lambda x: 1 if x > 0 else 0, consecutiveKills.values()))
        maxKillIndex = max([i for i in range(len(binaryConsecutiveKills)) if binaryConsecutiveKills[i] == 1])
        maxKill = list(consecutiveKills.keys())[maxKillIndex]
        
        # 게임모드
        gameMode =  historyData['info']['gameMode']
        
        # 게임시간
        startTime = datetime.fromtimestamp(int(str(historyData['info']['gameStartTimestamp'])[:-3]))
        endTime = datetime.fromtimestamp(int(str(historyData['info']['gameEndTimestamp'])[:-3]))
        duration = datetime.fromtimestamp(int(str(historyData['info']['gameDuration'])))
        now = datetime.datetime.now()

        # 게임시간 지속 시간
        gameDuation = str(duration.minute) + '분 ' + str(duration.second) + '초'

        # ~시간 전
        fewHoursGame = str(now.hour - endTime.hour) + '시간 전'

        # 게임 승패
        booleanVictory = [myIndexData['win']]
        stringVictory = list(map(lambda x: 'Victory' if int(x) == 1 else 'Lose', booleanVictory))[0]

        # 킬/데스/어시스트
        kills = myIndexData['kills']
        deaths = myIndexData['deaths']
        assists = myIndexData['assists']
        kda = [kills, deaths, assists]
        
        # 게임 내 챔피언 레벨
        champLevel = myIndexData['champLevel']

        # 게임 플레이한 챔피언 이름
        championName = myIndexData['championName']
        
        # 게임 내 아이템 리스트
        items_json = requests.get(items_url, headers=request_header).json()
        items = [items_json['data'][str(myIndexData['item%s'%i])]['name'] for i in range(7)]
        
        # SPELL Check / output: [['정화'], ['점멸']]
        spell_json = requests.get(spell_url, headers=request_header).json()
        champSpellList = [myIndexData['summoner1Id'],myIndexData['summoner2Id']]
        champSpell = [[spell_json['data'][json_obj]['name'] for json_obj in spell_json['data'] if spell_json['data'][json_obj]['key'] == str(spell)]for spell in champSpellList]

        # 룬, 특성
        runes_json = requests.get(runes_url, headers=request_header).json()

        ## 주, 서브 룬 ID List
        perksList = [myIndexData['perks']['styles'][0]['selections'], myIndexData['perks']['styles'][1]]

        ## 주, 서브 룬 ID List
        primaryRunes = [perksList[0][perks_obj]['perk'] for perks_obj in range(len(perksList[0]))]
        subRunes = [perksList[1]['selections'][subperks_obj]['perk'] for subperks_obj in range(len(perksList[1]['selections']))]

        ## 주, 서브 룬 Style (runes_json에서 Slot 위치)
        primaryRunesStyle = myIndexData['perks']['styles'][0]['style']
        subRunesStyle = perksList[1]['style']
        
        ## 주요 룬, 서브 룬 이름 리스트
        ### 주요 룬
        runesList = primaryRunes
        runeStyleNumber = primaryRunesStyle
        runeType = 'primary'
        primaryRunesNameList = runesNameFunc(runes_json,runesList, runeStyleNumber, runeType)

        ### 서브 룬
        runesList = subRunes
        runeStyleNumber = subRunesStyle
        runeType = 'sub'
        subRunesNameList = runesNameFunc(runes_json,runesList, runeStyleNumber, runeType)

        # 제어와드 개수
        visionWardsCount = myIndexData['visionWardsBoughtInGame']
        # 미니언 킬(CS)
        CsCount = myIndexData['totalMinionsKilled'] + myIndexData['neutralMinionsKilled']
