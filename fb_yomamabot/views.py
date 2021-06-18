from django.http import request
from django.shortcuts import render
import json
import requests
import random
import re

# Create your views here.
# yomamabot/fb_yomamabot/views.py
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
# yomamabot/fb_yomamabot/views.py

jokes = {
         'aymen': ["""  you asked me about aymen Messaoudi this is his profile \n https://www.facebook.com/profile.php?id=100011318887418""",
                   ],
         'bonjour':    ["""bonjour""",
                    ],
         
         }


def post_facebook_message(fbid, recevied_message):
        # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':'EAAYRE09NJVMBABA0dOkrB6JXv2ZAWiRZA4iXYZBKrix8MeVi2QSihRwwTQA0QqmyujKouXWmMfjIKygssb2NiZApZAbqydzMBg1EVVPBwY1llEkHwIWYyZCiALHOJvj0lBC6NY8LsBlhCceUM6tCB4xIdIcctnrQAkjdHZAZBYF9h2i4xCoH75NezjiCUzMyPw5uhfEx9JqpHgZDZD'}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = 'hey :) '+user_details['first_name']+'..!' + ''
 
    for token in tokens:
        if token in jokes:
            joke_text += random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "sorry bro i cant understand u"    
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAYRE09NJVMBABA0dOkrB6JXv2ZAWiRZA4iXYZBKrix8MeVi2QSihRwwTQA0QqmyujKouXWmMfjIKygssb2NiZApZAbqydzMBg1EVVPBwY1llEkHwIWYyZCiALHOJvj0lBC6NY8LsBlhCceUM6tCB4xIdIcctnrQAkjdHZAZBYF9h2i4xCoH75NezjiCUzMyPw5uhfEx9JqpHgZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())
 # ...... code that selects and assigns the joke_text .... 
    #response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    #status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    # ..... code to post message ...
    # post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAYRE09NJVMBACPxw5z0r0kUaXwZBmSGNr4HEun2uffSMOfCHzlYh8vS2enZAs85FT3PFZASHH1uLhtw2wwPvmEeIx1jyHFyBnp7yrU7sOpd9yUR6lNUrtXZChwKepEAipe8wWHcZCLvCoymqjAIIbHqRZA1p43TnZCkLIPRVCKbb5hckUDJDMNQF2td3ZCF1Bxg3gnM00UWrgZDZD' 
    # response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    # status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    # pprint(status.json())
class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '123456':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    # Post function to handle Facebook messages

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
              if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
