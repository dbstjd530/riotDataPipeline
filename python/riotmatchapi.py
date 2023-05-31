import requests
from urllib import parse
import datetime
from collections import OrderedDict
import json
import pandas as pd
import random

class RiotMatchData:
    def __init__(self):
        self.api_key = 'RGAPI-a0b17c3a-858a-43b1-bc81-3b55a768124b'
        self.server_url = "https://asia.api.riotgames.com"

        self.request_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.api_key
        }
    
    def summoner_v4_by_summoner_name(self, summonerName):
        encodingSummonerName = parse.quote(summonerName)
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encodingSummonerName}"
        response_json = requests.get(url, headers=self.request_header).json()
        return response_json
    
    def league_v4_entries(self, summonerId):
        url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}"
        response_json = requests.get(url, headers=self.request_header).json()
        return response_json
        
    # challenger leagues
    ## queue (RANKED_SOLO_5X5)
    def challengersleagues_by_queue(self, queueType):
        selectQueue = queueType
        url = f"https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{selectQueue}"
        response_json = requests.get(url, headers=self.request_header).json()
        return response_json

    # grandmaster leagues
    ## queue (RANKED_SOLO_5X5)
    def grandmasterleagues_by_queue(self, queueType):
        selectQueue = queueType
        url = f"https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{selectQueue}"
        response_json = requests.get(url, headers=self.request_header).json()
        return response_json

    # master leagues
    ## queue (RANKED_SOLO_5X5)
    def masterleagues_by_queue(self, queueType):
        selectQueue = queueType
        url = f"https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{selectQueue}"
        response_json = requests.get(url, headers=self.request_header).json()
        return response_json

    # Iron ~ Diamond leagues
    ## division (1~4) , tier, queue (RANKED_SOLO_5X5)
    def otherleagues_by_queue(self, division, tier, queueType, page):
        
        selectDivision, selectTier, selectQueue, pages = division, tier, queueType, page
        url = f"https://kr.api.riotgames.com/lol/league/v4/entries/{selectQueue}/{tier}/{division}?page={page}"
        response_json = requests.get(url, headers=self.request_header).json()
        return response_json


    def allTierUsersId(self, queueType, page):
        challengers = random.sample(pd.DataFrame(self.challengersleagues_by_queue(queueType)['entries'])['summonerName'].tolist(),k=10)
        grandmasters = random.sample(pd.DataFrame(self.grandmasterleagues_by_queue(queueType)['entries'])['summonerName'].tolist(),k=10)
        masters = random.sample(pd.DataFrame(self.masterleagues_by_queue(queueType)['entries'])['summonerName'].tolist(),k=10)
        diamonds = random.sample(pd.DataFrame(self.otherleagues_by_queue('II', 'DIAMOND', queueType, page))['summonerName'].tolist(),k=10) 
        platinums = random.sample(pd.DataFrame(self.otherleagues_by_queue('II', 'PLATINUM', queueType, page))['summonerName'].tolist(),k=10)
              
        allUser = challengers + grandmasters + masters + diamonds + platinums
        random.shuffle(allUser)
        return allUser

    # Match Information Data
    def match_v5_get_list_match_id(self, puuid, start, count):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        return requests.get(url, headers=self.request_header).json()

    def match_v5_get_match_history(self, matchId):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
        return requests.get(url, headers=self.request_header).json()


    # Primary, sub 룬 번호 -> 이름으로 변경하는 함수
    def runesNameFunc(self, runes_json, runesList, runeStyleNumber, runeType):
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

    def tierInfo(self, summonerId):
        #summonerId = selfsummoner_v4_by_summoner_name(summonerName)['id']
        tierDatas = self.league_v4_entries(summonerId)

        for tierdata in tierDatas:
            if tierdata['queueType'] == 'RANKED_SOLO_5x5':
                data = tierdata
        
        tier = data['tier'] 
        
        return tier
    
    
    # summonerName : '버즈는쩝쩝이', start : 0, count : 10
    def matchDataInfo(self, namesList, start, count):
        #summonerNamesList = self.allTierUsersId(queueType, page)
        summonerNamesList = namesList
        
        jsonDatas_ = []
        for names in summonerNamesList:
            try:
                summonerInfo = self.summoner_v4_by_summoner_name(names)
                puuid, summonerId = summonerInfo['puuid'], summonerInfo['id'] 
                tier = self.tierInfo(summonerId)
                matchId = self.match_v5_get_list_match_id(puuid, start, count)
            
                #jsonDatas_ = []
                for match in matchId:
                    historyData = self.match_v5_get_match_history(match) # history json
                    infoParicipantsIndex = historyData['metadata']['participants'].index(puuid) # json에서 내 닉네임 인덱스 찾기
                    myIndexData = historyData['info']['participants'][infoParicipantsIndex ]
                    
                    # 게임버전
                    gameVersion = historyData['info']['gameVersion'][:5] + '.1'
                    
                    # Item, Spell, Runes URL
                    items_url = f'https://ddragon.leagueoflegends.com/cdn/{gameVersion}/data/en_US/item.json'
                    spell_url = f'https://ddragon.leagueoflegends.com/cdn/{gameVersion}/data/en_US/summoner.json'      
                    runes_url = f'https://ddragon.leagueoflegends.com/cdn/{gameVersion}/data/en_US/runesReforged.json'
        
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
                
                    if len([i for i in range(len(binaryConsecutiveKills)) if binaryConsecutiveKills[i] == 1]) > 0:
                        maxKillIndex = max([i for i in range(len(binaryConsecutiveKills)) if binaryConsecutiveKills[i] == 1])
                        maxKill = list(consecutiveKills.keys())[maxKillIndex]
                    else:
                        maxKill = 'None'
                    
                    # 게임모드
                    gameMode =  historyData['info']['gameMode']
                    
                    # 게임시간
                    #startTime = datetime.datetime.fromtimestamp(int(str(historyData['info']['gameStartTimestamp'])[:-3]))
                    endTime = datetime.datetime.fromtimestamp(int(str(historyData['info']['gameEndTimestamp'])[:-3]))
                    duration = datetime.datetime.fromtimestamp(int(str(historyData['info']['gameDuration'])))
                    now = datetime.datetime.now()

                    # 게임시간 지속 시간
                    gameDuration = str(duration.minute) + '분 ' + str(duration.second) + '초'

                    # ~시간 전
                    fewHoursGame = (now - endTime).days

                    # 게임 승패
                    booleanVictory = [myIndexData['win']]
                    stringVictory = list(map(lambda x: 'Victory' if int(x) == 1 else 'Lose', booleanVictory))[0]

                    # 킬/데스/어시스트
                    kills = myIndexData['kills']
                    deaths = myIndexData['deaths']
                    assists = myIndexData['assists']
                    kda = [kills, deaths, assists]
                    
                    # 라인
                    lane = myIndexData['teamPosition']
                    
                    # 게임 내 챔피언 레벨
                    champLevel = myIndexData['champLevel']

                    # 게임 플레이한 챔피언 이름
                    championName = myIndexData['championName']
                    
                    # 게임 내 아이템 리스트
                    items_json = requests.get(items_url, headers=self.request_header).json()
                    items = [items_json['data'][str(myIndexData['item%s'%i])]['name'] for i in range(7) if myIndexData['item%s'%i] != 0]
                    
                    # SPELL Check / output: [['정화'], ['점멸']]
                    spell_json = requests.get(spell_url, headers=self.request_header).json()
                    champSpellList = [myIndexData['summoner1Id'],myIndexData['summoner2Id']]
                    champSpell = [[spell_json['data'][json_obj]['name'] for json_obj in spell_json['data'] if spell_json['data'][json_obj]['key'] == str(spell)]for spell in champSpellList]

                    # 룬, 특성
                    runes_json = requests.get(runes_url, headers=self.request_header).json()

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
                    primaryRunesNameList = self.runesNameFunc(runes_json, runesList, runeStyleNumber, runeType)

                    ### 서브 룬
                    runesList = subRunes
                    runeStyleNumber = subRunesStyle
                    runeType = 'sub'
                    subRunesNameList = self.runesNameFunc(runes_json, runesList, runeStyleNumber, runeType)

                    # 제어와드 개수
                    visionWardsCount = myIndexData['visionWardsBoughtInGame']
                    
                    # 미니언 킬(CS)
                    CsCount = myIndexData['totalMinionsKilled'] + myIndexData['neutralMinionsKilled']
                    
                    # 매치정보 return json 파일
                    matchDataJson = OrderedDict()
                    matchDataJson["matchId"] = match
                    matchDataJson["gameMode"] = gameMode
                    matchDataJson["outCome"] = stringVictory
                    matchDataJson["gameDuration"] = gameDuration
                    matchDataJson["fewHoursGame"] = fewHoursGame
                    matchDataJson['tier'] = tier
                    
                    matchDataJson["championInfo"] = {'championName': championName,
                                                     'lane': lane,
                                                    'championLevel': champLevel,
                                                    'killStreak': maxKill,
                                                    'kill': kills,
                                                    'death': deaths,
                                                    'assist': assists,
                                                    'spells': champSpell,
                                                    'items': items,
                                                    'runes': {'primaryRunes': primaryRunesNameList,
                                                            'subRunes':subRunesNameList},
                                                    'visionWardCount': visionWardsCount,
                                                    'minionCOunt': CsCount
                                                    }

                    result = json.dumps(matchDataJson, ensure_ascii=False, indent=4)
                    jsonDatas_.append(json.loads(result))
            
            except KeyError:
                print('Key Error')
                continue
            except requests.exceptions.RequestException as e:
                print(e)
            except Exception:
                print('Exception!!')
                continue
        return jsonDatas_s