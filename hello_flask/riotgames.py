from riotwatcher import LolWatcher, ApiError
import pandas as pd
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json


def summonerInfo(sumName):
    api_key = 'RGAPI-166f7c8a-76f0-41d5-a269-c3fbddc4cc48'
    watcher = LolWatcher(api_key)
    my_region = 'na1'

    summoner = watcher.summoner.by_name(my_region, sumName)
    print(summoner)

    rankedStats = watcher.league.by_summoner(my_region,  summoner['id'])
    print(rankedStats)


    return json_response(sumInfo=summoner)
