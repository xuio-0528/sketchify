from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import openai
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def summary_and_drawing(input_sequence):

    image_prompt = "Give me a painting following the conversation." + input_sequence
    
    image_response = openai.Image.create(
        prompt=image_prompt,
        n=3,
        size="1024x1024"
    )
    
    return [image_response['data'][i]['url'] for i in range(3)]


@api_view(http_method_names=["POST"])
def image_generate(request):
    data=json.loads(request.body)
    image_url = None
    messages = request.data.get("messages")
    
    image_url  = summary_and_drawing(messages)

    return Response(status=status.HTTP_200_OK, data={"image0": image_url[0], "image1": image_url[1], "image2": image_url[2]})