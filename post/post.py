
import requests
import re

def postshuoshuo(content):
    data={
        'syn_tweet_verson':'1',
        'paramstr':'1',
        'pic_template':'',
        'richtype':'',
        'richval':'',
        'special_url':'',
        'subrichtype':'',
        'who':'1',
        'con':content,
        'feedversion':'1',
        'ver':'1',
        'ugc_right':'64',#1为所有人，64为仅自己
        'to_sign':'0',
        'hostuin':hostqqnumber,
        'code_version':'1',
        'format':'fs',
    }
    response = requests.request('POST',
                    'https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6',
                    params=params, headers=headers,cookies=cookies,data=data)
    if response.status_code == 200:
        message=re.search(r"\"tid\"\:\"(.*?)\"",response.text).group(1)
        print(message)
    else:
        return

def deleteshuoshuo(id):
    data={
        'uin': hostqqnumber,
        "topicId": hostqqnumber+"_"+id+"__1",
        "feedsType": "0",
        "feedsFlag": "0",
        "feedsKey": id,
        "feedsAppid": "311",
        "feedsTime": "1510026657",
        "fupdate": "1",
        "ref": "feeds"
    }

    response = requests.request('POST',
                    'https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_delete_v6',
                    params=params, headers=headers,cookies=cookies,data=data)
    if response.status_code==200:
        message = re.search(r"\"message\"\:\"(.*?)\"", response.text).group(1)
        print(message)
    else:
        return

def liuyan(qqnumber,content):
    data={
        'content':content,
        'hostUin':qqnumber,
        'uin':hostqqnumber,
        'format':'fs',
        'inCharset':'utf-8',
        'outCharset':'utf-8',
        'iNotice':'1',
        'ref':'qzone',
        'json':'1',
        'g_tk':g_qzonetoken,
        'qzreferrer':'https://qzs.qq.com/qzone/msgboard/msgbcanvas.html#page=1'
    }
    response = requests.request('POST',
                    'https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/add_msgb',
                    params=params, headers=headers,cookies=cookies,data=data)
    if response.status_code == 200:
        message=re.search(r"\"message\"\:\"(.*?)\"",response.text).group(1)
        print("%s" % qqnumber, message)
    else:
        return



def deleteLiuyan(qqnumber,liuyanid):
    data = {
        "idList":liuyanid,
        'hostUin': hostqqnumber,
        'uinList': qqnumber,
        'format': 'fs',
        'inCharset': 'utf-8',
        'outCharset': 'utf-8',
        'iNotice': '1',
        'ref': 'qzone',
        'json': '1',
        'g_tk': g_qzonetoken,
        'qzreferrer': 'https://qzs.qq.com/qzone/msgboard/msgbcanvas.html'
    }
    requests.request('POST',
                    'https://h5.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/del_msgb',
                    params=params, headers=headers, cookies=cookies, data=data)

if __name__=="__main__":
    from scrape import prepare
    hostqqnumber, cookies, gtk, g_qzonetoken = prepare.INFO
    params = {
        'g_tk': str(gtk),
        'qzonetoken': g_qzonetoken
    }
    headers=prepare.headers
    deleteshuoshuo("1b4bd94a94c65d5ae8080d00")

