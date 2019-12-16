from django.urls import path, include
from .views import IndexView, CreateQuizView, RegisterView, LoginView, LogoutView, AddQAView
from .views import QuizListView, PlayView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create/", CreateQuizView.as_view(), name="create"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("add/<int:pk>", AddQAView.as_view(), name="add_questions"),
    path("list/", QuizListView.as_view(), name="list_view"),
    path("list/<int:pk>", PlayView.as_view(), name="play")
]