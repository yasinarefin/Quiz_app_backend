from django.db import models
from  User.models import User
from django.utils import timezone
# Create your models here.

class Quiz(models.Model):
    
    quiz_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    total_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_status(self):
        if self.start_time > timezone.now():
            return 'upcoming'
        elif self.end_time < timezone.now():
            return 'ended'
        else:
            return 'running'

    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time'])
        ]
    

    def __str__(self):
        return self.quiz_id


class Question(models.Model):
    quiz = models.OneToOneField(Quiz, on_delete = models.CASCADE, primary_key=True)
    question_count = models.IntegerField()
    questions = models.JSONField()
    answers = models.JSONField()
    def __str__(self):
        return self.pk

class Participation(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    answers = models.JSONField()
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['quiz']),
            models.Index(fields=['user']),
        ]
        

    
