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

def add_answer(request,*args,**kwargs):
    q_id=kwargs.get("id")
    qst=Questions.objects.get(id=q_id)
    ans=request.POST.get("answer")
    qst.answers_set.create(answer=ans,user=request.user)
    return redirect("home")

# def view_answer(request,*args,**kwargs):

def upvote_view(request,*args,**kwargs):
    ans_id=kwargs.get("id")
    ans=Answers.objects.get(id=ans_id)
    ans.up_vote.add(request.user)
    ans.save()
    return redirect("home")