# History Data Parsing
## matchDataInfo Function 
### item, spell, rune 게임 버전 별 Json 파일 변경
item, spell, rune 데이터는 암호화된 데이터로 리턴 받습니다. 해당 아이템, 스펠, 룬의 이름을 알기위해 Riot에서 제공하는 각각의 Json 파일 Url을 
게임 버전에 맞게 가져와야 합니다.

```python
# 게임버전
gameVersion = historyData['info']['gameVersion'][:5] + '.1'

# Item, Spell, Runes URL
items_url = f'https://ddragon.leagueoflegends.com/cdn/{gameVersion}/data/en_US/item.json'
spell_url = f'https://ddragon.leagueoflegends.com/cdn/{gameVersion}/data/en_US/summoner.json'      
runes_url = f'https://ddragon.leagueoflegends.com/cdn/{gameVersion}/data/en_US/runesReforged.json'
        
```
