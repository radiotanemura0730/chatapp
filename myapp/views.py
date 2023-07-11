from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login
from .forms import SignUpForm

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        error_message = ""
    
    elif request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("/")
        
        else:
            print(form.errors)


    context = {
        "form": form,
    }
    return render(request, "myapp/signup.html", context)


def login_view(request):
    return render(request, "myapp/login.html")

def friends(request):
    return render(request, "myapp/friends.html")

def talk_room(request):
    return render(request, "myapp/talk_room.html")

def setting(request):
    return render(request, "myapp/setting.html")

