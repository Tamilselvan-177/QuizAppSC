from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=255)

    def __str__(self):
        return self.topic_name

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text



class QuizAttempt(models.Model):
    attempt_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    score = models.IntegerField()
    attempt_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.email} - {self.topic.topic_name} - {self.score}"

class UserResponse(models.Model):
    response_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.email} - {self.question.question_text} - {self.selected_answer}"
