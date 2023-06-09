from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_id = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Answer(models.Model):
    answer_text = models.TextField()
    for_question = models.ForeignKey(Question,on_delete=models.CASCADE) 
    given_by = models.ForeignKey(User,on_delete=models.CASCADE)
    given_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.answer_text