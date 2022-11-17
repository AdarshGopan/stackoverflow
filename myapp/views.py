from email import message
from urllib import request
from django.shortcuts import redirect, render

from myapp.forms import RegistrationForm,LoginForm,QuestionForm
from django.contrib.auth.models import User
from django.views.generic import View,CreateView,FormView,TemplateView,ListView
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from myapp.models import Questions,Answers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"U MUST LOGIN TO PERFORM THIS ACTION")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]
class SignUpView(CreateView):  
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"REGISTRATION SUCCESSFULLY COMPLETED")
        return super().form_valid(form)

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                messages.success(request,"LOGIN SUCCESFULLY")
                return redirect("home")
            else:
                messages.error(request,"LOGIN FAILED")
                return render(request,self.template_name,{"form":form})

@method_decorator(decs,name="dispatch")
class HomeView(CreateView,ListView):
    template_name: str="index.html"
    model=Questions
    form_class=QuestionForm
    success_url=reverse_lazy("home")
    context_object_name="questions"
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

decs
def add_answer(request,*args,**kwargs):
    q_id=kwargs.get("id")
    qst=Questions.objects.get(id=q_id)
    ans=request.POST.get("answer")
    qst.answers_set.create(answer=ans,user=request.user)
    return redirect("home")

# def view_answer(request,*args,**kwargs):
decs
def upvote_view(request,*args,**kwargs):
    ans_id=kwargs.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.up_vote.add(request.user)
    ans.save()
    print(request)
    return redirect("home")

decs
def sign_out(request,*args,**kwargs):
    logout(request)
    messages.success(request,"LOGOUT SUCCESSFULLY")
    return redirect("signin")

@method_decorator(decs,name="dispatch")
class MyQuestions(ListView):
    model=Questions
    context_object_name="questions"
    template_name="myquestions.html"

    def get_queryset(self):
        return Questions.objects.filter(user=self.request.user)