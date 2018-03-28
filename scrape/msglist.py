import asyncio
import codecs
import json
import time

import aiohttp
import requests




class MsgList:
    """
    a class
    """

    def __init__(self, qqnumber):
        self.qqnumber = qqnumber
        self.hostqqnumber, self.cookies, self.gtk, self.g_qzonetoken = prepare.INFO
        self.headers = prepare.headers
        self.shuoshuoparams = {
            'uin': self.qqnumber,
            'ftype': '0',
            'sort': '0',
            'pos': '0',
            'num': '20',
            'replynum': '100',
            'callback': '_preloadCallback',
            'code_version': '1',
            'format': 'jsonp',
            'need_private_comment': '1',
            'g_tk': str(self.gtk),
            'qzonetoken': self.g_qzonetoken

        }
        self.likeParams = {
            'uin': self.hostqqnumber,
            'unikey': "http://user.qzone.qq.com/" + self.qqnumber + "/mood/",
            "g_tk": self.gtk,
            "qzonetoken": self.g_qzonetoken,
            'begin_uin': '0',
            'query_count': '60',
            'if_first_page': '1'
        }
        self.shuoshuolist = []
        self.count=0

    @asyncio.coroutine
    async def get_twenty_text(self, pos):
        url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6'
        self.shuoshuoparams["pos"] = str(pos)
        async with aiohttp.ClientSession(cookies=self.cookies, headers=self.headers) as session:
            async with session.get(url, params=self.shuoshuoparams) as resp:
                if resp and resp.status == 200:
                    data = await resp.text()
                    data = data.replace("_preloadCallback(", '').replace(");", '').replace("_Callback(", '')
                    return json.loads(data)
                else:
                    return

    @staticmethod
    def process_one(text):
        """
        process one shuoshuo
        """

        one = {"content": text["content"].replace("\n",""), "create_time": time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(text["created_time"])), "cmtnum": text["cmtnum"]}

        if "commentlist" in text.keys() and text["commentlist"] is not None:
            one["commentlist"]=[]
            for i in text["commentlist"]:
                comment = {"content": i["content"], "name": i["name"],"create_time": time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(i["create_time"]))}
                if "list_3" in i.keys():
                    comment["list"] = []
                    for j in i["list_3"]:
                        comment["list"].append({"content": j["content"], "create_time": time.strftime(
                            "%Y-%m-%d %H:%M:%S", time.localtime(j["create_time"])), "name": j["name"]})
                one["commentlist"].append(comment)
        return one

    def get_number(self):
        self.shuoshuoparams["pos"] = 0
        response = requests.get('https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6',
                                params=self.shuoshuoparams, headers=self.headers, cookies=self.cookies)
        if response and response.status_code == 200:
            text = response.text.replace(
                "_preloadCallback(", '').replace(");", '').replace("_Callback(", '')
            data = json.loads(text)
            print(self.qqnumber + " " + (data["message"] or "可以进入"))

            if data["message"]=="":
                return data['total']
            else:
                return 0


    def main(self):
        number = self.get_number()
        if number==0:
            print("%s 跳过" % (self.qqnumber))
            return
        event_loop = asyncio.get_event_loop()
        tasks = [self.get_twenty_text(pos * 20) for pos in range(int(number / 20) + 1)]
        results = event_loop.run_until_complete(asyncio.gather(*tasks))
        event_loop.close()
        for i in results:
            for one in i['msglist']:
                self.shuoshuolist.append(self.process_one(one))
        self.count=len(self.shuoshuolist)
        print("已完成%s的全部说说共%s个" % (self.qqnumber, self.count))



if __name__ == "__main__":
    import prepare
    start = time.clock()
    my = MsgList('1255754523')
    my.main()
    with codecs.open("temp.json", 'w', 'utf-8') as f:
        f.write(json.dumps(my.shuoshuolist, indent=2, ensure_ascii=False))
    end = time.clock()
    print("用时" + str(end - start) + " s")


# def process(text):
#     # text = re.sub(r"\[em\].*?\[\/em\]", '', text)
#     text = re.sub("\n", '', text)
#     # text = re.sub(r"@\{.*?\}", '', text)
#     return text
#     @asyncio.coroutine
#     async def get_one_like_list(self, shuoshuo):
#         self.likeParams["unikey"] = self.likeParams["unikey"] + shuoshuo["id"] + ".1"
#         url = "https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app"
#         async with aiohttp.ClientSession(cookies=self.cookies, headers=self.headers) as session:
#             async with session.get(url, params=self.likeParams) as resp:
#                 if resp and resp.status == 200:
#                     data = await resp.text()
#                     print(data)
#                     data = json.loads(data.replace("_preloadCallback(", '').replace(");", '').replace("_Callback(", ''))
#                     data = data["data"]
#                     shuoshuo["likeNumber"] = data["total_number"]
#                     shuoshuo["likes"] = []
#                     for i in data["like_uin_info"]:
#                         shuoshuo["likes"].append({"name": i["nick"], "uin": i["fuin"]})
#                     return shuoshuo
#                 else:
#                     return shuoshuo