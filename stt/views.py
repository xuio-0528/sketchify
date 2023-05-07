from django.shortcuts import render

# Create your views here.
import openai
import os
from dotenv import load_dotenv

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@api_view(http_method_names=['POST'])
def stt(request):
    audio_data = request.FILES.get('audio')
    audio_file = open(audio_data, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return Response(status=status.HTTP_200_OK, data=[{"role": "user", "content": transcript["text"]}])