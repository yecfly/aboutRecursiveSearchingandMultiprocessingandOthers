import os,sys,traceback,shutil
from multiprocessing import pool
import glob
import time

samples_count=0
dest_dir='./front_regroup/'
dest_dir_sub='./front_regroup_subfolder/'
errorlog='./error.txt'
MAPPING = {'neutral':'NE', 'angry':'AN', 'surprise':'SU', 'disgust':'DI', 'fear':'FE', 'happy':'HA', 'sad':'SA'}
RMAP= {'NE':0, 'AN':1, 'SU':2, 'DI':3, 'FE':4, 'HA':5, 'SA':6}

SubFolder=False
ONEFRAME=True

def getPIDandE(path):#path must follow.the style of {./front}/{1}/{angry}
    b1, emotionid=os.path.split(path)
    personid=int(os.path.split(b1)[-1])
    return personid, emotionid
def getEmotionFromFilename(filename):
    name=os.path.basename(filename)
    emotion=RMAP.get(name.split('_')[1])
    return emotion

def searchingUnderInputDir(imagedir):
    samples_count=0
    nl=[]
    tm=time.time()
    tnl=glob.glob(os.path.join(imagedir+'/', '*.jpg'))
    tsc=len(tnl)
    if tsc>0:
        samples_count=samples_count+tsc
        print('###Tracking 1 %s'%(imagedir))
        #return 0, 0
        b=sorted(tnl, key = lambda d:int(d.split(imagedir+os.path.sep)[-1].split('.jpg')[0]))
        pid,eid =getPIDandE(imagedir)
        if SubFolder:
            newdir=dest_dir_sub+eid+'/P%03d/'%(pid)
        else:
            newdir=dest_dir+eid+'/'
        if ONEFRAME:
            newdir=newdir.replace('./front_regroup','./front_regroup_oneframe')
        if not os.path.exists(newdir):
            try:
                os.makedirs(newdir)
            except:
                traceback.print_exc()
        for id, v in enumerate(b):
            newfilename=newdir+'P%03d_%s_%02d.jpg'%(pid, MAPPING.get(eid), id+1)
            if ONEFRAME:
                if id==3:
                    #shutil.copyfile(v,newfilename)
                    nl.append(newfilename)
            else:
                #shutil.copyfile(v,newfilename)
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

    if SubFolder:
        fsum='%s_subfolder_file_list.txt'%(path)
    else:
        fsum='%s_file_list.txt'%(path)
    if ONEFRAME:
        fsum=fsum.replace('.txt','_oneframe.txt')
    fin=open(fsum,'w')
    for filename in nl:
        em=getEmotionFromFilename(filename)
        fin.write('%s\t%d\n'%(filename, em))
    fin.close()
    print('Total: %d\n'%(samples_count))        

if __name__=='__main__':
    t0=time.time()
    imagedir='./front'
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