 # -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,HttpResponse
from BeautifulSoup import BeautifulSoup
from info.models import Store_Info
import sys,requests,re
import operator
"""
def index(req):
	printstore =Store_Info.objects.filter(location="").count()
	for p in store:
		if not p.location:
			findCoordinate(p)

	context= {'msg':"succesuccessss",'all_Store':"success"}
	return render(req,'index.html',context)

"""
def index(req):
	dic={}
	dic['50嵐'] = Store_Info.objects.filter(store="50lan").count()
	dic['大苑子'] = Store_Info.objects.filter(store="dayungs").count()
	dic['橘子工坊'] = Store_Info.objects.filter(store="orangetea").count()
	dic['清心福全'] = Store_Info.objects.filter(store="chingshin").count()
	dic['C-cup'] = Store_Info.objects.filter(store="c-cup").count()
	dic['舞茶道'] = Store_Info.objects.filter(store="sadou").count()
	dic['鮮茶道'] = Store_Info.objects.filter(store="presotea").count()
	dic['COCO'] = Store_Info.objects.filter(store="coco").count()
	dic['ComeBuy'] = Store_Info.objects.filter(store="comebuy").count()
	dic['水巷茶弄'] = Store_Info.objects.filter(store="teaplus").count()
	dic['清玉'] = Store_Info.objects.filter(store="kingtea").count()
	dic['茶湯會'] = Store_Info.objects.filter(store="teapatea").count()
	dic['茶的魔手'] = Store_Info.objects.filter(store="teamagichand").count()
	asd={}
	# dic = sorted(dic, key=dic.get)
	all_Store = Store_Info.objects.all().order_by("store")
	for key,value in sorted(dic.iteritems(),key=lambda(k,v):(v,k),reverse=True):    
		print"%s: %s"%(key,value)
		asd[key] =value
	context= {'msg':asd,'all_Store':all_Store}
	return render(req,'index.html',context)


# def index(req):
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
 		# print msg[0]
 		# print msg[1]
 		# print msg[2]
 	
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



