import getmsglist
import json
import codecs

qzoneCookieUrl="qzoneCookie.txt"
with codecs.open("friendlist.json",'r','utf-8') as f:
    friendlist = json.loads(f.read())
frienddict={}
for i in friendlist['data']:
    if i != "activity":
        frienddict[i]=friendlist['data'][i]['realname']
#print(frienddict)
shuoshuodict={}
count=0
for qqnumber in frienddict:
    realname=frienddict[qqnumber]
    shuoshuolist,icount=getmsglist.main(qqnumber,qzoneCookieUrl)
    shuoshuodict[qqnumber+" "+realname]=shuoshuolist
    count=count+icount
print("获得好友列表总共%s条说说"%count)
with codecs.open('shuoshuoqian20.json','w','utf-8') as f:
    f.write(json.dumps(shuoshuodict,sort_keys=True, indent=4,ensure_ascii=False))