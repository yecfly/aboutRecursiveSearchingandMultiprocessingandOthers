import os,sys,traceback,random
from multiprocessing import pool
import glob
import cv2
import time
import dlib

MAP = {'neutral':0, 'angry':1, 'surprise':2, 'disgust':3, 'fear':4, 'happy':5, 'sad':6}
samples_count=0
undetect_count=0
detector = dlib.get_frontal_face_detector()
errorlog='./error.txt'
def getLabel(path):
    label=os.path.split(path)[-1]
    print(label)
    id=MAP.get(label, None)
    if id is None:
        print('Unexpected case when mapping label')
        exit()
    return id

def searchingUnderInputDir(imagedir):
    samples_count=0
    undetect_count=0
    nl=[]
    fl=[]
    tm=time.time()
    filelist=[]
    filelist.extend(glob.glob(os.path.join(imagedir+'/', '*.jpg')))
    filelist.extend(glob.glob(os.path.join(imagedir+'/', '*.jpeg')))
    filelist.extend(glob.glob(os.path.join(imagedir+'/', '*.png')))
    for v in filelist:
        try:
            samples_count=samples_count+1
            img=cv2.imread(v, cv2.IMREAD_GRAYSCALE)
            fd=detector(img, 0)
            flag=True
            if len(fd)==0:
                undetect_count=undetect_count+1
                nl.append(v)
                #fw=open(filename,'a')
                #fw.write('%d\t%s\n'%(undetect_count,v))
                #fw.close()
                flag=False
            else:
                label=getLabel(imagedir)
                record='%s %d\n'%(v, label)
                fl.append(record)
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
            tsc=0
            tuc=0
            tsc, tuc, tnl, tfl=searchingUnderInputDir(fpa)
            samples_count=samples_count+tsc
            undetect_count=undetect_count+tuc
            nl.extend(tnl)
            fl.extend(tfl)

    t2=time.time()
    dtm=t2-tm
    print("Time comsuming %fs for %s\n"%(dtm, imagedir))
    return samples_count, undetect_count, nl, fl

def FileList(path, pp):
    global samples_count, undetect_count
    nl=[]
    fl=[]
    flist = os.listdir(path)
    par=[]
    print('Multiprocessing the list %s'%(str(flist)))
    for fn in flist:
        fpa = os.path.join(path, fn)
        if os.path.isdir(fpa):
            #fw='%s/%s_no_face_was_detected.txt'%(path, fn)
            #tsc,tuc=searchingUnderInputDir(fpa, fw)
            par.append(pp.apply_async(searchingUnderInputDir, (fpa,)))
    pp.close()
    pp.join()
    for r in par:
        tsc, tuc, tnl, tfl=r.get()
        samples_count=samples_count+tsc
        undetect_count=undetect_count+tuc
        nl.extend(tnl)
        fl.extend(tfl)

    fsum='%s_summary.txt'%(path)
    fin=open(fsum,'w')
    fin.write('Total: %d\nUndetected: %d\nRatio: %f\n'%(samples_count, undetect_count, undetect_count/samples_count))
    fin.close()
    ferr='%s_nofacedetected.txt'%(path)
    fin=open(ferr,'w')
    for v in nl:
        fin.write('%s\n'%(v))
    fin.close()
    flabel='%s_label.txt'%(path)
    fin=open(flabel,'w')
    for v in fl:
        fin.write(v)
    fin.close()
    flabel='%s_label_random.txt'%(path)
    fin=open(flabel,'w')
    random.shuffle(fl)
    for v in fl:
        fin.write(v)
    fin.close()
    print('Total: %d\nUndetected: %d\nRatio: %f\n'%(samples_count, undetect_count, undetect_count/samples_count))        

if __name__=='__main__':
    t0=time.time()
    imagedir='./V1'
    if len(sys.argv)==2:
        Pn=int(sys.argv[1])
    elif len(sys.argv)==3:
        Pn=int(sys.argv[1])
        imagedir=sys.argv[2]
    else:
        Pn=12

    pp=pool.Pool(processes=Pn)
    FileList(imagedir, pp)#only need to implement once
    t1=time.time()
    print('Total Time comsumed: %fs'%(t1-t0))