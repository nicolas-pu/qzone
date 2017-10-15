import getmsglist
import pymysql

def connecttodb(dbname):
    db = pymysql.connect("localhost","root","situmaimessql",dbname,use_unicode=True, charset="utf8")
    cursor=db.cursor()
    createsql='''
    drop table if exists shuoshuo;
    create table shuoshuo(
    id int(4) not null primary key auto_increment,
    qqnumber char(10),
    qqrealname char(20),
    content text,
    created_time datetime,
    comment text,
    commentnum varchar(255),
    TransferredContent TEXT
    )
    '''
    cursor.execute(createsql)
    return db
def insert(db,shuoshuolist):
    cursor=db.cursor()
    insersql="""
    insert into shuoshuo(qqnumber,qqrealname,content,created_time,comment,commentnum,TransferredContent)\
    values('%s', '%s', '%s', '%s', '%s','%s','%s')
    """
    for i in getmsglist.main("1255754523","info.txt")[0]:
        cursor.execute(insersql % ("1255754523",
        '我',
        i["content"],
        i["created_time"],
        i['commentlist'],
        i['cmtnum'],
        i["TranferredContent"]))
    db.commit()
    db.close



if __name__=="__main__":
    db=connecttodb("shuoshuo")
    insert(db,getmsglist.main("1255754523","info.txt")[0])