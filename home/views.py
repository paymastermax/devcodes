from django.shortcuts import render,redirect
from django.http import HttpResponse
from account.models import Signup
from chatroom.models import ChatModel as chbt
from QandA.models import Questions as qa

def homeview(request):
    all_questions = qa.objects.all().order_by("-time_posted")
    try:
        userlog = request.session["username"]
        userinfo = Signup.objects.get(username = userlog)
        notifs = chbt.objects.filter(r2uid_id = userinfo.uid , bell_seen = False).count()
    except Exception as e:
        userlog = False
        return render(request , "home/home.html" , context = {"allq": all_questions , "userlog":userlog})

    else:
        userlog = True
        return render(request , "home/home.html" , context = {"userinfo":userinfo , "notifs":notifs , "allq": all_questions , "userlog":userlog , "newmessage":notifs})


def Policies(request):
    return render(request , "home/privacy.html")
