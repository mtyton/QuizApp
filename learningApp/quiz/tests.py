from django.test import TestCase
from .models import Question, Quiz, Answer, User


class DBTest(TestCase):
    def setUp(self):
        pass

    def test_get_all_quizes(self):
        user = User.objects.create_user(username="test_user", email="test@gmail.com", password="zaq1@WSX")
        quiz = Quiz.objects.create(title="test", length=1, owner=user)
        quiz.save()
        quizes = Quiz.objects.all()
        self.assertEqual(len(quizes), 1)

    def test_get_question_for_quiz(self):
        user = User.objects.create_user(username="test_user", email="test@gmail.com", password="zaq1@WSX")
        quiz = Quiz.objects.create(title="test", length=1, owner=user)
        question = Question.objects.create(text="test_question", quiz=quiz)
        sec_question = Question.objects.create(text="sec_question", quiz=quiz)
        question.save()
        sec_question.save()
        questions = Question.objects.all()
        self.assertEqual(len(questions), 2)

    def test_get_ans_for_question(self):
        quiz = Quiz.objects.create()
        question = Question.objects.create()
        answers = question.get_related_answers()