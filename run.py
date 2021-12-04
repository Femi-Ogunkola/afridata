import json
import pandas as pd
import clips
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import boto3
from botocore.exceptions import NoCredentialsError
import datetime as dt
import json

os.environ['IMAGEIO_FFMPEG_EXE'] = 'ffmpeg'

bucket_name = "xeraphys"
ACCESS_KEY = "AKIARVAPJUP55NYGZ555"
SECRET_KEY = "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"
region ="us-east-1"



def get_total_seconds(stringHMS):
    """A string repensenting the Hour, minute and second e.g 00:00:05
    """
    timedeltaObj = dt.datetime.strptime(stringHMS, "%H:%M:%S") - dt.datetime(1900,1,1)
    return timedeltaObj.total_seconds()

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


def parse_play(filename,event):
    a = pd.read_json(filename)
    start = []
    stop = []
    for i in range(len(a[event]["timeline"])):
        start.append(int(a[event]['timeline'][i].get("start_time")))
        stop.append(int(a[event]['timeline'][i].get("stop_time")))
    return start,stop

def player_event_clip(filename,event):
    start,stop = parse_play(filename,event)
    #uri = 'https://asvideo.s3.us-east-2.amazonaws.com/clip.mp4'
    vid = "vid.mp4" #place video
    clip = VideoFileClip(vid)
    clips=[]
    for i in range(len(start)):
        clips.append(clip.subclip(start[i]-2,stop[i]+2))
    final = concatenate_videoclips(clips)

    return final
    

    

def all_events(filename):
    a = pd.read_json(filename,orient="index")
    cols = a.index
    all_links = []
    for i in range(len(cols)):
        final = player_event_clip(filename,str(cols[i]))
        final.write_videofile(str(cols[i])+".mp4")
        url=upload_to_aws(str(cols[i])+".mp4", bucket_name, region)
        all_links.append(url)
    a = pd.read_json("input.json",orient='index')
    a["event_url"] = all_links
    #final_json = final_json.replace("\/","/")
    final_json = a.to_json()
    final_json=final_json.replace("\/","/")
    print(type(final_json))
    with open('readme.json', 'w') as f:
        f.write(final_json)
    
    
    print("DONE")