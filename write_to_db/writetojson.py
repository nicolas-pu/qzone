
import codecs
import json
import time
from multiprocessing import Pool
from scrape.msglist import MsgList


count=0
def run(qqnumber,realname):
    one=MsgList(qqnumber)
    one.main()
    return (one.count,qqnumber,realname,one.shuoshuolist)

def callback(args):
    global count
    icount,qqnumber,realname,shuoshuolist=args
    count+=icount
    with codecs.open("C:\\Personal Files\\projects\\qzone\\shuoshuo\\"+qqnumber+'#'+realname+".json",'w','utf-8') as f:
        f.write(json.dumps(shuoshuolist,sort_keys=True, indent=4,ensure_ascii=False))
    print(qqnumber+' '+realname+" 写入完成")

if __name__=="__main__":
    from scrape import prepare
    start = time.clock()
    friendlist=prepare.FriendList
    pool = Pool()
    for i in friendlist:
        pool.apply_async(run, (i,friendlist[i]),callback=callback)
    pool.close()
    pool.join()
    print("get %s shuoshuos from all friends"%count)
    end = time.clock()
    print("用时"+str(end-start)+" s")
