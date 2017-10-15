import getmsglist
import json
import codecs
from getQQFriendList import getQQFriendList
from multiprocessing import Pool, Queue
from getmsglist import GetMsgList
import multiprocessing
import time
import os 

count=0
def getFriendList(friendlistUrl):
    if os.path.exists(friendlistUrl):
        with codecs.open(friendlistUrl,'r','utf-8') as f:
            friendlist = json.loads(f.read())
        print("get QQFriendList successful")
    else:
        friendlist=getQQFriendList(friendlistUrl)
    return friendlist

def run(qqnumber,realname):

    one=GetMsgList(qqnumber)
    one.main()
    return (one.count,qqnumber,realname,one.shuoshuolist)

def callback(args):
    global count
    icount,qqnumber,realname,shuoshuolist=args
    count+=icount
    with codecs.open("E:\\myfiles\\program\\project\\qzone\\说说\\"+qqnumber+'#'+realname+".json",'w','utf-8') as f:
        f.write(json.dumps(shuoshuolist,sort_keys=True, indent=4,ensure_ascii=False))
    print(qqnumber+' '+realname+" over")


if __name__=="__main__":
    start = time.clock()
    friendlistUrl="friendlist.json"
    friendlist=getFriendList(friendlistUrl)
    one=GetMsgList("1255754523")
    one.main()
    pool = Pool()
    for i in friendlist:
        pool.apply_async(run, (i,friendlist[i]),callback=callback)
    pool.close()
    pool.join()
    print("get %s shuoshuos from all friends"%count)
    end = time.clock()
    print("用时"+str(end-start)+" s")
