from riotwatcher import LolWatcher, ApiError
import pandas as pd
import json


def summonerInfo(sumName):
    api_key = 'RGAPI-166f7c8a-76f0-41d5-a269-c3fbddc4cc48'
    watcher = LolWatcher(api_key)
    my_region = 'na1'

    me = watcher.summoner.by_name(my_region, sumName)
    print(me)


    print(me.get(0))
    print(me.get(1))
    print(me.get(2))
    print(me.get(3))
    print(me.get(4))
    print(me.get(5))
    print(me.get(6))

    return (me)
