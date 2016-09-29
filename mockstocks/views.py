from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests

VERIFY_TOKEN = '29thsept2016'
PAGE_ACCESS_TOKEN = 'EAAPaQJyu0WMBAOfZCNmHLsNUxq5cMBmeZBBgNO2ZBeYmEAnoJRtS5PzNd72ZC0fezaOaZC3jzL3wHTguXwwypolfvQiZCDdflHoVboh51dbCCDwTs0RZBRtlxFIWzhKgSLXJhUz5djAJK3KUpURnno607ydfD8vwzHEnBMbTHODpwZDZD'

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
					sender_id = message['sender']['id']
					message_text = message['message']['text']
				except Exception as e:
					print e

		return HttpResponse()

def index(request):
	return HttpResponse('hi')