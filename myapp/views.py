import operator

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    SignUpForm, 
    LoginForm, 
    TalkForm, 
    ImageSettingForm, 
    MailSettingForm, 
    PasswordChangeForm, 
    UserNameSettingForm,
    )
from django.db.models import Q
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.urls import reverse_lazy
from .models import Talk

User = get_user_model()


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        error_message = ''
    
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
    template_name = "myapp/logout.html"

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

@login_required
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
def user_img_change(request):
    user = request.user
    if request.method == "GET":
        form = ImageSettingForm(instance=user)

    elif request.method == "POST":
        form = ImageSettingForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_img_change_done")
        
        else:
             print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/user_img_change.html", context)
    
@login_required
def user_img_change_done(request):
    return render(request, "myapp/user_img_change_done.html")

@login_required
def mail_change(request):
    user = request.user
    if request.method == "GET":
        form = MailSettingForm(instance=user)

    elif request.method == "POST":
        form = MailSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("mail_change_done")
        
        else:
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/mail_change.html", context)
    
@login_required
def mail_change_done(request):
    return render(request, "myapp/mail_change_done.html")

@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UserNameSettingForm(instance=user)

    elif request.method == "POST":
        form = UserNameSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
        
        else:
            print(form.errors)

    context = {
        "form": form,
    }

    return render(request, "myapp/username_change.html", context)

@login_required
def username_change_done(request):
    return render(request, "myapp/username_change_done.html")
    
class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name ="myapp/password_change.html"

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = "myapp/password_change_done.html"
