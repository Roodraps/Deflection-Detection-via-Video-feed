import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from reference_calculate import ref
file_name = "rod_ref.mp4"


ref_line = ref(file_name)
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
        croped_frame=frame[120:200 , 150:300]
        resize =cv2.resize(croped_frame, (750,400))
        
        
        
        gray = cv2.cvtColor(resize,cv2.COLOR_BGR2GRAY)
        
       
        ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)
        
       
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(binary,(kernel_size, kernel_size),0)
    
    
        low_thres=50
        high_thres=150
        canny_output = cv2.Canny(blur_gray,low_thres,high_thres)
        cv2.imshow('frame',canny_output)
        
        
        thresold = 150 # The minimum number of intersections to "*detect*" a line
        min_line_length = 0  # minimum number of pixels making up a line
        max_line_gap = 0  # maximum gap in pixels between connectable line segments
        lines = cv2.HoughLines(canny_output, 1, np.pi / 180, thresold, np.array([]),
                               min_line_length,max_line_gap)
        
        resize= cv2.line(resize, ref_pt1, ref_pt2, (0,0,255), 3, cv2.LINE_AA)
        if lines is not None:
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
                lin = cv2.line(resize, pt1, pt2, (0,255,255), 3, cv2.LINE_AA)
        
            cv2.imshow('frame1',lin)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
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

print(posi_def)
print(nega_def)
        


  