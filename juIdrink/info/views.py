 # -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,HttpResponse
from django.core import serializers #json serialize
from info.models import Store_Info
import sys,re
# import requests
import operator,math,json



def index(req):    
    return render(req,'index.html') 

def search(req):        
    return render(req,'search.html') 


def store(req):
    store_tuples = Store_Info.product

    dic = {}
    for identifier, friendly_name in store_tuples:
        dic[friendly_name] = Store_Info.objects.filter(store=identifier).count()

    asd={}
    all_Store = Store_Info.objects.all().order_by("store")
    for key,value in sorted(dic.iteritems(),key=lambda(k,v):(v,k),reverse=True):    
        # print"%s: %s"%(key,value)
        asd[key] =value

    return render(req,'store.html', dict(
        msg=asd, all_Store=all_Store, store_tuples=store_tuples))



def locate(req):
    data=""
    if req.is_ajax():
        zipcode = req.POST['zipcode']
        info = Store_Info.objects.filter(other=(zipcode)).order_by('store')
        infos = serializers.serialize('json', info)
        data = json.dumps({
            'data': infos
        })
    return HttpResponse(data, content_type='application/json')




"""
def p_other(req):
    # p_list =["dayungs","orange","chingshin","teaplus","c-cup","presotea","sadou","coco","comebuy","kingtea","teapatea","teamagichand"]
    for product in p_list:
        data = readSource('info/grouth/'+product+'.txt')
        li_com=re.compile('<li>.*?</b><br><b>(.*?)</b>.*?tel"><b>(.*?)</b>.*?add"><b>(.*?)</b><br></span></li>')
         li =li_com.findall(data)
         for msg in li :
             p=Store_Info(
                store=product,
                store_name=msg[0],
                city='',
                phone=msg[1],
                address=msg[2],
            ).save()
             print msg[0]
             print msg[1]
    context= {'zxc':data}
    return render(req,'index.html',context)

def readSource(fileUrl):
    serialize_data =""
    with open(fileUrl, 'r') as f:
        for line in f:
            serialize_data +=line.replace("\n","").replace("\t","")
    return serialize_data


def p_50lan(req):
    data = readSource('info/grouth/50lan.txt')
    li_com=re.compile('<li>.*?name\">(.*?)<br>(.*?)</a>.*?tel\">(.*?)</span>.*?add\">(.*?)</span> </li>')
    
     li =li_com.findall(data)
     for msg in li :
         p=Store_Info(
            store='50lan',
            store_name=msg[1],
            city='',
            # zone='中山區',
            phone=msg[2],
            address=msg[3],
        ).save()
    context = {'msg':li}
    return render(req,'index.html',context)

def findCoordinate(obj):
    print obj,obj.address.encode("utf-8", "ignore")
    try:
        url = "http://maps.google.com/maps/api/geocode/json?address="+obj.address
        reponse = requests.get(url)
        json = reponse.json()
        coordinate = json['results'][0]['geometry']['location']
        x = coordinate['lat']
        y = coordinate['lng']
        print x,y
        obj.location = str(x)+","+str(y)
        obj.save()
    except:
        return

def findZone(obj):
    url = "http://maps.google.com/maps/api/geocode/json?latlng="+obj.location+"&sensor"+"true_or_false&language=zh-TW"
    print url
    reponse = requests.get(url)
    json = reponse.json()
    zipcode = json['results'][0]['address_components'][5]['long_name']
    print str(zipcode)
    print unicode(zipcode)
    print zipcode
    obj.other = zipcode
    obj.save()

"""
