import pandas as pd
from season.store.retriever import Retriever


def  get_player_match_events(eventList):
    playerMatchEventsDict = [event.get('playerMatchEvents') for event in eventList]
    return playerMatchEventsDict

def get_player_match_events_csv(file):
    data = pd.DataFrame.from_dict(file,orient='records')
    return data
