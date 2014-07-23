	#coding=utf-8
from django.db import models

# Create your models here.
class Store_Info(models.Model):
	city_list =(
		('Keelung','基隆市'),
		('Taipei','台北'),
		('Xinbei','新北'),
		('Taoyuan','桃園'),
		('Hsinchu','新竹'),
		('Miaoli','苗栗'),
		('Taichung','台中'),
		('Nantou','南投'),
		('Changhua','彰化'),
		('Yunlin','雲林'),
		('Chiayi','嘉義'),
		('Tainan','台南'),
		('Kaohsiung','高雄'),
		('Pingtung','屏東'),
		('Ilan','宜蘭'),
		('Hualien','花蓮'),
		('Taitung','台東'),
		('Penghu','澎湖')
	)
	product = (
		('50lan', '50嵐'),
		('dayungs', '大苑子'),
		('orangetea', '橘子工坊'),
		('chingshin', '清心福全'),
		('teaplus', '水巷茶弄'),
		('c-cup', 'C-cup'),
		('presotea', '鮮茶道'),
		('sadou', '舞茶道'),
		('coco', 'COCO'),
		('comebuy', 'comebuy'),
		('kingtea', '清玉'),
		('teapatea', '茶湯會'),
		('teamagichand', '茶的魔手'),
	)
	store = models.CharField(max_length=10, choices=product,null=True,blank=True)
	store_name = models.CharField(max_length=10,null=True,blank=True)
	city = models.CharField(max_length=10, choices=city_list,null=True,blank=True)
	zone = models.CharField(max_length=5,null=True,blank=True)
	phone = models.CharField(max_length=30,null=True,blank=True)
	address = models.CharField(max_length=60,null=True,blank=True)
	location = models.CharField(max_length=200,null=True,blank=True)
	other = models.CharField(max_length=200,null=True,blank=True)
	def __unicode__(self):
		return self.store+self.city