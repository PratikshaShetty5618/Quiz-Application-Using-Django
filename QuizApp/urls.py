from django.urls import path,include
from . import views

urlpatterns = [
    path('create/', views.CreateQuiz1.as_view(), name="create_quiz1"),
    path('marking/', views.create_quiz2, name="create_quiz2"),
    path('update/<int:pk>',views.UpdateQuiz1.as_view(), name="update_quiz1"),
    path('marking_update/<int:id>',views.update_quiz2, name ="update_quiz2"),
    path('easy_ques/', views.CreateEasyQuiz.as_view(),name = "easy_ques"),
    path('easy_ques_update/<int:pk>', views.UpdateEasyQuiz.as_view(),name = "easy_ques_update"),
    path('medium_ques/', views.CreateMediumQuiz.as_view(),name = "medium_ques"),
    path('medium_ques_update/<int:pk>', views.UpdateMediumQuiz.as_view(),name = "medium_ques_update"),
    path('hard_ques/', views.CreateHardQuiz.as_view(),name = "hard_ques"),
    path('hard_ques_update/<int:pk>', views.UpdateHardQuiz.as_view(),name = "hard_ques_update"),
    path('category_list/', views.CategoryList.as_view(), name = "category_list"),
    path('category_quiz/<str:category>', views.CategoryQuiz.as_view(), name = "category_quiz"),
    path('quiz_detail/<slug:slug>', views.QuizDetail.as_view(), name ="quiz_detail"),
    path('quiz_ques/<slug:slug>',views.QuizQuestions.as_view(), name = "quiz_ques"),
    path('quiz_submit/<slug:slug>',views.quiz_submit, name="quiz_submit")

]