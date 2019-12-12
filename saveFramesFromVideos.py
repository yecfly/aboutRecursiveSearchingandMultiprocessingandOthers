import os
import cv2
import time
import ntpath, shutil
import sys
from PIL import Image as IM

#### Initiate ################################
tm=time.time()


def FileList(path, avilist):
    flist = os.listdir(path)
    for fn in flist:
        fpa = os.path.join(path, fn)

        if os.path.isdir(fpa):
            FileList(fpa, avilist)

        elif os.path.isfile(fpa) and fpa.find('.avi')>-1:
            avilist.append(fpa)
        elif os.path.isfile(fpa) and fpa.find('.mp4')>-1:
            avilist.append(fpa)
            
#################

##### Prepare images ##############################
dataroot='I:/Python/Learning/data/video/'
imageroot='I:/Python/Learning/data/videoframes/'
avil=[]
FileList(dataroot,avil)#searching for avi and mp4 videos
for i, v in enumerate(avil):
    print(v)
    videoname=ntpath.basename(v).split('.')[0]
    print(videoname)
    #sid=int(videoname[1:4])
    sdir=imageroot+videoname
    if not os.path.exists(sdir):
        os.mkdir(sdir)

    vC=cv2.VideoCapture(v)
    if vC.isOpened():
        ic=1
        ft=vC.read()
        while ft[0]:
            imn='%s-%06d.jpg'%(videoname,ic)
            idir=os.path.join(sdir,imn)
            cv2.imwrite(idir,ft[1])
            ic=ic+1
            #cv2.imwrite(idir,cv2.resize(ft[1],(1280,1280)))
            #ic=ic+5
            ft=vC.read()
t2=time.time()
print("Total :%d\tTime: %f"%(i+1, (t2-tm)))

