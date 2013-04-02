#!/usr/bin/python
#encoding=utf-8

#renren login moduler
import httplib
import urllib, urllib2, cookielib, json, time, hashlib, re, sys
import random
import time
class Renren(object):
	def __init__(self,email,password,idn):
		self.email=email
		self.password=password
		self.idn=idn
		# 人人网的登录主页 
		self.origURL='http://www.renren.com/SysHome.do' 
		self.domain='renren.com' 
		self.requestToken='' 
		self.rtk='' 
		# 如果有本地cookie，登录时无需验证。 
		self.cj = cookielib.LWPCookieJar()
		try:
			self.cj.revert('renren.cookie')
			#print("OK"); 
		except:
			pass 
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(self.opener)
 
	def get_token(self,rawHtml):
		try:
			self.requestToken=re.findall('get_check:\'[\d-]*\'?',rawHtml)[0].split(':')[1].strip('\'')
			print self.requestToken
			self.rtk=re.findall('get_check_x:\'.*?\'',rawHtml)[0].split(':')[1].strip('\'')
			print self.rtk
			return True 
		except:
			return False 
 
	def login(self):
		"""模拟登录""" 
		# 通过查看renren页面源码，找到要填充的变量，如下面的'email', 'password'等 
		headers=[("User-Agent","Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1"),
		         ("Content-Type","application/x-www-form-urlencoded")]
		params = {'email':self.email,'password':self.password}
		# 进行编码，并请求 
		req = urllib2.Request(
		    'http://www.renren.com/PLogin.do',
		    urllib.urlencode(params)
		)
		self.opener.addheaders=headers
		r = self.opener.open(req)
		rawHtml=r.read()
		self.cj.save('renren.cookie')
		open('res.html','w').write(rawHtml)
		return self.get_token(rawHtml)
 
	def status(self, status):
		#发布状态 
		params = {'content':status,'hostid':self.idn,'requestToken':self.requestToken,'channel':'renren','_rtk':self.rtk}
		# 进行编码，并请求 
		req = urllib2.Request(
			'http://shell.renren.com/'+self.idn+'/status',
			urllib.urlencode(params)
		)
		rawHtml=self.opener.open(req).read()
		return self.get_token(rawHtml)
 

if __name__ == '__main__': 
	niu_email = "xxxxxxxx@gmail.com"
	niu_pass = "password"
	niu_idn = "youridn"
	yefeng = Renren(niu_email, niu_pass, niu_idn)
	yefeng.login()
	lasttime = "00"
	fromsolidot = "(Got from www.solidot.com)"
	print "Success\n"
	while True:
		if time.strftime('%H',time.localtime(time.time())) != lasttime:
			lasttime = time.strftime('%H',time.localtime(time.time()))
			conn = httplib.HTTPConnection("www.solidot.org")
			conn.request("GET", "/")
			r1 = conn.getresponse()
			data = r1.read()
			famous = data[data.find("class=\"famous\"") : ]
			famous = famous[famous.find(">")+1 :famous.find("</p>") ]
			yefeng.status(famous + fromsolidot)
