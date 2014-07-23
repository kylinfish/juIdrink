 # -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,HttpResponse
from BeautifulSoup import BeautifulSoup
from info.models import Store_Info
import sys,requests,re
import operator

def index(req):
# def indexs(req):
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

	# dic = sorted(dic, key=dic.get)
	for key,value in sorted(dic.iteritems(),key=lambda(k,v):(v,k),reverse=True):    
		print"%s: %s"%(key,value)
	context= {'msg':dic}
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

def get_HTML_Content(url):
	reponse = requests.get(url)
	return reponse.content