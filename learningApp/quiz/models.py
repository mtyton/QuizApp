from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=120)
    length = models.IntegerField(default=5)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=250)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_related_answers(self):
        answers = Answer.objects.filter(question=self)
        return answers


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=0)
    ans_text = models.CharField(max_length=250)

    def __str__(self):
        return "Answer {}, correctable {}, question {}".format(self.ans_text, self.correct, self.ans_text)


class Score(models.Model):
    points = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default=None)