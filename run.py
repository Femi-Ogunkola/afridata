import datetime as dt
import json
from typing import List

import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pandas.core.frame import DataFrame

os.environ['IMAGEIO_FFMPEG_EXE'] = 'ffmpeg'

bucket_name = "xeraphys"
ACCESS_KEY = "AKIARVAPJUP55NYGZ555"
SECRET_KEY = "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"
region ="us-east-1"


# method to upload file to s3 bucket
def upload_to_aws(local_file, bucket_name, region):
    """
    Uploading to aws s3 bucket
    args
    local_file: filename we wish to upload
    bucket_name: s3 bucket name
    region: aws region
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    try:
        s3_file = local_file
        s3.upload_file(local_file, bucket_name, s3_file, ExtraArgs={'ACL': 'public-read'})
        location = region
        url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, s3_file)
        print(url)
        print("Upload Successful")
        return url
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def get_total_seconds(stringHMS):
    """A string repensenting the Hour, minute and second e.g 00:00:05
    """
    ftr = [60,1]
    return sum([a*b for a,b in zip(ftr, map(int,stringHMS.split(':')))])


def parse(a,event):
    start,stop = [],[]
    for i in range(len(a.index)):
        if len(a[event][i]) !=0:
            start.append(int(get_total_seconds(a[event][i][0].get("start_time"))))
            stop.append(int(get_total_seconds(a[event][i][0].get("stop_time"))))
    return start, stop
    
def player_event_clip(filename,event):
    start,stop = parse(filename,event)
    #print(start,stop)
    #uri = 'https://asvideo.s3.us-east-2.amazonaws.com/clip.mp4'
    vid = "vid.mp4" #place video
    clip = VideoFileClip(vid)
    clips=[]
    for i in range(len(start)):
        clips.append(clip.subclip(start[i],stop[i]))
    if len(clips)>0:
        final = concatenate_videoclips(clips)
        return final

    return  
            

def all_events(filename)-> List:
    print('here')
    #a = pd.read_json(filename,orient="index")
    cols = filename.columns
    all_links = []
    for j in range(len(filename.index)):
        for i in range(len(cols)):
            print('here')
            final = player_event_clip(filename,str(cols[i]))
            if final != None:
                final.write_videofile(f"{str(cols[i])}{j}.mp4")
                url='link'#upload_to_aws(str(cols[i])+".mp4", bucket_name, region)
                filename[f'{cols[i].split(".")[0]}.clip']= url
                #all_links.append(url)
    #filename['eventsJson'] = all_links
    final_json = filename.to_json(orient='records')
    print(final_json)
    return final_json    
    

if __name__ == "__main__":
    dict = [[{'successful_shortpass': {'total': 5, 'event_clip': '', 'timeline': []}, 'successful_longpass': {'total': 0, 'event_clip': '', 'timeline': []}, 'line_break_pass': {'total': 0, 'event_clip': '', 'timeline': []}, 'dribbles': {'attempts': 0, 'completed': 0, 'skill_moves': 0, 'nut_megs': 0, 'failed': 0, 'event_clip': '', 'timeline': []}, 'shots': {'outsidebox_ontarget': 0, 'outsidebox_offtarget': 0, 'insidebox_offtarget': 0, 'insidebox_ontarget': 0, 'total': 0, 'event_clip': '', 'timeline': []}, 'crosses': {'total': 0, 'event_clip': '', 'timeline': []}, 'goals': {'total': 0, 'header': 0, 'oneVone': 0, 'inside_box_shot_goal': 0, 'outside_box_shot_goal': 0, 'event_clip': '', 'timeline': []}, 'assists': {'total': 1, 'event_clip': '', 'timeline': [{'start_time': '0:0', 'stop_time': '0:12', '_id': '6120f425dafe6f0017c53d9d'}]}, 'chance_created': {'total': 0, 'timeline': []}, 'freeKick': {'off_target': 0, 'on_target': 0, 'total': 0, 'timeline': []}, 'penalty': {'event_clip': '', 'total': 0, 'missed': 0, 'scored': 0, 'timeline': []}, 'fouls': {'total': 0, 'won_in_opp_half': 0, 'won_in_own_half': 0, 'conceded_in_own_half': 0, 'conceded_in_opp_half': 0}, 'interceptions': {'event_clip': '', 'opponents_half': 0, 'own_half': 0, 'total': 0, 'timeline': []}, 'tackles': {'total': 0, 'event_clip': '', 'successful': 0, 'unsuccessful': 0, 'timeline': []}, 'ball_progression': {'event_clip': '', 'total': 0, 'own_half': 0, 'opp_half': 0, 'timeline': []}, 'blocks': {'total': 0, 'event_clip': '', 'timeline': []}, 'clearance': {'total': 0, 'event_clip': '', 'goal_line': 0, 'under_pressure': 0, 'timeline': []}, 'duels': {'total': 0, 'event_clip': '', 'won_aerial': 0, 'won_ground': 0, 'timeline': []}, 'saves': {'event_clip': '', 'oneVone': 0, 'inside_box': 0, 'outside_box': 1, 'total': 1, 'timeline': [{'start_time': '4:33', 'stop_time': '4:34', '_id': '6120f425dafe6f0017c53d9e'}]}, 'card': {'total': 0, 'yellow_dissent': 0, 'yellow_foul': 0, 'red_dissent': 0, 'red_foul': 0}, 'catches': {'event_clip': '', 'simple': 0, 'complex': 1, 'total': 1, 'timeline': [{'start_time': '0:53', 'stop_time': '0:54', '_id': '6120f425dafe6f0017c53d9f'}]}, 'start': 1, 'minutes': 88, 'bench': 0, '_id': '6120f425dafe6f0017c53d9c', 'match': '611fb82fcec3be0017a4c843', 'player_id': '6113e3deb5ef4d0017b81701', '__v': 0}],
        [{'successful_shortpass': {'total': 5, 'event_clip': '', 'timeline': []}, 'successful_longpass': {'total': 0, 'event_clip': '', 'timeline': []}, 'line_break_pass': {'total': 0, 'event_clip': '', 'timeline': []}, 'dribbles': {'attempts': 0, 'completed': 0, 'skill_moves': 0, 'nut_megs': 0, 'failed': 0, 'event_clip': '', 'timeline': []}, 'shots': {'outsidebox_ontarget': 0, 'outsidebox_offtarget': 0, 'insidebox_offtarget': 0, 'insidebox_ontarget': 0, 'total': 0, 'event_clip': '', 'timeline': []}, 'crosses': {'total': 0, 'event_clip': '', 'timeline': []}, 'goals': {'total': 0, 'header': 0, 'oneVone': 0, 'inside_box_shot_goal': 0, 'outside_box_shot_goal': 0, 'event_clip': '', 'timeline': []}, 'assists': {'total': 1, 'event_clip': '', 'timeline': [{'start_time': '0:0', 'stop_time': '0:17', '_id': '6120f425dafe6f0017c53d9s'}]}, 'chance_created': {'total': 0, 'timeline': []}, 'freeKick': {'off_target': 0, 'on_target': 0, 'total': 0, 'timeline': []}, 'penalty': {'event_clip': '', 'total': 0, 'missed': 0, 'scored': 0, 'timeline': []}, 'fouls': {'total': 0, 'won_in_opp_half': 0, 'won_in_own_half': 0, 'conceded_in_own_half': 0, 'conceded_in_opp_half': 0}, 'interceptions': {'event_clip': '', 'opponents_half': 0, 'own_half': 0, 'total': 0, 'timeline': []}, 'tackles': {'total': 0, 'event_clip': '', 'successful': 0, 'unsuccessful': 0, 'timeline': []}, 'ball_progression': {'event_clip': '', 'total': 0, 'own_half': 0, 'opp_half': 0, 'timeline': []}, 'blocks': {'total': 0, 'event_clip': '', 'timeline': []}, 'clearance': {'total': 0, 'event_clip': '', 'goal_line': 0, 'under_pressure': 0, 'timeline': []}, 'duels': {'total': 0, 'event_clip': '', 'won_aerial': 0, 'won_ground': 0, 'timeline': []}, 'saves': {'event_clip': '', 'oneVone': 0, 'inside_box': 0, 'outside_box': 1, 'total': 1, 'timeline': [{'start_time': '3:33', 'stop_time': '3:34', '_id': '6120f425dafe6f0017c53dfe'}]}, 'card': {'total': 0, 'yellow_dissent': 0, 'yellow_foul': 0, 'red_dissent': 0, 'red_foul': 0}, 'catches': {'event_clip': '', 'simple': 0, 'complex': 1, 'total': 1, 'timeline': [{'start_time': '0:65', 'stop_time': '0:75', '_id': '6120f425dafe6f0017c53d4f'}]}, 'start': 1, 'minutes': 88, 'bench': 0, '_id': '6120f425dafe6f0017c53d9d', 'match': '611fb82fcec3be0017a4c743', 'player_id': '6113e3deb5ef4d0017881701', '__v': 0}]]
    data = pd.DataFrame(dict)
    data=pd.json_normalize(data[0])
    data = data.filter(regex='timeline')
    #data.head(20)
    data=data.to_dict()
    #print(data)
    a = pd.DataFrame.from_dict(data)
    eventsJson = all_events(a)
    print(eventsJson)
