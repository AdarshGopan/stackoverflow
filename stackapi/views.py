from django.shortcuts import render

from rest_framework.response import Response
from stackapi.serializers import AnswerSerializer,QuestionSerializer
from myapp.models import Answers,Questions
from rest_framework import authentication,permissions,viewsets
from rest_framework.decorators import action
from stackapi.custompermissions import OwnerOrReadOnly
from rest_framework import mixins,generics
from rest_framework import serializers



class QuestionView(viewsets.ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]
    http_method_names=["get","post","put"]

    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     user=request.user
    #     serializer=QuestionSerializer(data=request.data,context={"user":user})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
 
    #localhost:8000/api/questions/1/add_answer/   
    @action(methods=["post"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        question=self.get_object()
        user=request.user
        serializer=AnswerSerializer(data=request.data,context={"user":user,"question":question})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    #localhost:8000/api/questions/5/answerslist/
    @action(methods=["get"],detail=True)
    def answerslist(self,request,*args,**kwargs):
        question=self.get_object()
        answer=question.answers_set.all()
        serializer=AnswerSerializer(answer,many=True)
        return Response(data=serializer.data) 
               
class QuestionDeleteView(mixins.DestroyModelMixin,generics.GenericAPIView):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[OwnerOrReadOnly]
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
class AnswersView(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated,OwnerOrReadOnly]
    authentication_classes=[authentication.TokenAuthentication]

    @action(methods=["post"],detail=True)
    def add_upvote(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        answer=Answers.objects.get(id=id)
        user=request.user
        answer.up_vote.add(user)
        answer.save()
        return Response(data="you upvoted successfully")


    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Answers.objects.get(id=id)
        if object.user == request.user:
            Answers.objects.filter(id=id).delete()
            return Response(data="successfully deleted")
        else:
            raise serializers.ValidationError("you don't have permission")
