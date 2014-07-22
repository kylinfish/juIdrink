from django.shortcuts import render,get_object_or_404,HttpResponse
from BeautifulSoup import BeautifulSoup
import sys



def index(req):

	#html
	data=[
		'<html>',
		'<head>',
		'<title>Title Hello</title>',
		'<body>HI',
		'<a href="test.html1" attr="1">Link1 </a>',
		'<a href="test.html2" attr="2">Link2 </a>',
		'</body>',
		'</html>'
	]
	soup = BeautifulSoup(''.join(data))
	body = soup.contents[0]
	context={'msg':body}
	print soup.findAll('a', href=True)
	return render(req,'index.html',context)