from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateQuiz1.as_view(), name="create_quiz1"),
    path('marking/', views.CreateQuiz2.as_view(), name="create_quiz2"),
    path('update/<int:pk>',views.UpdateQuiz1.as_view(), name="update_quiz1"),
]