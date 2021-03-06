from django.shortcuts import render , redirect
from account.models import Signup
from .forms import anserform
from django.db.models import Count
from .models import Questions , Answers , QuestionLike as qlike
from chatroom.models import ChatModel as chtb
from chatroom.models import FeedBack as fd
from django.http import JsonResponse , HttpResponse
from itertools import chain
import json,datetime

def custom_userquestions(userinfo):
    try:
        custom_q_questions = Questions.objects.all().annotate(no_of_answers = Count("question_to_answer")).order_by("-time_posted").filter(language__icontains = userinfo.hobby)
        the_rest_question = Questions.objects.all().annotate(no_of_answers = Count("question_to_answer")).order_by("-time_posted").exclude(language__icontains = userinfo.hobby)
        all_questions = chain(custom_q_questions , the_rest_question)
    except Exception as e:
        all_questions = Questions.objects.all().annotate(no_of_answers = Count("question_to_answer")).order_by("-time_posted")
        return all_questions
    else:
        return all_questions
def questionsview(request):
    try:
        userdetails = Signup.objects.get(username = request.session["username"])
        all_questions = custom_userquestions(userdetails)
        newmessage = chtb.objects.filter(r2uid_id =  userdetails.uid, bell_seen = False).count()
        userlog = True
    except Exception as e:
        userlog = False
        request.session["redirect"] = "/questions/"
        return redirect("/account/")
        return render(request , "questions/questions.html" , context = {"Questions":all_questions , "userlog":userlog})
    else:
        return render(request , "questions/questions.html" , context = {"Questions":all_questions , "mydetails":userdetails , "newmessage":newmessage , "userlog":userlog})

def myquestions(request):
    try:
        userdetails = Signup.objects.get(username = request.session["username"])
        newmessage = chtb.objects.filter(r2uid_id =  userdetails.uid, bell_seen = False).count()
        userlog = True
    except Exception as e:
        userlog = False
        request.session["redirect"] = "/questions/myquestions/"
        return redirect("/login/")
    else:
        all_questions = Questions.objects.filter(quid_id = userdetails.uid).annotate(no_of_answers = Count("question_to_answer")).order_by("-time_posted")
        return render(request , "questions/personal.html" , context = {"Questions":all_questions , "mydetails":userdetails , "newmessage":newmessage , "userlog":userlog})
def answersview(request , Qid):
    answers_form = anserform()

    allanswers = Answers.objects.filter(question_to_answer_id = Qid)
    question_info = Questions.objects.get(qid = Qid)
    try:
        userdetails = Signup.objects.get(username = request.session["username"])
        userlog = True
    except Exception as e:
        userlog = False
        return render(request , "questions/answers.html" , context = {"userdetails":"userdetails" , "answers_form":answers_form , "Qid":Qid , "allanswers":allanswers , "question_info":question_info , "newmessage":0})
    else:
        newmessage = chtb.objects.filter(r2uid_id =  userdetails.uid, bell_seen = False).count()
        return render(request , "questions/answers.html" , context = {"userdetails":userdetails , "answers_form":answers_form , "Qid":Qid , "allanswers":allanswers , "question_info":question_info , "newmessage":newmessage , "userlog":userlog})

def askquestionsview(request):
    if request.method == "POST":
        try:
            userdetails = Signup.objects.get(username = request.session["username"])
            questionlang = request.POST["language"]
            question = request.POST["question"]
        except Exception as e:
            request.session["redirect"] = "/questions/updatequestions/"
            return redirect("/login/")
        else:
            Questions.objects.create(quid_id = userdetails.uid, question = question , language = questionlang)
            return redirect("/questions/")
    else:
        return redirect("/questions/")


def update_answers(request , Qid):
    if request.method == "POST":
        try:
            userdetails = Signup.objects.get(username = request.session['username'])
            answerquery = request.POST["answer"]
        except Exception as e:
            request.session["redirect"] = "/questions/updateanswers/{}/".format(Qid)
            return redirect("/login/")
        else:
            Answers.objects.create(auid_id = userdetails.uid , question_to_answer_id = Qid , answer = answerquery)
            return redirect("/questions/answers/{}/".format(Qid))
    else:
        return redirect("/questions/answers/{}/".format(Qid))

# check if the user has liked or not
def checklikes(qid , uid):
    try:
        qdata = [value.luid_id for value in qlike.objects.filter(Qid_id = qid)]
    except Exception as e:
        return False
    else:
        if uid in qdata:
            return True
        else:
            return False

# update likes
def updatelikes(request):
    try:
        userdetails = Signup.objects.get(username = request.session['username'])
    except Exception as e:
        is_logged = False
        status = False
        liked = "question not liked"
    else:
        Qid = request.POST["qid"]
        if not checklikes(Qid , userdetails.uid):
            qlike.objects.create(Qid_id = Qid , luid_id = userdetails.uid)
        is_logged = True
        liked = "question liked"
        status = True
    data = {"status":status , "liked":liked,"is_logged":is_logged , "counter":Questions.objects.get(qid = Qid).question_liked.count()}
    return JsonResponse(data)
def feed(request):
    user_mail = request.POST["email"]
    feed = request.POST["feedback"]
    fd.objects.create(feedback_sender = user_mail, feedback = feed)
    return JsonResponse({"feedback":True})

def deleteQuestion(request):
    try:
        target_id = request.POST["Qid"]
        target_data = Questions.objects.get(qid = target_id)
        assoc_ans = Answers.objects.filter(question_to_answer_id = target_id)
        target_like = qlike.objects.filter(Qid_id = target_id)
        target_data.delete()
        assoc_ans.delete()
        target_like.delete()
    except Exception as e:
        data = {"pass":False}
    else:
        data = {"pass":True}
    return HttpResponse(json.dumps(data) , content_type = "application/json")

def editQuestion(request):
    try:
        id = request.POST["target_id"]
        content = request.POST["content"]
    except Exception as e:
        data = {
                "Status":False,
                "Message":"Could not save your edition."
        }
    else:
        data = {
            "Status":True,
            "Message":"Message updated",
            "timestamp":"0 sec(s) ago"

        }
        try:
            target_model = Questions.objects.get(qid = id)
            if (content !="") & (target_model.question != content):
                target_model.question = content
                target_model.time_posted = datetime.datetime.now()
                target_model.save()
        except Exception as e:
            data = {
                    "Status":True
                    }
    return HttpResponse(json.dumps(data) , content_type="application/json")
