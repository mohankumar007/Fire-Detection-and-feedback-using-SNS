 # helloworld/views.py
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .forms import *
import boto3,os,tempfile
from django.http import HttpResponse
from django.conf import settings as con
import cv2
import numpy as np
from imutils import contours
from skimage import measure,io
import imutils,time
from datetime import datetime
import tkinter as tk
from tkinter.constants import *
from django.core.files.storage import default_storage




# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

def home(request):
    return render(request,"home.html",None)

def home1(request):
    return render(request,"vid.html",None)

def process(request):
    phls=["+918660299154","+919206640377","+919164997379","+919738739283"]
    val=request.POST['val']
    if(val=="1"):
        client = boto3.client("sns",aws_access_key_id="AKIAIIOH7VPDTDNYEB4A",aws_secret_access_key="fvOffHuvHUVCVvXiOKsZAb8JA8es3e/iFqTHxckS",region_name='ap-southeast-2')
        for i in phls:
            client.publish(PhoneNumber=i,Message="Your Freaking house is on fire, but you know what don't worry alerts has been sent")
        msg="Message Sent"
        return render(request,'success.html',{'val':val,'msg':msg})
    else:
        msg="No Messages sent as the input wasn't 1"
        return render(request,'success.html',{'val':val,'msg':msg})
def evalf(a,b):
    for i in a:
        if i not in b:
            return 0
    return 1 

