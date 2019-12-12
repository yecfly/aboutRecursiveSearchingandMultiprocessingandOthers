import os,sys,traceback
import glob
import cv2
import time
import dlib

FF=True
samples_count=0
undetect_count=0
detector = dlib.get_frontal_face_detector()
errorlog='./error.txt'

def searchingUnderInputDir(imagedir, filename):
    global samples_count, undetect_count
    tm=time.time()
    for v in glob.glob(os.path.join(imagedir+'/', '*.jpg')):
        try:
            samples_count=samples_count+1
            img=cv2.imread(v, cv2.IMREAD_GRAYSCALE)
            fd=detector(img, 0)
            flag=True
            if len(fd)==0:
                undetect_count=undetect_count+1
                fw=open(filename,'a')
                fw.write('%d\t%s\n'%(undetect_count,v))
                fw.close()
                flag=False
            t2=time.time()
            print('Current File:%s\tTime:%f\t%s'%(v,(t2-tm),str(flag)))
        except:
            print('ERROR in processing %s'%(v))
            ferr=open(errorlog,'a')
            ferr.write('ERROR in processing %s\n'%(v))
            traceback.print_exc()
            traceback.print_exc(file=ferr)
            ferr.close()
    flist=os.listdir(imagedir)
    for fn in flist:
        fpa=os.path.join(imagedir, fn)
        if os.path.isdir(fpa):
            searchingUnderInputDir(fpa, filename)

    t2=time.time()
    dtm=t2-tm
    print("Time comsuming %fs for %s\n"%(dtm, imagedir))

def FileList(path):
    global samples_count, undetect_count
    flist = os.listdir(path)
    for fn in flist:
        fpa = os.path.join(path, fn)
        if os.path.isdir(fpa):
            fw='%s/%s_no_face_was_detected.txt'%(path, fn)
            searchingUnderInputDir(fpa, fw)
    fsum='%s_summary.txt'%(path)
    fin=open(fsum,'w')
    fin.write('Total: %d\nUndetected: %d\nRatio: %f\n'%(samples_count, undetect_count, undetect_count/samples_count))
    fin.close()
    print('Total: %d\nUndetected: %d\nRatio: %f\n'%(samples_count, undetect_count, undetect_count/samples_count))        

if __name__=='__main__':
    t0=time.time()
    if len(sys.argv)==2:
        imagedir=str(sys.argv[1])
    else:
        imagedir='./'
    FileList(imagedir)#only need to implement once
    t1=time.time()
    print('Total Time comsumed: %fs'%(t1-t0))