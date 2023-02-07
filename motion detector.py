import cv2 as cv,time,pandas as p
from datetime import datetime
static_back=None
#list when any motion happens
motion_list=[None,None]
#time of movemewnt
time=[]
#two columns for start and endtime
df=p.DataFrame(columns=["Start","End"])
#video capture
vid=cv.VideoCapture(0)
#ifinite while loop for images to become video
while True:
    #read frame from video
    check,frame=vid.read()
    #initializing motion as 0 for no motion
    motion=0
    #colour to grayscale
    gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    #grayscale to gaussianblur(easy change)
    gray=cv.GaussianBlur(gray,(21,21),0)
    #first iteration assign value of static back to first frame
    if static_back is None:
        static_back=gray
        continue
    #diff b/w static background with current frame(gaussianblur)
    diff_frame=cv.absdiff(static_back,gray)
    #if diff greater than 30 show white colour(255)
    thresh_frame=cv.threshold(diff_frame,30,255,cv.THRESH_BINARY)[1]
    thresh_frame=cv.dilate(thresh_frame,None,iterations=2)
    #contours of moving object
    counts,_=cv.findContours(thresh_frame.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    for contour in counts:
        if cv.contourArea(contour)<1000000:
            continue
        motion=1
        
        (x.y,w,h)=cv.boundingRect(contour)
        #making rectangle around movinbg object
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    #changing status of motion
    motion_list.append(motion)
    motion_list=motion_list[-2:]
    #appending start time of motion
    if motion_list[-1]==1 and motion_list==0:
        time.append(datetime.now())
    #appending end time of motion
    if motion_list[-1]==0 and motion_list[-2]==1:
        time.append(datetime.now())
    #display in grayscale
    cv.imshow("GrayFrame",gray)
    #display diff current frame to static frame
    cv.imshow("DiffFrame",diff_frame)
    #display black and white in which intensity duiff more than 30(pixels will appear white)
    cv.imshow("ThresholdFrame",thresh_frame)
    #display colour frame with contour
    cv.imshow("ColourFrame",frame)
    key=cv.waitKey(1)
    #if s entered process stops
    if key==ord("s"):
        #if something moving then append end time
        if motion==1:
            time.append(datetime.now())
        break
for i in range(0,len(time),2):
    df=df.append({"Start":time[i],"End":time[i+1]},ignore_index=True)
#creating csv file fot time of movements
df.to_csv("Timeofmovements.csv")
vid.release()
cv.destroyAllWindows()


        



        