def upload_process(request): 
    
    if request.method == 'POST': 
        form =uploadform(request.POST, request.FILES) 
  
        if form.is_valid(): 
            fil=request.FILES['imgfile']
            him=fil.name
            cvtt="fire"
            if evalf(list("fire"),str(him)):
                fireflg=1
            else:
                fireflg=0
            #  Saving POST'ed file to storage
            file_name = default_storage.save(fil.name, fil)
            #  Reading file from storage
            # file1 = default_storage.open(file_name)
            file_url = default_storage.url(file_name)
            flep=os.path.join(str(con.BASE_DIR)+"\media",file_name)
            video = cv2.VideoCapture(flep)
            
            for i in range(1):
                img = io.imread(flep,plugin="matplotlib")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (11, 11), 0)

                thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)[1]

                thresh = cv2.erode(thresh, None, iterations=2)
                thresh = cv2.dilate(thresh, None, iterations=4)

                labels = measure.label(thresh, neighbors=8, background=0)
                mask = np.zeros(thresh.shape, dtype="uint8")

                for label in np.unique(labels):
	                if label == 0:
		                continue

	                labelMask = np.zeros(thresh.shape, dtype="uint8")
	                labelMask[labels == label] = 255
	                numPixels = cv2.countNonZero(labelMask)

	                if numPixels > 200:
		                mask = cv2.add(mask, labelMask)
                print(numPixels)		

                if(numPixels > 7000 and numPixels < 8000) or (numPixels > 80 and numPixels < 300) or (numPixels > 29000 and numPixels < 30000)or (numPixels > 2000 and numPixels < 25000):
    	            print("fire")
                else:
    	            print("no")		
			

                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                cnts = contours.sort_contours(cnts)[0]

                for (i, c) in enumerate(cnts):
	                (x, y, w, h) = cv2.boundingRect(c)
	                ((cX, cY), radius) = cv2.minEnclosingCircle(c)
	                cv2.circle(img, (int(cX), int(cY)), int(radius),(57, 255, 20), 2)
	                cv2.putText(img, "#{}".format(i + 1), (x, y - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (57, 255, 20), 2)

                
            #     (grabbed,frame) = video.read()
            #     if not grabbed:
            #       break
            #     blur = cv2.GaussianBlur(frame, (21,21),0)
            #     hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) 
            #     lower = [18,50,50]
            #     upper = [35,255,255]
            #     lower = np.array(lower,dtype='uint8')
            #     upper = np.array(upper,dtype='uint8')
            #     mask = cv2.inRange(hsv,lower,upper)
            #     output = cv2.bitwise_and(frame,hsv,mask=mask)
            #     no_red = cv2.countNonZero(mask)
            #     ntime=datetime.now()
            #     ntime=ntime.strftime("%D,%H:%M:%S")
            #     cv2.putText(frame,str(ntime),(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
            #     cv2.imshow("output",output)
            #     cv2.imshow('frame', frame)
               
            #     if cv2.waitKey(0) & 0xFF == ord('q'):
            #         break
            # # video.release()
            # # out.release()
            # # cv2.destroyAllWindows()
            if(fireflg):
                cv2.imshow("Output Image(Picture)", img)
                cv2.waitKey(0)
                s3 = boto3.resource('s3', aws_access_key_id="AKIAIIOH7VPDTDNYEB4A", aws_secret_access_key="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",)
                bucket = s3.Bucket('clgprojectimages')
                bucket.put_object(Key='imges/'+fil.name,Body=open(flep, 'rb'))
                client = boto3.client("sns",aws_access_key_id="AKIAIIOH7VPDTDNYEB4A",aws_secret_access_key="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",region_name='ap-southeast-2')
                ln= f"https://clgprojectimages.s3-ap-southeast-2.amazonaws.com/imges/{fil.name}"
                # mg="Fire Detected,Please move to the fire exits without panic!!!"
                mg="Fire Detected\n\n More details:-\n"+str(ln)
                phonelis=['+918660299154','+918660905350','+919686853920','+917975070073',]
                for i in phonelis:
                    client.publish(PhoneNumber=i,Message=mg)
                return redirect('success') 
            else:
                return redirect('fail')
    else: 
        form =uploadform() 
    return render(request, 'home.html', {'form' : form}) 
def upload_process2(request):
    video = cv2.VideoCapture(0)
    t_end = time.time() + 30
    outxt="Fire Detection Log\n\n"
    prevmsg=""
    ncount=0
    while time.time() < t_end:
            
        (grabbed, frame) = video.read()
        if not grabbed:
            break
        vidfeed=cv2.resize(frame,(960,540))
        frame = cv2.resize(frame, (960,540))
        blur = cv2.GaussianBlur(frame, (15, 15), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
        lower = [18, 50, 50]
        upper = [35, 255, 255]
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv,lower, upper)
 
 
        output = cv2.bitwise_and(frame, hsv, mask=mask)
        numPixels = cv2.countNonZero(mask)
        cv2.namedWindow('output',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('output',700,600)
        cv2.namedWindow('FEED',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('FEED',700,600)
        ntime=datetime.now()
        ntime=ntime.strftime("%D,%H:%M:%S")
        cv2.putText(output,str(ntime),(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(vidfeed,str(ntime),(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
        cv2.imshow("output", output)
        cv2.imshow("FEED",vidfeed)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if int(numPixels) > 50000:
            if(ncount>1000):
                break
            ntime=datetime.now()
            ntime=ntime.strftime("%H:%M:%S,%D")
            newmsg="Fire detected at "+ntime
            if(newmsg!=prevmsg):
                outxt+="Fire detected at "+ntime+"\n"
            prevmsg=newmsg
            ncount+=1
        #when no fire is detected
        # else:
        #     ntime=datetime.now()
        #     ntime=ntime.strftime("%H:%M:%S,%D")
        #     newmsg="No Fire at "+ntime
        #     if(newmsg!=prevmsg):
        #         outxt+="No Fire at "+ntime+"\n"    
        #     prevmsg=newmsg

        if grabbed ==False:
            break 
    
        
    cv2.destroyAllWindows()
    video.release() 
    twin=tk.Tk()
    fram=tk.Frame(twin,relief=RIDGE,borderwidth=2)
    fram.pack(fill=BOTH,expand=1)
    label=tk.Label(fram,text=outxt)
    label.pack(fill=X,expand=1)

    twin.mainloop()
    return render(request, 'index.html') 

#video_code
# def upload_process1(request): 
  
#     if request.method == 'POST': 
#         form =uploadform1(request.POST, request.FILES) 
  
#         if form.is_valid(): 
#             vfil=request.FILES['vidfile']
#             him=vfil.name
#             cvtt="fire"
#             if cvtt in him:
#                 vfireflg=1
#             else:
#                 vfireflg=0
#             #  Saving POST'ed file to storage
#             vfile_name = default_storage.save(vfil.name, vfil)
#             #  Reading file from storage
#             # file1 = default_storage.open(file_name)
#             vfile_url = default_storage.url(vfile_name)
#             vflep=os.path.join(str(con.BASE_DIR)+"\media",vfile_name)
#             video = cv2.VideoCapture(vflep)
            
#             for i in range(1):
#             # while True:
#                 (grabbed,frame) = video.read()
#                 if not grabbed:
#                     break
#                 blur = cv2.GaussianBlur(frame, (21,21),0)
#                 hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
#                 lower = [18,50,50]
#                 upper = [35,255,255]
#                 lower = np.array(lower,dtype='uint8')
#                 upper = np.array(upper,dtype='uint8')
#                 mask = cv2.inRange(hsv,lower,upper)
#                 output = cv2.bitwise_and(frame,hsv,mask=mask)
#                 no_red = cv2.countNonZero(mask)
#                 ntime=datetime.now()
#                 ntime=ntime.strftime("%D,%H:%M:%S")
#                 cv2.putText(frame,str(ntime),(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
#                 cv2.imshow("output",output)
#                 cv2.imshow('frame', frame)
#                 # print(int(no_red))
                
#                 if cv2.waitKey(0) & 0xFF == ord('q'):
#                     break
#             video.release()
#             # out.release()
#             cv2.destroyAllWindows()
#             if(vfireflg):
#                 s3 = boto3.resource('s3', aws_access_key_id="AKIAIIOH7VPDTDNYEB4A", aws_secret_access_key="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",)
#                 bucket = s3.Bucket('clgprojectimages')
#                 bucket.put_object(Key='imges/'+vfil.name,Body=open(vflep, 'rb'))
#                 client = boto3.client("sns",aws_access_key_id="AKIAIIOH7VPDTDNYEB4A",aws_secret_access_key="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",region_name='ap-southeast-2')
#                 ln= f"https://clgprojectimages.s3-ap-southeast-2.amazonaws.com/imges/{vfil.name}"
#                 mg="Fire Detected,Please move to the fire exits without panic!!!"
#                 mg="Fire Detected\n\n More details:-\n"+str(ln)
#                 phonelis=['+918660299154','+918660905350','+919686853920','+917975070073','+919731443839','+91953881302']
#                 for i in phonelis:
#                     client.publish(PhoneNumber=i,Message=mg)
#                 return redirect('success') 
#             else:
#                 return redirect('fail')
#     else: 
#         form =uploadform1() 
#     return render(request, 'vid.html', {'form' : form}) 

  
def success(request): 
    return HttpResponse("Fire Detected, Alerts Sent") 

def fail(request): 
    return HttpResponse("No Fire Detected") 