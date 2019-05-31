import requests
import random
import json
import time
import pymysql
import threading

NULL=0
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
et=0
tfp=open('tmp.txt','r')
bp=tfp.readline()
id=int(bp)+1
tfp.close()
efp=open('err.txt','a')
while 1:
    try:
        m=requests.get('https://api.bilibili.com/x/space/acc/info?mid='+str(id)+'&jsonp=jsonp')         #此api可获取用户基本信息
        f=requests.get('https://api.bilibili.com/x/relation/stat?vmid='+str(id))                         #此api可获取用户关注和粉丝信息  
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
        tfp=open('tmp.txt','w')
        tfp.write(str(id)+'\n')
        tfp.close()
        et=0
        print(str(id)+' success')
    except:
        if mdata['code']==-404:             #若该用户不存在，code值为-404
            cursor.execute(submit,(id,"NOT EXIST",NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL))
            db.commit()
            tfp=open('tmp.txt','w')
            tfp.write(str(id)+'\n')
            tfp.close()
            et=0
            print("ERR:"+str(id)+"\tNOT EXIST")
        else:
            if et<5:
                et=et+1
                print("ERR:"+str(id)+"\tERROR\tTRY:"+str(et))
                id=id-1
            else:
                print("skip "+str(id))
                efp.write(str(id)+'\n')
                efp.flush()
                et=0
    id=id+1
    time.sleep(t)
efp.close()
    


