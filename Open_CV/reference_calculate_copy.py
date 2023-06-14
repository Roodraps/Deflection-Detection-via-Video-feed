
import cv2
import math
import numpy as np
#file_name = "rod1_4sec.mp4"
def ref(file_name):
    cap = cv2.VideoCapture(file_name)
    moving_lines = []
    while (cap.isOpened()):
        
        ret, frame = cap.read()
        if ret ==True:
            croped_frame = frame[780:900 , 950:1300]
            #resize =cv2.resize(croped_frame, (750,400))
            gray = cv2.cvtColor(croped_frame,cv2.COLOR_BGR2GRAY)
            
           
            ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)
            
           
            kernel_size = 5
            blur_gray = cv2.GaussianBlur(binary,(kernel_size, kernel_size),0)
        
        
            low_thres=50
            high_thres=150
            canny_output = cv2.Canny(blur_gray,low_thres,high_thres)
            #cv2.imshow('frame',canny_output)
            
            
            thresold = 180 # The minimum number of intersections to "*detect*" a line
            min_line_length = 0  # minimum number of pixels making up a line
            max_line_gap = 0  # maximum gap in pixels between connectable line segments
            lines = cv2.HoughLines(canny_output, 1, np.pi / 180, thresold, np.array([]),
                                   min_line_length,max_line_gap)
            
            
            if lines is not None:
                moving_lines.append(lines)
                
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break
    
    cap.release()
    cv2.destroyAllWindows()


    lines = 0
    ref_line = 0
    count = 0
    for lines_frame in moving_lines:
        if len(lines_frame)==2:
            #print(lines_frame)
            count = count + 1
            lines = lines + lines_frame
    for line in lines:
        ref_line = ref_line + line 
        
    
    return ref_line/(2*count)
