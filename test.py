import sys
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


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

print soup.findAll('a', href=True)
