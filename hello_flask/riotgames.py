import requests

def findSummoner(sumName):

    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + sumName + "?api_key=RGAPI-166f7c8a-76f0-41d5-a269-c3fbddc4cc48"

    resp = request.get(URL)
    respJSON = resp.json()

    sumLevel = respJSON('summonerLevel')
    sumLevel = str(sumLevel)

    ID = respJSON('id')
    ID = str(ID)

    URL2 = "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + ID + "?api_key=RGAPI-5f73779d-d12c-45f1-ac61-788ba13a8409"

    resp2 = request.get(URL2)
    respJSON2 = resp2.json()

    highestChamp = respJSON2(0)("championId")
    highestChamp = str(highestChamp)

    champLevel = respJSON2(0)("championLevel")
    champLevel = str(champLevel)

    champMastery = respJSON2(0)("championPoints")
    champMastery = str(champMastery)

    sumInfo = [sumName, sumLevel,highestChamp,champLevel,champMastery]

    return sumInfo
