

from django.urls import path
from . import views

urlpatterns = [

    path('validate_question',views.validate_question,name='validate_question'),
    path('',views.create_quiz,name='create_quiz'),
    path('create_question',views.create_question,name='create_question'),
    path('save_question',views.save_question,name='save_question'),
    path('get_quiz/<int:pk>',views.get_quiz,name='get_quiz'),
    path('quizes',views.ListQuiz.as_view(),name='ListQuiz'),
    path('save_score',views.save_score,name='save_score'),
    path('login',views.user_login,name='user_login'),
    path('register',views.register,name='register'),
    path('logout',views.user_logout,name='user_logout'),
    path('history/<str:quiz_name>',views.history,name='history'),
]
