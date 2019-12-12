import random, time
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0:
    print('蒙特卡洛方法实现计算圆周率')
    data = int(input("请输入你要每个进程投多少个飞镖:\n"))
    t1=time.time()
    print("进程{}广播{}数据量给其他进程".format(rank, data))
data = comm.bcast(data if rank == 0 else None, root=0)
incount = 0
i=0
while i < data:
    x = random.random()
    y = random.random()
    if (x**2 + y**2) < 1:
        incount+=1
    i+=1
sum = comm.reduce(incount, root=0,op=MPI.SUM)
if sum!=None:
   print('规约得到总命中数{}'.format(sum))
   s=(sum*4.0/data/size)
   print('PI=')
   print('%.15f'%(s))
   t2=time.time()
   print('Time used: %fs'%(t2-t1))