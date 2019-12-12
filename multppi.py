from multiprocessing import pool
import numpy as np
import random, os
def func(id,list):#accept a argment for tracking
    cnt=0
    N=1000000#Test a smaller number first. When it works, change it to a bigger number.
    print('Starting at process %d with pid %d'%(id, os.getpid()))#print a state, it's good for tracking.
    for i in range(N):
        x=random.uniform(0,1)
        y=random.uniform(0,1)
        if (x*x+y*y)<1:
            cnt+=1
        vPi=4.0*cnt/N
    print('End process %d with pid %d and return the estimated value %.16f'%(id,os.getpid(),vPi))
    list.append(vPi)
    return vPi

if __name__=='__main__':
    Num=4#use a variable for a constant parameter, so you can change the value easily.
    pool_instance=pool.Pool(processes=Num)##creat processeses, replace 4 with Num
    result=[]
    list=[]
    for i in range(Num):#you should call the func for every processes, replace 3 with Num
        #msg="hello %d"%(i)
        result.append(pool_instance.apply_async(func,(i,list,)))
    
    pool_instance.close()
    pool_instance.join()
    print('The returned objects type is %s'%(str(type(result[0]))))#the return object is not a value, but an 'ApplyResult' object
    pi=0
    for res in result:####need to iterate the result for every ApplyResult object returned
        pi=pi+res.get()###need to call 'get()' function to get the value from ApplyResult object
    pi=pi/Num###get a mean value
    print('the result of estimation for pi is: %.18f'%(pi))
    print(list)