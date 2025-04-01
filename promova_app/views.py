from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from promova_app.models import *
from openai import OpenAI
import requests

def index(request):
    return redirect('login')

def login(request):
    if request.method == 'POST':
        email_from_form = request.POST['email']
        try:
            passowrd = request.POST['password']
            the_user = Users.objects.get(email = email_from_form)
            if bcrypt.checkpw(passowrd.encode(),the_user.password.encode()):
                    request.session['user_id'] = the_user.id
                    return redirect('home') 
        except:
            pass
        messages.error(request,'Wrong email or passowrd try agin , or your account is not active!')
    return render(request,'login.html')

def signin(request):
    if request.method == 'POST':
        errors = Users.objects.validate(request.POST)
        if len(errors) > 0 :
            for key,value in errors.items():
                messages.error(request,value)
            return render(request,'signin.html')
        else:
            haspw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            Users.objects.create(
                name = request.POST['name'],
                company = request.POST['company'],
                email = request.POST['email'],
                phone = request.POST['phone'],
                password = haspw
            )
            messages.success(request,'You successfully rigistred , Please wait to activate your account !')
            return redirect('login')
    return render(request,'signin.html')
def home(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        context ={
            'user':Users.objects.get(id=user_id)
        }
        return render(request,'home.html',context)
    else:
        return redirect('/')

def talk(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        context ={
            'user':Users.objects.get(id=user_id),
            'chats':Chats.objects.filter(user = Users.objects.get(id = user_id))
        }
        if request.method == 'POST':
            base_url = "https://api.aimlapi.com/v1"
            api_key = "446eda63ca72487c9089bad3800d270d"
            system_prompt = "You are  market agent. Be descriptive and helpful. max pargraph is 265 words only."
            user_prompt = request.POST['talk']
            api = OpenAI(api_key=api_key, base_url=base_url)
            completion = api.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=256,
            )
            
            response = completion.choices[0].message.content
            context ={
                'questions': user_prompt,
                'answers':response,
                'user':Users.objects.get(id=user_id),
                'chats':Chats.objects.filter(user = Users.objects.get(id = user_id))
            }
            Chats.objects.create(
                question = user_prompt,
                answer = response,
                user = Users.objects.get(id = user_id)
            )
            return render(request,'talk.html',context)
        return render(request,'talk.html',context)
    else:
        return redirect('/')

def images(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        context= {
            'user':Users.objects.get(id=user_id),
            'images':Images.objects.filter(user = Users.objects.get(id=user_id))
        }
        if request.method == 'POST':
            response = requests.post(
                "https://api.aimlapi.com/v1/images/generations",
                headers={
                    "Authorization": "Bearer 2f909e94d4694d09a362ac0531a834c7",
                    "Content-Type": "application/json"
                },
                json={  # Use 'json' instead of 'data' for proper JSON handling
                    "model": "dall-e-3",
                    "prompt": request.POST['img'],
                    "n": 1,
                    "quality": "standard",
                    "response_format": "url",
                    "size": "1024x1024",
                    "style": "vivid"
                }
            )
            data = response.json()
            print(data)
            img = data["data"][0]["url"]
            Images.objects.create(
                url = img,
                user = Users.objects.get(id=user_id)
            )
            context = {
                'img':img,
                'user_prompt':request.POST['img'],
                'user':Users.objects.get(id=user_id),
                'images':Images.objects.filter(user = Users.objects.get(id=user_id))
            }
            return render(request,'images.html',context)
        return render(request,'images.html',context)
    else:
        return redirect('/')

def videos(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        context = {
            'user':Users.objects.get(id = user_id)
        }
        if request.method == 'POST':
            url = "https://api.aimlapi.com/v2/generate/video/alibaba/generation"
            payload = {
            "model": "wan/v2.1/1.3b/text-to-video",
            "prompt": "playing baby",
            "aspect_ratio": "16:9",
            }
            headers = {
            "Authorization": "Bearer 446eda63ca72487c9089bad3800d270d",
            "Content-Type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)
            json_response = response.json()
            print("Generation:", response.json())
            url = "https://api.aimlapi.com/v2/generate/video/alibaba/generation"
            params = {
                "generation_id": json_response["id"],
            }
            headers = {"Authorization": "Bearer 446eda63ca72487c9089bad3800d270d", "Content-Type": "application/json"}

            response = requests.get(url, params=params, headers=headers)
            print("Generation:", response.json())
            print(response["video"]["url"])
            return render(request,'video.html',context)
        return render(request,'video.html',context)
    else:
        return redirect('/')

def contact(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        context = {
            'user':Users.objects.get(id=user_id)
        }
        if request.method == 'POST':
            MessagesFromUser.objects.create(
                message = request.POST['contact'],
                user = Users.objects.get(id =user_id)
            )
            return redirect('home')
        else:
            return render(request,'contact-us.html',context)
    else:
        return redirect('/')

def logout(request):
    del request.session['user_id']
    return redirect('/')



# Create your views here.
