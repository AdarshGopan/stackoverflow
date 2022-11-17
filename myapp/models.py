from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
# Create your models here.
class Questions(models.Model):
    question=models.CharField(max_length=400)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    @property
    def fetch_answers(self):
        answers=self.answers_set.all().annotate(up_count=Count('up_vote')).order_by('-up_count')
        return answers
        

    def __str__(self):
        return self.question

class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    up_vote=models.ManyToManyField(User,related_name="upvotes")
    
    @property
    def up_vote_count(self):
        return self.up_vote.all().count()

    def __str__(self):
         return self.answer

# class UserProfiles(models.Model):
# 	pro_pic=models.ImageField()
# 	dob=models.DateField()
# 	address=models.CharField()
# 	user=models.OneToOneField(User,on_delete=models.CASCADE)


        # parent class act as to invoke child
# ====================================================
# usr
# <User: ammu>
# >>> Questions.objects.create(question="first question",user=usr)
# <Questions: first question>
# >>> usr=User.objects.get(id=1)
# >>> usr
# <User: adarsh>
# >>> usr.questions_set.create(question="this is adarsh question")
# <Questions: this is adarsh question>
# >>> usr=User.objects.get(id=3)
# >>> usr.questions_set.create(question="this is aromal  question")
# <Questions: this is aromal  question>
# >>>


# =============================================================
# >>> qst=Questions.objects.get(id=5)
# >>> qst
# <Questions: which country host mensT20 worldcup>
# >>> qst.answers_set.all()
# <QuerySet [<Answers: Australia>, <Answers: Qatar>]>
# >>> qst=Questions.objects.get(id=6)
# >>> qst
# <Questions: hosting country of FIFA worldcup 2022>
# >>> qst.answers_set.all()
# <QuerySet [<Answers: Qatar>, <Answers: india>]>
# >>> usr=User.objects.get(id=1)
# >>> usr.answers_set.all()
# <QuerySet [<Answers: Qatar>, <Answers: france>]>
# >>> usr.questions_set.all()
# <QuerySet [<Questions: this is adarsh question>, <Questions: which country host mensT20 worldcup>]>
# >>>


# up_vote add
# ========================================
# usr=User.objects.get(id=3)
# >>> usr
# <User: aromal>
# >>> ans=Answers.objects.get(id=1)
# >>> ans.up_vote.add(usr)
# >>> usr=User.objects.get(id=1)
# >>> ans.up_vote.add(usr)
# >>> ans.up_vote.all()  "TO GET VOTED USER "  
#   --->>> <QuerySet [<User: adarsh>, <User: aromal>]>
#  ans.up_vote.all().count() "TO COUNT"
# 2
# >>> 