from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from blog_generator.forms import CustomUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from pytube import YouTube
#import os
from django.conf import settings
import assemblyai as aai
#import openai
#OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Create your views here.
@login_required
def index(request):
    return render(request,'index.html')


def log_in(request):
     
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect('home')
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect('login')
        return render(request, 'templates/login.html')

def sign_up(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Success')
            return redirect('login')
    return render(request,'templates/signup.html',{'form':form})

def all_blogs(request):
    return render(request,'all-blog.html')

def blog_de(request):
    return render(request,'blog-details.html')

def log_out(request):
  
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout success")
    return redirect('home')
'''
@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            youtube_link = data.get('link')
            
            # Check if a valid YouTube link was provided
            if not youtube_link:
                return JsonResponse({"error": "Invalid YouTube link."}, status=400)

            # Title fetching (if needed)
            title = yt_title(youtube_link)

            # Get transcription
            transcription = get_transcription(youtube_link)
            if not transcription:
                return JsonResponse({'error': "Failed to get transcript"}, status=500)
            
            # Generate blog content
            blog_content = generate_blog_from_transcription(transcription)
            if not blog_content:
                return JsonResponse({'error': "Failed to generate blog article"}, status=500)

            return JsonResponse({
                "content": blog_content,
                "success": True,
            })
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"error": "Invalid request."}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
 
def yt_title(link):
    yt=YouTube(link)
    title=yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file,new_file)
    return new_file
    
def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = "215b875626e145ccbe9c90c68038d30e"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text

def generate_blog_from_transcription(transcription):
    prompt = f"Based on the following trnascript from a YouTube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = prompt,
        max_tokens =1000
        
    )
    generate_content = response.choices[0].text.strip()
    
    return generate_content
'''