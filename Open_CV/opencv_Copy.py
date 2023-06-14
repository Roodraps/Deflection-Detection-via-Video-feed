import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
from reference_calculate_copy import ref
import time
import pandas as pd
from datetime import datetime
# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS
field_names =['Frames', 'Deflection','time_stamp']

with open('data.csv','w') as csv_file:
    csv_writer = csv.DictWriter(csv_file,fieldnames = field_names)
    csv_writer.writeheader()



file_name = "rod.mp4"
ref_file = "rod_ref.mp4"

ref_line = ref(ref_file)
print(ref_line)
ref_rho = ref_line[0][0]
ref_theta = ref_line[0][1]
ref_a = math.cos(ref_theta)
ref_b = math.sin(ref_theta)
ref_x0 = ref_a * ref_rho
ref_y0 = ref_b * ref_rho
ref_pt1 = (int(ref_x0 + 1000*(-ref_b)), int(ref_y0 + 1000*(ref_a)))
ref_pt2 = (int(ref_x0 - 1000*(-ref_b)), int(ref_y0 - 1000*(ref_a)))


deflection = []
frame_count = 0
frames =[]
cap = cv2.VideoCapture(file_name)



while (cap.isOpened()):
    
    ret, frame = cap.read()
    if ret ==True:
        frame_count = frame_count + 1
        croped_frame=frame[780:900 , 950:1300]
        #resize =cv2.resize(croped_frame, (750,400))
        
        
        
        gray = cv2.cvtColor(croped_frame,cv2.COLOR_BGR2GRAY)
        
       
        ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)
        
       
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(binary,(kernel_size, kernel_size),0)
    
    
        low_thres=50
        high_thres=150
        canny_output = cv2.Canny(blur_gray,low_thres,high_thres)
       # cv2.imshow('frame',canny_output)
        
        
        thresold = 150 # The minimum number of intersections to "*detect*" a line
        min_line_length = 0  # minimum number of pixels making up a line
        max_line_gap = 0  # maximum gap in pixels between connectable line segments
        lines = cv2.HoughLines(canny_output, 1, np.pi / 180, thresold, np.array([]),
                               min_line_length,max_line_gap)
        
        #resize= cv2.line(resize, ref_pt1, ref_pt2, (0,0,255), 3, cv2.LINE_AA)
        if lines is not None and len(lines) >= 2:
            croped_frame = cv2.line(croped_frame, ref_pt1, ref_pt2, (0,0,255), 3, cv2.LINE_AA)
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                deflection.append(rho-ref_rho)
                frames.append(frame_count)
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                lin = cv2.line(croped_frame, pt1, pt2, (0,255,255), 3, cv2.LINE_AA)
                
                with open('data.csv','a') as csv_file:
                    deflec=rho-ref_rho
                    csv_writer = csv.DictWriter(csv_file,fieldnames = field_names)
                    info = {
                    'Frames': frame_count ,
                    'Deflection': deflec,
                    'time_stamp':int(time.time()*1e9)
                    }
                    csv_writer.writerow(info)
                
                
        # else:
        #     lin = croped_frame
        #     with open('data.csv','a') as csv_file:
        #             deflec=0
        #             csv_writer = csv.DictWriter(csv_file,fieldnames = field_names)
        #             info = {
        #             'Frames': frame_count ,
        #             'Deflection': deflec
        #             }
        #             csv_writer.writerow(info)
       
        #cv2.imshow('frame1',lin)
        
              
        if cv2.waitKey(33) & 0xFF == ord('q'):
                break
    else:
        break
    
    
cap.release()
cv2.destroyAllWindows()

posi_def = []      
posi_frames =[]  
nega_def = []
nega_frames = []
for i in range(0,len(deflection)):
    if deflection[i] >= 0:
        posi_def.append(deflection[i])
        posi_frames.append(frames[i])
    else:
        nega_def.append(deflection[i])
        nega_frames.append(frames[i])
        
        
        
        
plt.plot(posi_frames,posi_def, label='positive def')
plt.plot(nega_frames,nega_def,label='negative def')
plt.xlabel('Frames')
plt.ylabel('Deflection from reference')
plt.legend()
plt.show()

        


  