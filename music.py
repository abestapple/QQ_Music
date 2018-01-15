#__*__ encoding:utf-8 __*__
import requests,time
from json import loads,dumps
from fake_useragent import UserAgent
from database import Music,db
headers={"User-Agent":UserAgent().chrome}
url="https://c.y.qq.com/v8/fcg-bin/v8.fcg?channel=singer&page=list&key=cn_woman_all&pagesize=100&pagenum=1&g_tk=5381&jsonpCallback=GetSingerListCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
res=requests.get(url,headers=headers)
res.encoding="utf-8"
data=res.text
data2=data.split("GetSingerListCallback")[1]
# data3=(data2.split("(",1)[1]).split(")")[0]
data3=data2[1:-1]
data4=loads(data3)
data5=data4["data"]["list"]
Fsinger_mid=list(map(lambda x:x["Fsinger_mid"],data5))
# https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=5381&jsonpCallback=MusicJsonCallbacksinger_track&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid=001fNHEf1SFEFN&order=listen&begin=0&num=30&songstatus=1
a=0
max=0
min=0

for i in Fsinger_mid:
    try:
        url="https://c.y.qq.com/v8/fcg-bin/fcg_v8_singer_track_cp.fcg?g_tk=5381&jsonpCallback=MusicJsonCallbacksinger_track&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&singermid=%s&order=listen&begin=0&num=30&songstatus=1"%i
        res = requests.get(url, headers=headers)
        res.encoding = "utf-8"
        data = res.text
        data2 = data.split("MusicJsonCallbacksinger_track")[1]
        # data3=dumps(data2)
        # print (loads(data3)[1:-1])
        #获取歌的id
        for j in loads(data2[1:-1])["data"]["list"]:
            try:
                url="https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=%s&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"%(j["musicData"]["songid"])
                songmid=j["musicData"]["songmid"] #获取songmid
                headers = {"User-Agent": UserAgent().chrome,"referer":"https://y.qq.com/n/yqq/song/{}.html".format(songmid)}
                res = requests.get(url, headers=headers)
                res.encoding = "utf-8"
                data = res.text
                #歌词
                singer_name=j["musicData"]["singer"][0]["name"]
                album_name=j["musicData"]["albumname"]
                song_name=j["musicData"]["songname"]
                irics=loads(data.split("jsonp1")[1][1:-1])["lyric"]
                list=Music(singer_name=singer_name,song_name=song_name,album_name=album_name,irics=irics)
                db.session.add(list)
                db.session.commit()
                a+=1
                print ("完成了%s"%a)

            except:
                min+=1
                print("min=%s"%min)

    except:
        max+=1
        print("max=%s"%max)
    finally:
        time.sleep(2)
print ("全部完成!!!!")
    # https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=7168586&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0
    # https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=1530858&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0


