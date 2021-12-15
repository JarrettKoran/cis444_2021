from riotwatcher import LolWatcher, ApiError
import pandas as pd
import json


def summonerInfo(sumName):
    api_key = 'RGAPI-166f7c8a-76f0-41d5-a269-c3fbddc4cc48'
    watcher = LolWatcher(api_key)
    my_region = 'na1'

    me = watcher.summoner.by_name(my_region, sumName)
    print(me)

    json_sumLevel =  me['summonerLevel']

    print('Summoner Level: ' + json_sumLevel)


    return (me)
