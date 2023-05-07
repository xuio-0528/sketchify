from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import openai
import os
from dotenv import load_dotenv
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import json

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "gpt-3.5-turbo"
max_tokens = 100
temperature = 0.7
top_p = 0.7



def convert_string_to_list(string):
    string = string[1:-1]
    string = string.replace(' {','{').replace(' }','}').replace('{ ','{').replace('} ','}').replace('},{','}/{')
    str_list = string.split('/')
    result = []
    for sl in str_list:
        dicts = eval(sl)
        result.append(dicts)
    return result

def initialize_message(user_name):
    prompt = []
    baseline_prompt = {"role": "system", "content": f"""
                    당신은 {user_name}님의 일기 작성을 돕는 비서 sketchify입니다. {user_name}님의 감정 상태에 따라 일기 작성을 도와주세요. 비서의 역할은 다음의 순서로 진행됩니다.
                    1. 어떤 일이 있었는지에 대한 이야기 들어주기
                    2. 그 일에 대한 감정 상태가 어떤지 물어보고 들어주기.
                    3. 혹시 더 하고 싶은 얘기가 있는지 묻고 들어주기.
                    4. 일기를 마치고 작성해주기. 일기의 시작에는 <를 끝에는 >를 붙여주세요. 한국어로 작성한 일기와 영어로 작성한 일기 각각을 제공해주세요. 일기는 30자 이내로 작성하세요.
                    일기 작성 돕기를 시작하세요."""
            }
    prompt.append(baseline_prompt)
    prompt .append({"role": "system", "content": f"""안녕하세요, {user_name}님. 일기 작성을 도와드리겠습니다. 어떤 일이 있으셨나요? 이야기를 들려주세요."""})
    return prompt

@api_view(http_method_names=['POST'])
def chat(request):
        
    data=json.loads(request.body)
    audio_data = request.FILES.get('audio')
    messages_data = data.get('messages')
    user_name = data.get('user_name')
    
    messages = convert_string_to_list(messages_data) if isinstance(messages_data, str) else messages_data
    
    if not messages:
        # generate initial message and gpt response
        prompt = initialize_message(user_name)
        response = openai.ChatCompletion.create(model = model_engine, messages=prompt)
        system_message = response["choices"][0]["message"]["content"]
        return Response(status=status.HTTP_200_OK, data=[{"role": "system", "content": system_message}])
    
    else:
        prompt = initialize_message(user_name)
        # audio = audio_data.open()
        # # audio_file = open(audio, "rb")
        # audio_file = audio
        # transcript = openai.Audio.transcribe("whisper-1", audio_file)
        # messages.insert(0, prompt)
        prompt.extend(messages)
        # prompt.append({"role": "user", "content": transcript["text"]})

        response = openai.ChatCompletion.create(model=model_engine, messages=prompt)
        system_message = response["choices"][0]["message"]["content"]
        # return Response(status=status.HTTP_200_OK, data=[{"role": "user", "content": transcript["text"]},{"role": "system", "content": system_message}])
        return Response(status=status.HTTP_200_OK, data=[{"role": "user", "content": messages[-1]['content']},{"role": "system", "content": system_message}])
