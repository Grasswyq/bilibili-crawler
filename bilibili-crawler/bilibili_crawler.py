import requests
import random
import json
import time
import pymysql

config={
    "host":"127.0.0.1",
    "user":"root",
    "password":"g9.5Ls9.23&heart",
    "database":"bilibili_users"
    }
db=pymysql.connect(**config)
cursor=db.cursor()
submit="INSERT INTO users_info(ID,name,sex,sign,vtype,vstatus,level,birthday,following,follower) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
t=0.1
id=4974
sfp=open('K:\\test\\data.txt','w')
efp=open('err.txt','w')
while 1:
    m=requests.get('https://api.bilibili.com/x/space/acc/info?mid='+str(id)+'&jsonp=jsonp')         #此api可获取用户基本信息
    f=requests.get('https://api.bilibili.com/x/relation/stat?vmid='+str(id))                         #此api可获取用户关注和粉丝信息
    try:
        mdata=json.loads(m.text)
        mdict=mdata['data']
        name=mdict['name']                  #用户名
        sex=mdict['sex']                    #性别
        sign=mdict['sign']                  #个性签名
        level=mdict['level']                #等级
        birthday=mdict['birthday']          #生日
        mdict=mdict['vip']                  
        vtype=mdict['type']                 #大会员为 type=1 status=1 年度大会员为 type=2 status =1
        vstatus=mdict['status']             #非会员为 type=1 status=0
        fdata=json.loads(f.text)
        fdict=fdata['data']
        following=fdict['following']        #关注数
        follower=fdict['follower']          #粉丝数
        cursor.execute(submit,(id,name,sex,sign,vtype,vstatus,level,birthday,following,follower))
        db.commit()
        sfp.write(str(id)+'\n')
        sfb.flush()
        print(str(id)+' success')
    except:
        print("ERR:读取id="+str(id)+"失败")
        efp.write(str(id)+'\n')
        efp.flush()
        print(str(id)+' error')
    if id==200000:
        break
    id=id+1
    #time.sleep(t)
sfb.close()
efp.close()
    


