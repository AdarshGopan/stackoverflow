"""stackoverflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from stackapi.views import QuestionView,AnswersView,QuestionDeleteView
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()
router.register("api/questions",QuestionView,basename="questions")
router.register("api/answers",AnswersView,basename="answers")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.SignUpView.as_view(),name="register"),
    path('login',views.LoginView.as_view(),name="signin"),
    path('stack/home',views.HomeView.as_view(),name="home"),
    path('questions/<int:id>/answers/add',views.add_answer,name="add-answer"),
    path('answer/<int:id>/upvotes/add',views.upvote_view,name="add-upvote"),
    path('stack/logout',views.sign_out,name="signout"),
    path('stack/myquestions/list',views.MyQuestions.as_view(),name="myquestions"),
    path("token/",ObtainAuthToken.as_view()),
    path("question/<int:pk>/",QuestionDeleteView.as_view(),name="delete-question"),
 ]+router.urls
#  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

