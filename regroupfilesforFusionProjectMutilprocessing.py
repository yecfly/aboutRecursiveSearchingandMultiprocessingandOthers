import os,sys,traceback,shutil
from multiprocessing import pool
import glob
import time

samples_count=0
dest_dir='./V2/'
errorlog='./error.txt'
MAPPING = {'neutral':'NE', 'angry':'AN', 'surprise':'SU', 'disgust':'DI', 'fear':'FE', 'happy':'HA', 'sad':'SA'}
MAPTOINT = {'neutral':0, 'angry':1, 'surprise':2, 'disgust':3, 'fear':4, 'happy':5, 'sad':6}
RMAP= {'NE':0, 'AN':1, 'SU':2, 'DI':3, 'FE':4, 'HA':5, 'SA':6, 'AF':4}
MAP = {0:'neutral', 1:'angry', 2:'surprise', 3:'disgust', 4:'fear', 5:'happy', 6:'sad'}

def getPIDandE(path):#path must follow.the style of {./front}/{1}/{angry}
    b1, emotionid=os.path.split(path)
    personid=int(os.path.split(b1)[-1])
    return personid, emotionid
def getEmotionFromFilename(filename):
    ###function designed to return emotions for images in KDEF and JAFFE datasets
    name=os.path.basename(filename)
    tag=name[4:6]
    emotion=RMAP.get(tag)
    if emotion is None:
        tag=name[3:5]
        emotion=RMAP.get(tag)
        if emotion is None:
            print('Unexpected case occur for %s.'%(filename))
    return emotion
def getEmotionFromDirname(filename):
    name=os.path.dirname(filename)
    tag=os.path.split(name)[-1]
    emotion=MAPTOINT.get(tag)
    if emotion is None:
        print('Unexpected case ocurr in getEmotionFromDirname')
        exit()
    return emotion

def searchingUnderInputDir(imagedir):
    ####searching under folders with multilabel files
    ####and remove the files into a new folder defined in dest_dir
    samples_count=0
    nl=[]
    tm=time.time()
    tnl=[]
    tnl.extend(glob.glob(os.path.join(imagedir+'/', '*.jpg')))
    tnl.extend(glob.glob(os.path.join(imagedir+'/', '*.JPG')))
    tnl.extend(glob.glob(os.path.join(imagedir+'/', '*.tiff')))
    tsc=len(tnl)
    if tsc>0:
        samples_count=samples_count+tsc
        print('###Tracking 1 %s'%(imagedir))
        for id, v in enumerate(tnl):
            em=getEmotionFromFilename(v)
            newfilename=dest_dir+MAP.get(em)+'/'
            if not os.path.exists(newfilename):
                os.makedirs(newfilename)
            newfilename=newfilename+os.path.basename(v)
            os.rename(v, newfilename)
            nl.append(newfilename)
    flist=os.listdir(imagedir)
    for fn in flist:
        fpa=os.path.join(imagedir, fn)
        if os.path.isdir(fpa):
            tsc=0
            tnl=[]
            tsc, tnl=searchingUnderInputDir(fpa)
            samples_count=samples_count+tsc
            nl.extend(tnl)

    t2=time.time()
    dtm=t2-tm
    print("Time comsuming %fs for %s\n"%(dtm, imagedir))
    return samples_count, nl

def FileList(path, pp):
    global samples_count
    nl=[]
    flist = os.listdir(path)
    par=[]
    print('Multiprocessing the list %s'%(str(flist)))
    for fn in flist:
        #fpa = os.path.join(path, fn)
        fpa = os.path.join(path, fn)
        fpa = os.path.normpath(fpa)
        if os.path.isdir(fpa):
            par.append(pp.apply_async(searchingUnderInputDir, (fpa,)))
    pp.close()
    pp.join()
    for r in par:
        tsc, tnl=r.get()
        samples_count=samples_count+tsc
        nl.extend(tnl)

    fsum='%s_file_list.txt'%(path)
    fin=open(fsum,'w')
    for filename in nl:
        em=getEmotionFromDirname(filename)
        fin.write('%s\t%d\n'%(filename, em))
    fin.close()
    print('Total: %d\n'%(samples_count))        

if __name__=='__main__':
    t0=time.time()
    imagedir='./KDEF_G'
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