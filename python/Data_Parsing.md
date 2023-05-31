# League of Legends API Data Parsing
## 1. 데이터 파싱
⚠ Riot Developer에서 API key 승인을 먼저 받아야합니다.
### 1.1 챌린저, 그랜드마스터 등 각 티어 유저들의 SummonerName List 받아오기
챌린저, 그랜드마스터, 마스터, 다이아 등 각 티어 별로 SummonerName(닉네임)을 받아오는 API가 각각 다르기 때문에 함수를 맞춰서 작성합니다.
```python
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
```

### 1.2 모든 티어들의 유저 SummonerName을 종합하여 받아오기.
Json으로 리턴되는 각 함수를 SummonerName 정보만 있는 리스트로 형 변환 후에 랜덤으로 추출합니다. 
```python
    def allTierUsersId(self, queueType, page):
        challengers = random.sample(pd.DataFrame(self.challengersleagues_by_queue(queueType)['entries'])['summonerName'].tolist(),k=10)
        grandmasters = random.sample(pd.DataFrame(self.grandmasterleagues_by_queue(queueType)['entries'])['summonerName'].tolist(),k=10)
        masters = random.sample(pd.DataFrame(self.masterleagues_by_queue(queueType)['entries'])['summonerName'].tolist(),k=10)
        diamonds = random.sample(pd.DataFrame(self.otherleagues_by_queue('II', 'DIAMOND', queueType, page))['summonerName'].tolist(),k=10) 
        platinums = random.sample(pd.DataFrame(self.otherleagues_by_queue('II', 'PLATINUM', queueType, page))['summonerName'].tolist(),k=10)
              
        allUser = challengers + grandmasters + masters + diamonds + platinums
        random.shuffle(allUser)
        return allUser
```

