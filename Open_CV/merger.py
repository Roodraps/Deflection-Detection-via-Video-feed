import time
# import cv2
import pandas as pd
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "fYS_1yXjhlhpq2csSs6VKaCVW6yqaAkw7abu5j0tF2iC5tc6Ma4WSCdqau5wAO0DnVihzd9zHU2z2rEr3B9YdQ=="
org = "iit bhilai"
bucket = "suraj"
data =pd.read_csv('data.csv')
print(data.head())
# def check(df):
print(data.size)

i=0
while(True):
    data=pd.read_csv('data.csv')
    if data.shape[0]>i:
        print(data.size, end = ' - ')
        deflection=data.iloc[i-1,1]
        frames=data.iloc[i-1,0]
        time_stamp=data.iloc[i-1,2]
        data_req="video_frames Deflection=" + str(deflection) + ",Frames=" + str(frames)+' '+ str(time_stamp)
        print(data_req)     
        with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
        
            write_api.write(bucket, org, data_req)
        i+=1

    else:      
        time.sleep(0.5)
