import operator

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, LoginForm, TalkForm
from django.db.models import Q
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from .models import Talk

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

class Login(LoginView):
        
    authentication_form = LoginForm
    template_name = "myapp/login.html"

class Logout(LoginRequiredMixin, LogoutView):
    pass

@login_required
def friends(request):
    user = request.user
    friends = User.objects.exclude(id=user.id)

    info = []
    info_have_message = []
    info_have_no_message = []

    for friend in friends:
        latest_message = Talk.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
        ).order_by('time').last()

        if latest_message:
            info_have_message.append([friend, latest_message.talk, latest_message.time])
        else:
            info_have_no_message.append([friend, None, None])

    info_have_message = sorted(info_have_message, key=operator.itemgetter(2))

    info.extend(info_have_message)
    info.extend(info_have_no_message)

    context = {
        "info": info,
    }
    return render(request, "myapp/friends.html", context)
    
@login_required
def talk_room(request, user_id):

    user = request.user
    friend = get_object_or_404(User, id=user_id)

    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).order_by("time")

    form = TalkForm()
    context = {
        "form": form,
        "talk": talk,
        "friend": friend,
    }

    if request.method == "POST":
        new_talk = Talk(talk_from=user, talk_to=friend)
        form = TalkForm(request.POST, instance=new_talk)

        if form.is_valid():
               
            form.save()

            return redirect("talk_room", user_id)
            
        else:

            print(form.errors)

    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

