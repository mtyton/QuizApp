from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Quiz, Question, Answer
from .forms import QuizCreateForm, RegisterForm, LoginForm, AddQuestionForm, AddAnswerToQuestionForm
from django.core.paginator import Paginator


class IndexView(View):
    def get(self, request):
        return render(request, "quiz/home.html")

    def post(self, request):
        pass


class LoginView(View):
    def get(self, request):
        form = LoginForm
        return render(request, "quiz/login.html", context={"form":form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form['login'].data
            password = form['password'].data

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user=user)
                return redirect(reverse("index"))
            else:
                return HttpResponse("error while loging in")
        else:
            return HttpResponse("error while geting form data")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "quiz/register.html", context={'form':form})

    def post(self, request):
        if request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form['login'].data
                password = form['password'].data
                confirmation = form['confirmation'].data
                email = form['email'].data
                if password == confirmation:
                    new_user = User.objects.create_user(username=username, email=email, password=password)
                    return redirect(reverse('index'))
                else:
                    return render(request, "quiz/register.html", context={'form': form})
            else:
                render(request, 'quiz/create.html', context={'form': form})
        else:
            return HttpResponse("error, work in progress")


class LogoutView(View):
    def get(self, request):
        user = request.user
        logout(request)
        return redirect(reverse("index"))


class CreateQuizView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = QuizCreateForm()
            return render(request, 'quiz/create.html', context={'form': form})
        else:
            return redirect(reverse("login"))

    def post(self, request):
        if request.user.is_authenticated:
            form = QuizCreateForm(request.POST)
            if form.is_valid():
                title = form['title'].data
                length = form['length'].data
                request.session['curr_len'] = int(length)
                owner = request.user
                new_quiz = Quiz.objects.create(title=title, length=length, owner=owner)
                new_quiz.save()
                return redirect(reverse('add_questions', args=(new_quiz.id, )))
            else:
                return redirect(reverse("login"))
        else:
            return redirect(reverse("login"))


class AddQAView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            quiz = Quiz.objects.get(id=pk)
            question_form = AddQuestionForm()
            answer_form = AddAnswerToQuestionForm()
            return render(request, "quiz/add.html", context={'answer_form': answer_form, "question_form":question_form})
        else:
            return redirect(reverse("login"))

    def post(self, request, pk):
        if request.user.is_authenticated:
            quiz = Quiz.objects.get(id=pk)
            question_form = AddQuestionForm(request.POST)
            if question_form.is_valid():
                question = Question.objects.create(text=question_form['text'].data, quiz=quiz)
                answer_form = AddAnswerToQuestionForm(request.POST)
                if answer_form.is_valid():
                    answers = self.get_ans(answer_form)
                    for ans in answers:
                        obj_ans = Answer.objects.create(ans_text=ans['text'], correct=ans['correct'],
                                                        question=question)
                        obj_ans.save()
                if request.session['curr_len'] == 1:
                    return redirect((reverse("index")))
                else:
                    question_form = AddQuestionForm()
                    answer_form = AddAnswerToQuestionForm()
                    request.session['curr_len']-=1
                    return render(request, "quiz/add.html",
                                  context={'answer_form': answer_form, "question_form": question_form})

            else:
                return HttpResponse("ERROR")

        else:
            return redirect(reverse("login"))

    def get_ans(self, form):
        answers=[]
        answers.append({"text":form['first_ans'].data, 'correct':form['first_corr'].value()})
        answers.append({"text": form['sec_ans'].data, 'correct': form['sec_corr'].value()})
        answers.append({"text": form['third_ans'].data, 'correct': form['third_corr'].value()})
        answers.append({"text": form['fourth_ans'].data, 'correct': form['fourth_corr'].value()})
        return answers


class QuizListView(View):
    def get(self, request):
        if request.user.is_authenticated:
            quizes = Quiz.objects.all()
            request.session['point'] = 0
            return render(request, "quiz/choose.html", context={'quiz_list':quizes})
        else:
            return redirect("index")


class PlayView(View):
    def get(self, request, pk):
        return self.generate_page(request, pk)

    def post(self, request, pk):
        msg=""
        id = request.POST.get("choice")
        answer = Answer.objects.get(id=id)
        if answer.correct:
            msg = "Your Answer was correct"
            request.session['point'] += 1
        else:
            msg="Your Answer was wrong"
        return self.generate_page(request, pk, msg, True)

    def generate_page(self, request, pk, message="please answer the Question", answered=False):
        if request.user.is_authenticated:
            quiz = Quiz.objects.filter(id=pk).first()
            question_list = Question.objects.filter(quiz=quiz)
            paginator = Paginator(question_list, 1)
            page = request.GET.get('page')
            questions = paginator.get_page(page)
            context = {"quiz": quiz, "questions": questions, 'answered':answered, 'msg':message}
            return render(request, "quiz/play.html", context=context)
        else:
            return redirect(reverse("index"))