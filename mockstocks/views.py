from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests
import stocks

VERIFY_TOKEN = '29thsept2016'
PAGE_ACCESS_TOKEN = 'EAAPaQJyu0WMBAAtXxDyHPZAAbcHHIaixe75auZCfLb0ysIJkeC1sf2bncRhRfjsopPvY8CZByFI6svVGPSI8es1oIRPaZBwdaXO2ex9KcH82cMworCESyeuTdzUB0Yge7d4XdsSo5yFYMsrvnk1kkqqaGAs4fX2yGmyZCUsRMRQZDZD'

def stock(message):
	code = stocks.get_code(message)
	print code
	url = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/jsonp?symbol=%s&callback=myFunction'%(code)
	resp = requests.get(url=url).text.split('(')[1].split(')')[0]
	data=json.loads(resp)
	output_text = ''
	output_text = 'Name: %s\nSymbol: %s\nOpen: %s\nLast Price: %s\nChange Percent: %s\nHigh: %s\nLow: %s'%(data['Name'],data['Symbol'],data['Open'],data['LastPrice'],data['ChangePercent'],data['High'],data['Low'])
	return output_text

def quick_response(fbid,code):
	post_fb_url='https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg_quick = {
				"recipient":{
				    "id":fbid
				  },
				  "message":{
				    "text":"View Chart",
				    "quick_replies":[
				      {
				        "content_type":"text",
				        "title":"Daily",
				        "payload":"daily:%s"%(code)
				      },
				      {
				        "content_type":"text",
				        "title":"Weekly",
				        "payload":"weekly:%s"%(code)
				      },
				      {
				        "content_type":"text",
				        "title":"Quit",
				        "payload":"quit"
				      }
				    ]
				  }
	}
	response_msg_quick = json.dumps(response_msg_quick)
	status2 = requests.post(post_fb_url, headers={"Content-Type": "application/json"},data=response_msg_quick)
	print status2.json()

def post_fb_msg(fbid,message):
	post_fb_url='https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	output_text = stock(message)
	code = stocks.get_code(message)
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text": output_text }})
	status1 = requests.post(post_fb_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status1.json()
	quick_response(fbid,code)

def handle_quickreply(fbid,payload):
	print 'payload=%s'%payload
	if payload == 'quit' or not payload:
		return
	payload, code = payload.split(':')
	print payload, code
	if payload == "daily":
		image_url = 'http://stockcharts.com/c-sc/sc?s=%s&p=D&b=5&g=0&i=t15810600769&r=1475241538081'%(code)
	elif payload == 'weekly':
		image_url = 'http://stockcharts.com/c-sc/sc?s=%s&p=W&b=5&g=0&i=t57136307326&r=1475242265838'%(code)

	response_msg_image = {
				"recipient":{
				    "id":fbid
				  },
				  "message":{
				    "attachment":{
				      "type":"image",
				      "payload":{
				        "url":	image_url
				      }
				    }
				  }
	}
	response_msg_image = json.dumps(response_msg_image)
	post_fb_url='https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	status3 = requests.post(post_fb_url, headers={"Content-Type": "application/json"},data=response_msg_image)
	print status3.json()
	quick_response(fbid,code)

class MyChatBotView(generic.View):
	def get(self,request,*args,**kwargs):
		if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self,request,*args,**kwargs):
		return generic.View.dispatch(self,request,*args,**kwargs)

	def post(self,request,*args,**kwargs):
		incoming_message=json.loads(self.request.body.decode('utf-8'))
		print incoming_message
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				try:
					if 'quick_reply' in message['message']:
						handle_quickreply(message['sender']['id'],message['message']['quick_reply']['payload'])
						return HttpResponse()

				except Exception as e:
					print e

				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					post_fb_msg(sender_id,message_text)
				except Exception as e:
					print e

		return HttpResponse()

def index(request):
	# return HttpResponse('hi')
	# return HttpResponse( post_fb_msg('12','hi') )
	return HttpResponse(handle_quickreply('123','daily:aapl'))
